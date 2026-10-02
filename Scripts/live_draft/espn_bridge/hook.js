// hook.js -- runs in the PAGE's own world, before ESPN's scripts load.
//
// WHY THIS EXISTS: on 2026-09-02 we proved ESPN's REST read replica publishes a draft only AFTER
// it finishes (doc 136).  The live picks are in the browser the whole time -- which is why a
// FantasyPros extension can show them.  So we stop asking ESPN's server and listen to the page.
//
// It does TWO things, deliberately overlapping, because we do not yet know which one carries picks:
//   1. wraps WebSocket and forwards every frame
//   2. wraps fetch/XHR and forwards any response that mentions a playerId
// It PARSES NOTHING.  All interpretation happens in Python, where it can be fixed without
// reloading an extension.

(() => {
  const send = (kind, payload) => {
    try {
      window.postMessage({ __espnBridge: true, kind, at: Date.now(), payload }, '*');
    } catch (e) {}
  };

  // ---- 1. websocket frames -------------------------------------------------
  const RealWS = window.WebSocket;
  window.WebSocket = function (url, protocols) {
    const ws = protocols ? new RealWS(url, protocols) : new RealWS(url);
    send('ws-open', { url: String(url) });
    // v1.1 -- 2026-09-02.  THE FIRST VERSION THREW BINARY FRAMES AWAY.  It logged only their
    // size and returned, so if ESPN's KONA draft socket speaks binary the picks were discarded
    // silently and the console looked identical to "no picks arrived".  Both are now captured,
    // and a raw sample of EVERY frame is forwarded whether or not it matches a known shape --
    // a parser that only forwards what it already understands cannot tell you what it is missing.
    ws.addEventListener('message', (ev) => {
      const d = ev.data;
      if (typeof d === 'string') {
        send('ws-msg', { url: String(url), data: d.length > 200000 ? d.slice(0, 200000) : d });
        return;
      }
      try {
        if (d instanceof Blob) {
          d.text().then((t) => send('ws-msg', {
            url: String(url), binary: true,
            data: t.length > 200000 ? t.slice(0, 200000) : t })).catch(() => {});
        } else if (d instanceof ArrayBuffer || ArrayBuffer.isView(d)) {
          const buf = d instanceof ArrayBuffer ? d : d.buffer;
          const bytes = new Uint8Array(buf);
          let t = '';
          try { t = new TextDecoder('utf-8', { fatal: false }).decode(bytes); } catch (e) {}
          let b64 = '';
          try {
            let bin = '';
            for (let i = 0; i < bytes.length && i < 120000; i++) bin += String.fromCharCode(bytes[i]);
            b64 = btoa(bin);
          } catch (e) {}
          send('ws-msg', { url: String(url), binary: true, bytes: bytes.length,
                           data: t.slice(0, 200000), b64: b64.slice(0, 200000) });
        } else {
          send('ws-other', { url: String(url), type: Object.prototype.toString.call(d) });
        }
      } catch (e) { send('ws-error', { url: String(url), err: String(e) }); }
    });

    // what the CLIENT sends is often the subscribe/handshake that explains the reply format
    const realSend = ws.send.bind(ws);
    ws.send = function (payload) {
      try {
        if (typeof payload === 'string' && payload.length < 4000)
          send('ws-send', { url: String(url), data: payload });
      } catch (e) {}
      return realSend(payload);
    };
    return ws;
  };
  window.WebSocket.prototype = RealWS.prototype;
  Object.assign(window.WebSocket, RealWS);

  // ---- 2. fetch responses that look pick-shaped ----------------------------
  const looksLikePicks = (t) =>
    typeof t === 'string' && t.length > 80 &&
    /"playerId"|"overallPickNumber"|"pickNumber"|"draftDetail"/.test(t);

  const realFetch = window.fetch;
  window.fetch = async function (...args) {
    const res = await realFetch.apply(this, args);
    try {
      const url = (args[0] && args[0].url) || String(args[0]);
      res.clone().text().then((t) => {
        if (looksLikePicks(t)) send('fetch', { url, data: t.slice(0, 400000) });
      }).catch(() => {});
    } catch (e) {}
    return res;
  };

  // ---- 3. XHR, for anything not using fetch --------------------------------
  const RealXHR = window.XMLHttpRequest;
  function BridgeXHR() {
    const x = new RealXHR();
    let u = '';
    const open = x.open;
    x.open = function (m, url, ...rest) { u = String(url); return open.call(x, m, url, ...rest); };
    x.addEventListener('load', () => {
      try {
        const t = x.responseType === '' || x.responseType === 'text' ? x.responseText : null;
        if (looksLikePicks(t)) send('xhr', { url: u, data: t.slice(0, 400000) });
      } catch (e) {}
    });
    return x;
  }
  BridgeXHR.prototype = RealXHR.prototype;
  Object.assign(BridgeXHR, RealXHR);
  window.XMLHttpRequest = BridgeXHR;

  send('hooked', { href: location.href });
})();
