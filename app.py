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
        "Content-Type": "application/json"
    }
    payload = {
        "response_source": "default",
        "query": question
    }
    url = f"https://app.customgpt.ai/api/v1/projects/{CUSTOMGPT_AGENT_ID}/conversations"
    
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    answer = data.get("data", {}).get("openai_response", "Je n'ai pas pu trouver une réponse.")
    
    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
