
import re
from typing import Literal

Intent = Literal["PAY_NOW", "PAY_LATER", "NOT_INTERESTED", "CHOOSE_POLICY", "OTHER"]

def detect_intent(user_text: str) -> Intent:
    t = user_text.lower().strip()
    if any(k in t for k in ["pay now", "payment now", "proceed", "yes pay"]):
        return "PAY_NOW"
    if any(k in t for k in ["later", "not now", "remind", "tomorrow", "next", "evening", "morning"]):
        return "PAY_LATER"
    if any(k in t for k in ["not interested", "stop", "no thanks", "dont call"]):
        return "NOT_INTERESTED"
    if t == "okay" or t == "ok":
        return "OKAY"
    if re.findall(r"pol\d{5}", t):
        return "CHOOSE_POLICY"
    return "OTHER"

def extract_time(user_text: str) -> str:
    from datetime import datetime, timedelta
    now = datetime.now()
    if "tomorrow" in user_text.lower():
        day = now + timedelta(days=1)
    else:
        day = now + timedelta(days=2)
    hour = 18 if "evening" in user_text.lower() else 10
    dt = day.replace(hour=hour, minute=0, second=0, microsecond=0)
    return dt.isoformat()


