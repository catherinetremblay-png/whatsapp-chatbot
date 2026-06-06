import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

CUSTOMGPT_API_KEY = os.environ.get("CUSTOMGPT_API_KEY")
CUSTOMGPT_AGENT_ID = os.environ.get("CUSTOMGPT_AGENT_ID")

@app.route("/webhook", methods=["POST"])
def webhook():
    question = request.form.get("Body", "")

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
    msg_url = f"https://app.customgpt.ai/api/v1/projects/{CUSTOMGPT_AGENT_ID}/conversations/{session_id}/messages"
    msg_r = requests.post(msg_url, headers=headers, json={"prompt": question})
    msg_data = msg_r.json()
    answer = str(msg_data)

    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
