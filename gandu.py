import pywhatkit as kit
import time
from datetime import datetime, timedelta

def send_message(phone_no, message):
    now = datetime.now()
    send_time = now + timedelta(seconds=10)  # Schedule to send 10 seconds from now
    hour = send_time.hour
    minute = send_time.minute
    second = send_time.second
    
    kit.sendwhatmsg(phone_no, message, hour, minute, second)

if __name__ == "__main__":
    phone_no = "+919902257755"  # Replace with the recipient's phone number
    message = "FUCKER call me immediately madher chodh."
    
    while True:
        send_message(phone_no, message)
        # No sleep, send the next message immediately
