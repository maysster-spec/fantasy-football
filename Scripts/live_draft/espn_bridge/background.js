// background.js -- the only piece allowed to talk to localhost.  Content scripts are subject to
// CORS; an MV3 service worker with host_permissions is not.
const ENDPOINT = 'http://127.0.0.1:8787/pick';
let queue = [], flushing = false, dropped = 0;

chrome.runtime.onMessage.addListener((msg) => {
  if (!msg || msg.__espnBridge !== true) return;
  queue.push(msg);
  if (queue.length > 500) { queue.splice(0, queue.length - 500); dropped++; }
  flush();
});

async function flush() {
  if (flushing || !queue.length) return;
  flushing = true;
  const batch = queue.splice(0, 40);
  try {
    await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dropped, events: batch }),
    });
    dropped = 0;
  } catch (e) {
    queue.unshift(...batch);          // listener not up yet -- keep them
  }
  flushing = false;
  if (queue.length) setTimeout(flush, 400);
}
