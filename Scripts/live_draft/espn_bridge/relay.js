// relay.js -- isolated world.  The MAIN-world hook cannot talk to the extension, and the page
// cannot reach localhost, so this sits between them and hands everything to the service worker.
window.addEventListener('message', (ev) => {
  const m = ev.data;
  if (!m || m.__espnBridge !== true) return;
  try { chrome.runtime.sendMessage(m); } catch (e) {}
});
