import os
import requests
import sys

# Dòng này để ép GitHub in chữ ra ngay lập tức
print(">>> BAT DAU KIEM TRA BOT <<<", flush=True)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f">>> TOKEN: {'Da nhan' if TOKEN else 'TRONG'}", flush=True)
print(f">>> CHAT_ID: {CHAT_ID}", flush=True)

def test_send():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": "Test tu GitHub Actions!"})
        print(f">>> KET QUA TELEGRAM: {r.text}", flush=True)
    except Exception as e:
        print(f">>> LOI HE THONG: {e}", flush=True)

if __name__ == "__main__":
    test_send()
    print(">>> KET THUC KIEM TRA <<<", flush=True)
