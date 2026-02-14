import os
import requests

# Ép in ra màn hình để kiểm tra bảng đen
print("🚀 HỆ THỐNG BẮT ĐẦU CHẠY...")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"Kiểm tra Token: {'Đã nhận' if TOKEN else 'TRỐNG'}")
print(f"Kiểm tra ID: {CHAT_ID}")

def send_test():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "🔔 THÔNG BÁO: Bot đã kết nối được với GitHub Actions!"}
    
    try:
        r = requests.post(url, json=payload)
        print(f"Kết quả từ Telegram: {r.text}")
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

if __name__ == "__main__":
    send_test()
    print("🏁 QUÁ TRÌNH CHẠY KẾT THÚC.")
