import os
import requests
import threading
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

CUSTOMGPT_API_KEY = "10365|blOnzLmWa4jsaEuMAUErGLtlX7deYmcCjSQrnKfY0f3bfa02"
CUSTOMGPT_AGENT_ID = "86582"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

def get_and_send_response(question, to_number, from_number):
    headers = {
        "Authorization": f"Bearer {CUSTOMGPT_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Étape 1 : créer une conversation
    conv_url = f"https://app.customgpt.ai/api/v1/projects/{CUSTOMGPT_AGENT_ID}/conversations"
    conv_r = requests.post(conv_url, headers=headers, json={"name": "whatsapp"})
    conv_data = conv_r.json()
    session_id = conv_data.get("data", {}).get("session_id", "")

    # Étape 2 : envoyer le message
    msg_url = f"https://app.customgpt.ai/api/v1/projects/{CUSTOMGPT_AGENT_ID}/conversations/{session_id}/messages?stream=false"
    msg_r = requests.post(msg_url, headers=headers, json={"prompt": question}, timeout=60)
    msg_data = msg_r.json()
    answer = msg_data.get("data", {}).get("openai_response", str(msg_data))

    # Envoyer la réponse via Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=answer,
        from_=from_number,
        to=to_number
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    question = request.form.get("Body", "")
    to_number = request.form.get("From", "")
    from_number = request.form.get("To", "")

    # Répondre immédiatement à Twilio
    thread = threading.Thread(
        target=get_and_send_response,
        args=(question, to_number, from_number)
    )
    thread.start()

    resp = MessagingResponse()
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
