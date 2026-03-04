# Voice Bot - Automatische Telefonzentrale

Ein Voice-Bot für automatisierte Telefonannahme für kleine und mittlere Betriebe.

## Features (Phase 1)

- Automatische Anrufannahme
- DTMF-Menüführung
- Öffnungszeiten ansagen
- Rückrufbitte aufnehmen
- Voicemail aufnehmen
- Weiterleitung zu Mitarbeitern

## Tech Stack

- Python 3.10+
- FastAPI
- Twilio Voice API
- ngrok (Development)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Roadmap

- [x] Phase 1: Basic DTMF menu
- [ ] Phase 2: Speech recognition
- [ ] Phase 3: AI-powered responses