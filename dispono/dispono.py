import asyncio
import sys
from pathlib import Path

import aiohttp_cors
import socketio
from aiohttp import web

static_folder = Path(__file__).parent / 'static'


class Dispono:
    def __init__(self, task=None, port: int = 8080):
        self.__port = port
        self._sio = socketio.AsyncServer(cors_allowed_origins="*")
        self._app = web.Application()

        self._sio.attach(self._app)

        self._cors = aiohttp_cors.setup(self._app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        self._cors.add(self._app.router.add_get('/', self.__frontend))
        self._cors.add(self._app.router.add_static('/img', static_folder / 'img'))

        self._sio.on('connect', self.__connect)
        self._sio.on('disconnect', self.__disconnect)
        self._sio.on('stdout', self.__on_stdout)
        self._sio.on('stderr', self.__on_stderr)

        self._sid = None
        self.__task = task

        self._sio.start_background_task(self.__wait_for_connection)

        web.run_app(self._app, port=self.__port, print=None)

    # Server functions.
    async def __frontend(self, request):
        with (static_folder / 'coding_game.js').open() as file:
            content = file.read()
        content = content.replace('<PORT>', str(self.__port))
        return web.Response(text=content, content_type='text/html')

    # SIO functions.
    async def __connect(self, sid, environ):
        print('Browser IDE connected')
        self._sid = sid
        self._sio.start_background_task(self.__run_background_task)

    async def __disconnect(self, sid):
        print('Browser IDE disconnected')
        await self._sio.disconnect(sid)

    async def sync_code(self, code):
        async def done():
            done_event.set_result(True)

        done_event = asyncio.Future()

        await self._sio.emit('syncCode', code, room=self._sid, callback=done)
        await done_event

    async def run_code(self):
        async def done():
            done_event.set_result(True)

        done_event = asyncio.Future()

        await self._sio.emit('runCode', room=self._sid, callback=done)
        await done_event

    async def __on_stdout(self, sid, data):
        print(data, flush=True, file=sys.stdout)

    async def __on_stderr(self, sid, data):
        print('\033[31m', end='')
        print(data, flush=True, file=sys.stderr)
        print('\033[0m', end='')

    async def __run_background_task(self):
        if self.__task:
            await self.__task(self)

        await self._sio.close_room(self._sid)

        await self._app.shutdown()
        await self._app.cleanup()

        # Silent termination of server.
        from os import _exit
        _exit(0)

    def __init_script(self):
        return """fetch('http://localhost:{}/').then(c => c.text()).then((s => eval(s)()));""".format(self.__port)

    async def __wait_for_connection(self):
        await asyncio.sleep(3)
        if not self._sid:
            print('\033[31mNo browser IDE found.', 'Run the following JS code inside the web console:',
                  file=sys.stderr)
            print('\n\t', self.__init_script(), '\n\033[0m', file=sys.stderr)
