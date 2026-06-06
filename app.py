import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

CUSTOMGPT_API_KEY = os.environ.get("CUSTOMGPT_API_KEY")
CUSTOMGPT_AGENT_ID = "86582"

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
    
    # Retourner la réponse brute de l'étape 1 pour déboguer
    resp = MessagingResponse()
    resp.message(str(conv_data))
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
