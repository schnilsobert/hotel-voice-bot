from twilio.twiml.voice_response import VoiceResponse, Gather, Record
import responses
import os
from dotenv import load_dotenv

load_dotenv()

def handle_menu_selection(digit: str) -> VoiceResponse:
    """Handle DTMF input and return appropriate response"""
    response = VoiceResponse()
    
    if digit == "1":
        response.say(responses.OPENING_HOURS, language="de-DE")
        response.redirect("/voice")
        
    elif digit == "2":
        response.say(responses.CALLBACK_MESSAGE, language="de-DE")
        response.record(
            max_length=30,
            action="/handle-recording",
            method="POST",
            finish_on_key="#"
        )
        
    elif digit == "3":
        response.say(responses.VOICEMAIL_MESSAGE, language="de-DE")
        response.record(
            max_length=120,
            action="/handle-recording",
            method="POST",
            finish_on_key="#"
        )
        
    elif digit == "9":
        response.say(responses.FORWARD_MESSAGE, language="de-DE")
        response.dial(os.getenv("FORWARD_NUMBER"))
        
    else:
        response.say(responses.INVALID_INPUT, language="de-DE")
        response.redirect("/voice")
    
    return response

def create_main_menu() -> VoiceResponse:
    """Create the main menu with DTMF gathering"""
    response = VoiceResponse()
    
    gather = Gather(
        num_digits=1,
        action="/handle-key",
        method="POST",
        timeout=5
    )
    
    gather.say(responses.WELCOME, language="de-DE")
    response.append(gather)
    
    response.redirect("/voice")
    
    return response