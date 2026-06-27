# Peer Check-in Platform Split Workspace

This workspace restructures member-6's GitHub prototype into two separate local app folders.

## Folders

- `elder-side/`: older-adult user app based on the original member-6 prototype
- `worker-side/`: social-worker companion dashboard starter
- `shared/`: shared mock data used by both sides

## Open

- Open `index.html` in this folder to choose a side
- Or open `elder-side/index.html` directly for the original user-facing app flow

## Elder-side Included Flows

- First screen with four large actions
- ID-based one-to-one chat with each connected person
- Ask/check-in and answer phrases integrated as quick messages inside the one-to-one chat
- Reply-assist choices that react to the other person's latest question
- Connection list with app IDs, broad living area, and shared interests only
- Group chat room with IDs only
- Voice input helper with browser-support fallback
- Microphone permission and device check before voice input
- Help/report with a clear emergency-service boundary

## Notes

- The GitHub source primarily contained elder-user flows
- The worker-side folder is separated so later welfare/staff work can be edited independently
- No backend, login, database, real matching, GPS, or notification system
- No medical diagnosis, medication management, emergency dispatch, or real welfare case management
- No real-name, exact address, phone number, or detailed health-information exposure
