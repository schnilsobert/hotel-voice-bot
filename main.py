from fastapi import FastAPI, Form, Request
from fastapi.responses import Response
import menu
import os
import logging
from datetime import datetime
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Bot API")

@app.post("/voice")
async def voice_entry(request: Request):
    """Main entry point for incoming calls"""
    logger.info("Incoming call received")
    response = menu.create_main_menu()
    return Response(content=str(response), media_type="application/xml")

@app.post("/handle-key")
async def handle_key(Digits: str = Form(...)):
    """Handle DTMF key press"""
    logger.info(f"Key pressed: {Digits}")
    response = menu.handle_menu_selection(Digits)
    return Response(content=str(response), media_type="application/xml")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/handle-recording")
async def handle_recording(
    RecordingUrl: str = Form(...),
    RecordingSid: str = Form(...),
    CallSid: str = Form(...),
    From: str = Form(...)
):
    logger.info(f"Recording received: {RecordingUrl}")
    
    try:
        # Audio herunterladen
        import requests as req
        from openai import OpenAI
        
        audio_url = RecordingUrl + ".mp3"
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        audio_response = req.get(audio_url, auth=(account_sid, auth_token))
        
        # Transkription mit Whisper
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        with open("recording.mp3", "wb") as f:
            f.write(audio_response.content)
        
        with open("recording.mp3", "rb") as f:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="de"
            )
        
        text = transcript.text
        logger.info(f"Transkription: {text}")
        
    except Exception as e:
        logger.error(f"Transkription fehlgeschlagen: {e}")
        text = "Transkription fehlgeschlagen"
    
    # SMS senden
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=f"Neuer Anruf von {From}:\n\"{text}\"",
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=os.getenv("FORWARD_NUMBER")
    )
    
    response = VoiceResponse()
    response.say(
        "<speak><prosody rate='85%'>Vielen Dank.<break time='300ms'/> Wir melden uns so schnell wie möglich bei Ihnen.<break time='300ms'/> Auf Wiederhören.</prosody></speak>",
        language="de-DE",
        voice="Google.de-DE-Neural2-B",
        ssml=True
    )
    return Response(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)