import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

@app.route('/')
def home():
    return "MNP Bot Chalu Hai!"

@app.route('/sms', methods=['POST'])
def receive_sms():
    data = request.json or {}
    sender = str(data.get("sender", ""))
    message = str(data.get("message", ""))

    # Filter: Sirf 'AIRDRT' sender ya 'FTA MNP' wale msg hi aage bhejega
    if "AIRDRT" in sender.upper() or "FTA MNP" in message:
        url = f"https://telegram.org{TOKEN}/sendMessage"
        payload = {
            "chat_id": GROUP_CHAT_ID,
            "text": message  # Bina kisi badlav ke as-it-is bhejega
        }
        requests.post(url, json=payload)
        return {"status": "forwarded"}, 200

    return {"status": "ignored"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
