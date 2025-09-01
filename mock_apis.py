
import random
from datetime import datetime

def initiate_payment(customerId: str, policyNumber: str, amount: float):
    payment_id = str(random.randint(10000, 99999))
    return {"paymentId": payment_id, "paymentLink": f"https://pay.link/{payment_id}"}

def confirm_payment(paymentId: str, policyNumber: str):
    status = "SUCCESS" if random.random() > 0.2 else "FAILED"
    return {"status": status}

def update_policy(customerId: str, policyNumber: str, paymentStatus: str):
    return {"status": "Updated"}

def send_email(to: str, subject: str, body: str, attachment: str):
    return {"status": "Sent"}

def schedule_callback(customerId: str, policyNumber: str, time_iso: str):
    try:
        datetime.fromisoformat(time_iso.replace("Z",""))
        return {"status": "Scheduled"}
    except Exception:
        return {"status": "Invalid Time"}
