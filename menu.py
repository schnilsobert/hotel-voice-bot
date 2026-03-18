from twilio.twiml.voice_response import VoiceResponse, Gather, Record
from datetime import datetime
import pytz
import responses
import os
from dotenv import load_dotenv

load_dotenv()

def is_business_hours() -> bool:
    """Check if current time is within business hours"""
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz)
    weekday = now.weekday()  # 0=Montag, 6=Sonntag
    hour = now.hour + now.minute/60

    mon_fri_start = float(os.getenv("BUSINESS_HOURS_MON_FRI_START", 7))
    mon_fri_end = float(os.getenv("BUSINESS_HOURS_MON_FRI_END", 17))
    sat_start = float(os.getenv("BUSINESS_HOURS_SAT_START", 8))
    sat_end = float(os.getenv("BUSINESS_HOURS_SAT_END", 12))

    if weekday <= 4:
        return mon_fri_start <= hour < mon_fri_end
    elif weekday == 5:
        return sat_start <= hour < sat_end
    else:
        return False

def handle_menu_selection(digit: str) -> VoiceResponse:
    response = VoiceResponse()
    
    if digit == "1":
        response.say(responses.OPENING_HOURS, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
        response.redirect("/voice")
        
    elif digit == "2":
        response.say(responses.CALLBACK_MESSAGE, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
        response.record(
            max_length=60,
            action="/handle-recording",
            method="POST",
            finish_on_key="#",
            timeout=20
        )
        
    elif digit == "3":
        response.say(responses.VOICEMAIL_MESSAGE, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
        response.record(
            max_length=180,
            action="/handle-recording",
            method="POST",
            finish_on_key="#",
            timeout=10
        )
        
    elif digit == "9":
        if is_business_hours():
            response.say(responses.FORWARD_MESSAGE, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
            response.dial(os.getenv("FORWARD_NUMBER"))
        else:
            response.say(responses.CLOSED_FORWARD, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
            response.redirect("/voice")
        
    else:
        response.say(responses.INVALID_INPUT, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
        response.redirect("/voice")
    
    return response

def create_main_menu() -> VoiceResponse:
    response = VoiceResponse()
    
    gather = Gather(
        num_digits=1,
        action="/handle-key",
        method="POST",
        timeout=5
    )
    
    if is_business_hours():
        gather.say(responses.WELCOME, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
    else:
        gather.say(responses.WELCOME_CLOSED, language="de-DE", voice="Google.de-DE-Neural2-B", ssml=True)
    
    response.append(gather)
    response.redirect("/voice")
    return response