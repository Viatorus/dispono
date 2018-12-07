![logo](https://raw.githubusercontent.com/Viatorus/dispono/master/artwork/logo_banner.png)

# Dispono
Dispono is a tool to synchronization your source code and run it inside a browser IDE.

It works cross-platform and cross-browser since it doesn't requires any plugins.

Currently supported browser IDE's:
* [CodinGame](https://www.codingame.com/)

## Installation

```
pip install dispono
```

Only **Python 3.6+** is supported.

## Usage

1. Write a python script:
    ```python
    from dispono import Dispono
   
   
    async def task(ide):
        await ide.sync_code('print("Hello browser. :)")')
        await ide.run_code()
    
   
    Dispono(task, port=8080)
    ```
    The above code will open a server at port 8080, transfer the code to your browser IDE and run the code.   

2. Open your browser IDE (e.g. a CodinGame contest).

3. Run the python script.
    
   When you start the script the first time, you have to execute a small javascript snippet inside the browser tab web
   console in order to connect to the server.

   All following runs will work out of the box for the same session.

## Advanced usage

### C/C++

In combination with [Quom](https://github.com/Viatorus/quom), your multi-file C/C++ project can be easily synced with 
your web IDE. Quom generates a single file from all local included header and source files.

```python
from io import StringIO

from dispono import Dispono
from quom import Quom


async def task(ide):
    dst = StringIO()
    Quom('main.cpp', dst)
    await ide.sync_code(dst.getvalue())
    await ide.run_code()


Dispono(task, port=8080)
```

## How does it work

Dispono starts a lightweight web server serving a javascript file for your specific browser IDE.

The javascript file contains code to control the IDE (sync/run/get output) and a client instance.

After registration the client by the server, the server can send commands to the client.
 
The communication between server and client happens with [socket.io](https://socket.io/). 

## Planned features

* Download code from web IDE.
* Correctly forward console output to the server.
* Support more web IDE's.
* Support multiple clients at the same time.
