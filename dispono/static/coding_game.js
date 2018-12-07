/* global $ */

(function () {
	let core_io = null;
	let client = null;

	/**
	 * Updates the source code inside the editor.
	 */
	function updateSourceCode(sourceCode) {
		window.document.dispatchEvent(new CustomEvent("ExternalEditorToIDE", {
			detail: {
				status: "updateCode",
				code: sourceCode
			}
		}));
	}

	function transferConsoleOutput() {
		$(".frame-players").each(function () {
			$(this).find(".stderr > .outputLine").each(function () {
				client.emit('stderr', $(this).text());
			});
			$(this).find(".stdout > pre > .outputLine").each(function () {
				client.emit('stdout', $(this).text());
			});
		});
	}

	function waitUntilGameIsFinish(done) {
		if ($('.play.in-progress').length || $('.play-stop').length) {
			setTimeout(() => waitUntilGameIsFinish(done), 1000);
		} else {
			transferConsoleOutput();
			done();
		}
	}

	function loadUI() {
		// Change background of source code panel.
		const aceContent = $('.ace_content');
		if (!aceContent.length) {
			console.error("Could not find source code panel.");
			return;
		}
		aceContent.css('background-image', 'url("http://localhost:<PORT>/img/logo.svg")');
		aceContent.css('background-position', 'center center');
		aceContent.css('background-repeat', 'no-repeat');
		aceContent.css('background-size', '33% 33%');
	}

	function unloadUI() {
		$('.cg-ide-actions').off('DOMNodeInserted');
		$('#toolSyncButton').remove();
		$('.ace_content').css('background', '');
	}

	function addScriptTag(src) {
		return new Promise((resolve) => {
			const s = document.createElement('script');
			s.setAttribute('src', src);
			s.setAttribute('type', 'text/javascript');
			s.onload = () => resolve();
			document.body.appendChild(s);
		});
	}

	function initializeClient() {
		client = io('http://localhost:<PORT>', {
			reconnectionDelay: 2000,
			reconnectionDelayMax: 2000,
			timeout: 1000,
			forceNew: true
		});

		client.on('connect', () => {
			console.log("Server connected.");
		});

		client.on('disconnect', () => {
			console.log("Server disconnected.");
			client.disconnect();
			initializeClient();
		});

		client.on('syncCode', (sourceCode, done) => {
			console.log("Sync code.")
			updateSourceCode(sourceCode);
			done();
		});

		client.on('runCode', (_, done) => {
			console.log("Run code.")
			$('.play').click();
			waitUntilGameIsFinish(done);
		});
	}

	async function init() {
		if (typeof io === 'undefined') {
			// Load core.io-client.
			await addScriptTag('https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js');
		}
		initializeClient();

		loadUI();
	}

	init().catch((e) => {
		console.error(e);
	});
});
