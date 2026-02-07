from fastapi import FastAPI, Form, Request
from fastapi.responses import Response
import menu
import logging
from datetime import datetime

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### `.env.example`
```
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+49123456789
FORWARD_NUMBER=+49987654321