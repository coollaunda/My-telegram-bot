import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

@app.route('/')
def home():
    return "MNP Bot Chalu Hai!"

# Yeh naya hissa /start ka jawab dene ke liye hai
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json or {}
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text == "/start" and chat_id:
        url = f"https://telegram.org{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": "✅ बॉट 100% चालू है! जैसे ही FTA MNP का SMS आएगा, यह अपने आप ग्रुप में भेज देगा।"
        })
    return {"status": "ok"}, 200

@app.route('/sms', methods=['POST'])
def receive_sms():
    data = request.json or {}
    sender = str(data.get("sender", ""))
    message = str(data.get("message", ""))

    if "AIRDRT" in sender.upper() or "FTA MNP" in message:
        url = f"https://telegram.org{TOKEN}/sendMessage"
        payload = {
            "chat_id": GROUP_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload)
        return {"status": "forwarded"}, 200

    return {"status": "ignored"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
