import os
import schedule
import time
from twilio.rest import Client

# --- 1. Configuration ---
# Get your Twilio credentials from environment variables
# In your terminal:
# export TWILIO_ACCOUNT_SID="your_twilio_sid_here"
# export TWILIO_AUTH_TOKEN="your_twilio_token_here"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Your Twilio phone number (the one you bought)
TWILIO_PHONE_NUMBER = "+1234567890"  # <-- !! REPLACE with your Twilio number

# The university's number you want to call
UNIVERSITY_PHONE_NUMBER = "+905551234567"  # <-- !! REPLACE with the number to be called

# --- IMPORTANT: This URL must be a PUBLIC internet address ---
# We will get this from 'ngrok' in the next step.
# This URL tells Twilio where to find your running Flask server.
YOUR_SERVER_URL = "https://your-unique-ngrok-url.ngrok-free.app"  # <-- !! REPLACE THIS

def make_reservation_call():
    """
    Uses the Twilio API to initiate the phone call.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        print(f"[{time.ctime()}] It's 9 AM on Monday. Initiating call to {UNIVERSITY_PHONE_NUMBER}...")
        
        call = client.calls.create(
            to=UNIVERSITY_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            # This is the crucial part:
            # It tells Twilio, "When the call connects,
            # contact this URL to get your instructions."
            url=f"{YOUR_SERVER_URL}/start-call"
        )
        
        print(f"Call initiated successfully. SID: {call.sid}")

    except Exception as e:
        print(f"[{time.ctime()}] Error making call: {e}")

# --- 3. The Scheduler ---
def main():
    """
    Sets up the schedule and keeps the script running.
    """
    print("Reservation Bot Scheduler started.")
    print(f"Will call {UNIVERSITY_PHONE_NUMBER} every Monday at 09:00.")
    print("Press Ctrl+C to stop.")

    # Run the job every Monday at 9:00 AM
    schedule.every().monday.at("09:00").do(make_reservation_call)
    
    # --- For Testing: Run it now ---
    # print("--- TEST MODE: Calling now instead of scheduling. ---")
    # make_reservation_call()
    # -------------------------------

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
