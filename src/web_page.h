#pragma once

#include <Arduino.h>

const char WEB_PAGE[] PROGMEM = R"HTML(
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f3f5f1">
  <title>Klipsch-Drehplatte</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #172b27;
      --muted: #526661;
      --surface: #ffffff;
      --ground: #f3f5f1;
      --line: #d8e2dc;
      --accent: #0b6758;
      --accent-dark: #064f43;
      --error: #a02e27;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--ground);
      color: var(--ink);
      font: 16px/1.5 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    main {
      width: min(100%, 560px);
      margin: 0 auto;
      padding: max(28px, env(safe-area-inset-top)) 20px max(36px, env(safe-area-inset-bottom));
    }
    .eyebrow {
      margin: 0 0 8px;
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .13em;
      text-transform: uppercase;
    }
    h1 { margin: 0; font-size: clamp(29px, 8vw, 40px); line-height: 1.12; letter-spacing: -.035em; }
    .intro { margin: 12px 0 28px; color: var(--muted); }
    .panel {
      padding: 28px 22px 24px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--surface);
      box-shadow: 0 14px 40px rgba(23, 43, 39, .07);
    }
    .panel-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
    h2 { margin: 0; font-size: 21px; line-height: 1.25; letter-spacing: -.02em; }
    .subtle { margin: 8px 0 0; color: var(--muted); }
    .badge {
      flex: none;
      padding: 6px 11px;
      border-radius: 999px;
      background: #e6f1ed;
      color: var(--accent-dark);
      font-size: 13px;
      font-weight: 700;
    }
    .badge.offline { background: #f9e9e6; color: var(--error); }
    .directions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-top: 30px; }
    .direction-button {
      display: flex;
      min-height: 142px;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 2px solid var(--accent-dark);
      border-radius: 20px;
      background: var(--accent);
      color: #ffffff;
      font: inherit;
      font-size: 18px;
      font-weight: 800;
      touch-action: none;
      user-select: none;
      -webkit-user-select: none;
      -webkit-touch-callout: none;
      cursor: pointer;
      transition: transform .12s ease, background-color .16s ease, opacity .16s ease;
    }
    .direction-button svg { width: 42px; height: 42px; }
    .direction-button:active, .direction-button.pressed { transform: scale(.97); background: var(--accent-dark); }
    .direction-button:focus-visible { outline: 3px solid #88c7b6; outline-offset: 3px; }
    .direction-button:disabled { opacity: .42; cursor: not-allowed; }
    .hint { margin: 16px 0 0; color: var(--muted); text-align: center; font-size: 14px; }
    .divider { height: 1px; margin: 24px 0 18px; background: var(--line); }
    .status { min-height: 26px; margin: 0; color: var(--muted); text-align: center; }
    .status.error { color: var(--error); }
    .footnote { margin: 22px 2px 0; color: var(--muted); font-size: 14px; }
    @media (max-width: 380px) {
      main { padding-inline: 14px; }
      .panel { padding: 24px 17px 20px; }
      .panel-head { display: block; }
      .badge { display: inline-block; margin-top: 14px; }
      .direction-button { min-height: 128px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .direction-button { transition: none; }
    }
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">Lokale Steuerung</p>
    <h1>Klipsch-Drehplatte</h1>
    <p class="intro">Richtungstaste halten. Beim Loslassen stoppt der Motor.</p>

    <section class="panel" aria-labelledby="control-title">
      <div class="panel-head">
        <div>
          <h2 id="control-title">Drehung steuern</h2>
          <p class="subtle">Der Motor läuft langsam, solange du drückst.</p>
        </div>
        <span id="connection" class="badge offline">Verbinde …</span>
      </div>

      <div class="directions" aria-label="Drehrichtung wählen">
        <button id="left" class="direction-button" type="button" aria-label="Nach links drehen, halten zum Fahren" aria-pressed="false" disabled>
          <svg viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M25 9 10 24l15 15M11 24h27" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>Links</span>
        </button>
        <button id="right" class="direction-button" type="button" aria-label="Nach rechts drehen, halten zum Fahren" aria-pressed="false" disabled>
          <svg viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="m23 9 15 15-15 15m14-15H10" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>Rechts</span>
        </button>
      </div>
      <p class="hint">Taste loslassen oder Verbindung verlieren stoppt die Bewegung.</p>
      <div class="divider"></div>
      <p id="status" class="status" role="status" aria-live="polite">Verbindung wird geprüft …</p>
    </section>
    <p class="footnote">Der Motor hält seine Position, solange der Treiber mit Strom versorgt wird.</p>
  </main>

  <script>
    const leftButton = document.getElementById('left');
    const rightButton = document.getElementById('right');
    const buttons = [leftButton, rightButton];
    const statusText = document.getElementById('status');
    const connection = document.getElementById('connection');
    let online = false;
    let busy = false;
    let holding = false;
    let activeButton = null;
    let startRequest = Promise.resolve();
    let keepAliveTimer = null;

    function showStatus(message, error = false) {
      statusText.textContent = message;
      statusText.classList.toggle('error', error);
    }

    function renderControls() {
      for (const button of buttons) {
        button.disabled = !online || (busy && !holding);
        const pressed = button === activeButton && holding;
        button.classList.toggle('pressed', pressed);
        button.setAttribute('aria-pressed', String(pressed));
      }
      connection.textContent = online ? 'Verbunden' : 'Keine Verbindung';
      connection.classList.toggle('offline', !online);
    }

    async function post(path, body = '') {
      const response = await fetch(path, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
        cache: 'no-store'
      });
      if (!response.ok) throw new Error(response.status === 409 ? 'Der Motor ist noch beschäftigt.' : 'Befehl wurde abgelehnt.');
      return response.json();
    }

    async function refreshStatus() {
      if (holding) return;
      try {
        const response = await fetch('/api/status', { cache: 'no-store' });
        if (!response.ok) throw new Error('status');
        const data = await response.json();
        online = true;
        busy = data.busy === true;
        showStatus(busy ? 'Motor bewegt sich …' : data.state === 'stopped' ? 'Gestoppt. Zum Fahren eine Richtung halten.' : 'Bereit.');
      } catch (_) {
        online = false;
        busy = false;
        showStatus('Keine Verbindung. WLAN und Seite prüfen.', true);
      }
      renderControls();
    }

    async function stopHold(message = 'Gestoppt. Taste zum Fahren erneut halten.') {
      if (!holding) return;
      holding = false;
      busy = false;
      if (keepAliveTimer !== null) clearInterval(keepAliveTimer);
      keepAliveTimer = null;
      activeButton = null;
      renderControls();
      try {
        await startRequest.catch(() => {});
        await post('/api/stop');
        showStatus(message);
      } catch (_) {
        showStatus('Stopp gesendet. Bei WLAN-Ausfall stoppt der Motor automatisch.', true);
      }
      renderControls();
      setTimeout(refreshStatus, 250);
    }

    function startHold(direction, button) {
      if (!online || busy || holding) return;
      holding = true;
      busy = true;
      activeButton = button;
      showStatus(`Dreht nach ${direction} … loslassen stoppt.`);
      renderControls();
      startRequest = post('/api/hold', `direction=${direction}`);
      startRequest.then(() => {
        if (!holding) return;
        keepAliveTimer = setInterval(async () => {
          if (!holding) return;
          try {
            await post('/api/keepalive');
          } catch (_) {
            await stopHold('Verbindung unterbrochen. Der Motor wurde gestoppt.');
          }
        }, 200);
      }).catch(async (error) => {
        const wasHolding = holding;
        holding = false;
        busy = false;
        activeButton = null;
        if (keepAliveTimer !== null) clearInterval(keepAliveTimer);
        keepAliveTimer = null;
        if (wasHolding) {
          try { await post('/api/stop'); } catch (_) {}
        }
        showStatus(error.message || 'Bewegung konnte nicht gestartet werden.', true);
        renderControls();
      });
    }

    function bindHold(button, direction) {
      button.addEventListener('pointerdown', (event) => {
        if (event.button !== undefined && event.button !== 0) return;
        event.preventDefault();
        try { button.setPointerCapture(event.pointerId); } catch (_) {}
        startHold(direction, button);
      });
      button.addEventListener('pointerup', () => stopHold());
      button.addEventListener('pointercancel', () => stopHold());
      button.addEventListener('lostpointercapture', () => stopHold());
      button.addEventListener('contextmenu', (event) => event.preventDefault());
      button.addEventListener('keydown', (event) => {
        if ((event.key === ' ' || event.key === 'Enter') && !event.repeat) {
          event.preventDefault();
          startHold(direction, button);
        }
      });
      button.addEventListener('keyup', (event) => {
        if (event.key === ' ' || event.key === 'Enter') {
          event.preventDefault();
          stopHold();
        }
      });
    }

    bindHold(leftButton, 'left');
    bindHold(rightButton, 'right');
    window.addEventListener('blur', () => stopHold('Fenster verlassen. Der Motor wurde gestoppt.'));
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stopHold('Seite verlassen. Der Motor wurde gestoppt.');
    });
    window.addEventListener('beforeunload', () => {
      if (holding) fetch('/api/stop', { method: 'POST', keepalive: true }).catch(() => {});
    });

    renderControls();
    refreshStatus();
    setInterval(refreshStatus, 1200);
  </script>
</body>
</html>
)HTML";
