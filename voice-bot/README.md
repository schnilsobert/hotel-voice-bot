# hotel-voice-bot
Hotel service bot to greet people and make life easier for hotel staff

# Voice Bot - Hotel Support

Ein Voice-Bot für automatisierte Telefonannahme in Hotels.

## Features (Phase 1)

- Automatische Anrufannahme
- DTMF-Menüführung
- Öffnungszeiten ansagen
- Check-in/Check-out Infos
- Weiterleitung zu Mitarbeitern

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with Twilio credentials
uvicorn main:app --reload
```

## Test

1. Start ngrok: `ngrok http 8000`
2. Configure Twilio webhook
3. Call your number