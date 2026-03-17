from flask import Flask, request, jsonify
import requests
import json
import logging
from datetime import datetime

TELEGRAM_TOKEN = "8662538546:AAHb2Zmh7n2SZewupF1YhXBH33hgJq3-ZoI"
TELEGRAM_CHAT_ID = "1466991936"
WEBHOOK_SECRET = "goldxauusd2026"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)

def format_signal(data):
    signal = data.get("signal","?")
    price = data.get("price","?")
    entry = data.get("entry","?")
    target = data.get("target","?")
    stop = data.get("stop","?")
    conf = data.get("confidence","?")
    rsi = data.get("rsi","?")
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    emoji = "🟢 KAUFEN 📈" if signal == "KAUFEN" else "🔴 VERKAUFEN 📉"
    return (f"<b>⚡ XAUUSD GOLD SIGNAL</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{emoji}\n\n"
            f"💰 <b>Preis:</b> {price}\n"
            f"🎯 <b>Einstieg:</b> {entry}\n"
            f"✅ <b>Ziel:</b> {target}\n"
            f"🛑 <b>Stop:</b> {stop}\n\n"
            f"📊 <b>Konfidenz:</b> {conf}%\n"
            f"📉 <b>RSI:</b> {rsi}\n\n"
            f"🕐 {now}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<i>⚠️ Kein Finanzberatung</i>")

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    data = json.loads(request.get_data(as_text=True))
    send_telegram(format_signal(data))
    return jsonify({"status": "ok"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200

if __name__ == "__main__":
    send_telegram("🚀 <b>Gold Signal Bot gestartet!</b>\n✅ Server aktiv\n✅ Telegram verbunden")
    app.run(host="0.0.0.0", port=5000)
