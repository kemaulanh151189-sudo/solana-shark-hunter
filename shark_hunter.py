import os
import requests
import sys

def force_print(message):
    print(message)
    sys.stdout.flush()

force_print("🚀 CHUONG TRINH BAT DAU...")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

force_print(f"🔹 Token: {'Da nhan' if TOKEN else 'TRONG'}")
force_print(f"🔹 Chat ID: {CHAT_ID}")

try:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": CHAT_ID, "text": "Kiem tra log tu GitHub!"})
    force_print(f"🔹 Ket qua tu Telegram: {res.text}")
except Exception as e:
    force_print(f"❌ LOI: {str(e)}")

force_print("🏁 KET THUC.")
