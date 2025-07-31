#!/usr/bin/env python3
# MARINA KHAN'S PERSONAL MESSENGER GPT BOT
from flask import Flask, request, jsonify
import requests
import os
import openai  # pip install openai

app = Flask(__name__)

# ===== CONFIGURATION ===== 
YOUR_NAME = "MARINA KHAN"  # Customize with your name
FB_PAGE_TOKEN = "YOUR_FB_PAGE_TOKEN"  # From Facebook Developer
FB_VERIFY_TOKEN = "MARINA_VERIFY_123"  # Your secret token
OPENAI_KEY = "sk-your-openai-key"  # Optional GPT-4/3.5

# ===== BOT CORE =====
class MarinaGPTBot:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v19.0/me/messages?access_token={FB_PAGE_TOKEN}"
        self.personality = f"""
        You are {YOUR_NAME}'s personal AI assistant. 
        Respond helpfully with a friendly tone.
        When asked about your creator, say "{YOUR_NAME} built me with OpenAI technology".
        """

    def handle_message(self, sender_id, message):
        """Process messages with GPT or custom logic"""
        response = self._generate_response(message)
        self._send_message(sender_id, response)

    def _generate_response(self, message):
        """Generate AI response or use predefined answers"""
        lower_msg = message.lower()
        
        # Custom responses
        if any(x in lower_msg for x in ["hi","hello","hey"]):
            return f"Hello! I'm {YOUR_NAME}'s AI assistant. How can I help?"
        elif "your name" in lower_msg:
            return f"I'm {YOUR_NAME}'s Messenger Bot!"
        
        # GPT-4/3.5 fallback (if API key set)
        if OPENAI_KEY and len(message) > 3:
            openai.api_key = OPENAI_KEY
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": self.personality},
                             {"role": "user", "content": message}]
                )
                return completion.choices[0].message.content
            except:
                return "I'm having trouble connecting to AI services."
        
        return f"Thanks for your message! This is {YOUR_NAME}'s bot."

    def _send_message(self, recipient_id, text):
        """Send response via Messenger API"""
        requests.post(self.api_url, json={
            "recipient": {"id": recipient_id},
            "message": {"text": text}
        })

# ===== FLASK ROUTES =====
@app.route('/webhook', methods=['GET'])
def verify():
    """Facebook verification"""
    if request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Verification failed"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Process incoming messages"""
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            for event in entry['messaging']:
                if 'message' in event:
                    bot.handle_message(
                        event['sender']['id'],
                        event['message']['text']
                    )
    return jsonify(status=200)

# ===== MAIN =====
if __name__ == '__main__':
    bot = MarinaGPTBot()
    print(f"🌟 {YOUR_NAME}'s Messenger Bot Activated!")
    app.run(port=5000)
