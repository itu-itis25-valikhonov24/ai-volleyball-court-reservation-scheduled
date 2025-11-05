# Ai caller which would reserve a court for volleyball by calling on scheduled time to given number

### Prerequisites: Install the Libraries

Open your terminal and install the necessary Python libraries:
```bash
# Flask is our web server
pip install Flask

# Twilio is for the phone call
pip install twilio

# Google's AI library is for Gemini
pip install google-generativeai
Part 1: The Web Server (The "Brain")
```
-----

### How to Run This (Step-by-Step)

You'll need three separate terminal windows.

#### Step 1: Set Your API Keys

First, set your secret keys as environment variables so your code can access them securely.

```bash
# In your terminal (for Mac/Linux)
export GOOGLE_API_KEY="your-gemini-key-goes-here"
export TWILIO_ACCOUNT_SID="your-twilio-sid-goes-here"
export TWILIO_AUTH_TOKEN="your-twilio-token-goes-here"

# For Windows (use 'set' instead of 'export')
set GOOGLE_API_KEY="your-gemini-key-goes-here"
set TWILIO_ACCOUNT_SID="your-twilio-sid-goes-here"
set TWILIO_AUTH_TOKEN="your-twilio-token-goes-here"
```

#### Step 2: Use `ngrok` to Get a Public URL

Your Flask server (`app.py`) runs on your local computer (`localhost:5000`), which Twilio cannot access from the internet. We need a tool called **ngrok** to create a secure, public tunnel to it.

1.  [Download and install ngrok](https://ngrok.com/download).
2.  In **Terminal 1**, run this command:
    ```bash
    ngrok http 5000
    ```
3.  `ngrok` will give you a public URL. It looks something like this:
    `Forwarding https://abcd-1234.ngrok-free.app -> http://localhost:5000`

**Copy that `https://...` URL.** This is your server's public address.

#### Step 3: Run the Flask Server (The "Brain")

1.  Go to `trigger_call.py` and **paste your ngrok URL** into the `YOUR_SERVER_URL` variable.
2.  Now, in **Terminal 2**, run your Flask app:
    ```bash
    python app.py
    ```
    You should see it running. Any time Twilio contacts your server, you'll see activity in this window.

#### Step 4: Run the Scheduler (The "Trigger")

1.  In **Terminal 3**, run your scheduler script:
    ```bash
    python trigger_call.py
    ```
    This script will now sit and wait until 9:00 AM on Monday.

-----

### 🧪 To Test It Immediately

You don't want to wait until Monday\! To test it right now, go to `trigger_call.py` and **un-comment** these two lines inside the `main()` function:
ction:

```bash
# --- For Testing: Run it now ---    
print("--- TEST MODE: Calling now instead of scheduling. ---")    
make_reservation_call()    
# -------------------------------
```

Now, when you run python trigger_call.py (with ngrok and app.py already running), it will make the call immediately. You can pick up the phone and have a conversation with your Gemini bot!
