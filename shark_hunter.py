import os
import requests

def main():
    print("--- ĐANG KIỂM TRA KẾT NỐI ---")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print(f"Token (4 ký tự đầu): {token[:4] if token else 'Trống'}")
    print(f"Chat ID: {chat_id}")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": "🔔 Test từ GitHub!"}
    
    try:
        r = requests.post(url, json=data)
        print(f"Kết quả gửi tin: {r.text}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
