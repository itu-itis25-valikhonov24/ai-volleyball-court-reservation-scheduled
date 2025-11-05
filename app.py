import os
import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

# --- 1. Configuration ---
# Set your API key as an environment variable
# In your terminal: export GOOGLE_API_KEY="your_gemini_api_key_here"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the Flask app
app = Flask(__name__)

# --- 2. Define the AI's "Brain" ---
# This prompt is the most important part. It tells the AI its personality and goals.
GEMINI_PROMPT = """
You are "Halı", an AI assistant calling a university sports facility to reserve a volleyball court.
You MUST speak only fluent, polite, and natural Turkish.

YOUR GOAL:
Reserve a volleyball court for Sunday.

YOUR RULES:
1.  **Preferred Time:** First, ask for Sunday from 7:00 PM (19:00) to 8:30 PM (20:30).
2.  **Backup Plan:** If 7:00 PM is taken, ask for any other 1.5-hour (90-minute) slot
    that starts after 5:00 PM (17:00) but ends no later than 9:00 PM (21:00).
3.  **Conversation Flow:**
    * Start by politely introducing yourself and stating your purpose (e.g., "Merhaba, Pazar günü için voleybol sahası rezervasyonu yapmak istiyorum.").
    * Be conversational. Respond to questions naturally.
4.  **Keep Track:** You must understand the conversation history.

CONVERSATION HISTORY:
{history}

HUMAN SAID:
{human_input}

YOUR RESPONSE (in Turkish):
"""

# Initialize the Gemini model
ai_model = genai.GenerativeModel('gemini-1.5-pro-latest')

# This list will store the conversation history for the AI
conversation_history = []


# --- 3. The Main Webhook Endpoint ---
# This is the URL that Twilio will contact
@app.route("/handle-call", methods=['GET', 'POST'])
def handle_call():
    """Handles the back-and-forth conversation with Twilio."""
    
    response = VoiceResponse()
    
    # Get the text from the human's speech (transcribed by Twilio)
    human_input = request.values.get('SpeechResult', None)
    
    # Add the human's input to our history
    if human_input:
        conversation_history.append(f"HUMAN: {human_input}")
    
    # --- Get the AI's response ---
    # Format the prompt with the latest history and input
    prompt = GEMINI_PROMPT.format(
        history="\n".join(conversation_history),
        human_input=human_input if human_input else "No input, this is the start of the call."
    )
    
    # Call the Gemini API
    try:
        ai_text_response = ai_model.generate_content(prompt).text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        ai_text_response = "Özür dilerim, bir hata oluştu. Lütfen daha sonra tekrar deneyin."

    # Add the AI's response to our history
    conversation_history.append(f"AI: {ai_text_response}")

    # --- Tell Twilio what to do next ---
    # Use <Gather> to speak the AI's response and then immediately
    # listen for the human's next reply.
    gather = Gather(
        input='speech',          # We're expecting speech
        speech_timeout='auto',   # Let Twilio decide when the person stops talking
        language='tr-TR',        # Transcribe Turkish speech
        action='/handle-call'    # Send the transcribed text back to this same URL
    )
    
    # Speak the AI's response in a Turkish voice
    gather.say(ai_text_response, language='tr-TR', voice='Polly.Filiz')
    
    # Add this <Gather> instruction to our main response
    response.append(gather)
    
    # If the AI hangs up (e.g., says "Teşekkürler, hoşçakalın"), 
    # we could add logic here to <Hangup/>.
    # For now, it will just keep listening.
    
    return str(response)


# --- 4. The Entry Point for the Call ---
@app.route("/start-call", methods=['GET', 'POST'])
def start_call():
    """
    This is the first thing Twilio runs when the call connects.
    It immediately redirects to /handle-call to start the conversation.
    """
    # Clear the history for this new call
    conversation_history.clear()
    
    response = VoiceResponse()
    # Redirect to our main conversation handler to get the AI's first line
    response.redirect('/handle-call', method='POST')
    return str(response)

# --- 5. Run the Server ---
if __name__ == "__main__":
    # This makes the server run on port 5000.
    # We will expose this port to the internet using ngrok.
    app.run(port=5000, debug=True)
