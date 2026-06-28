# 온기 Split Workspace

This is a local clickable prototype workspace for member-6's older-adult peer check-in service.

## Open

- Open `index.html` in this folder to choose a side
- Or open `elder-side/index.html` / `worker-side/index.html` directly

## Included Structure

- `elder-side/`: older-adult user app
- `worker-side/`: social-worker operations screen
- `shared/`: shared mock data used by both sides

## Elder-side Included Flows

- First screen with four large actions
- ID-based one-to-one chat with each connected person
- Ask/check-in and answer phrases integrated as quick messages inside the one-to-one chat
- Reply-assist choices that react to the other person's latest question
- Connection list shows app IDs and shared interests only
- Group chat room still exists, but only IDs are shown
- Voice input helper with browser-support fallback
- Microphone permission and device check before voice input
- Help/report with a clear emergency-service boundary

## Boundaries

- No backend, login, database, real matching, GPS, or notification system
- Reply-assist choices are local prototype logic, not a real server-side call
- No medical diagnosis, medication management, emergency dispatch, or welfare case management
- No real-name, exact address, phone number, or detailed health-information exposure
