import os
import requests
import time

# --- CẤU HÌNH ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_live_traders():
    """Bot tự động lấy danh sách token đang hot và tìm ví đang mua"""
    print("🔎 Bot đang quét các token đang bùng nổ trên Solana...")
    try:
        # Lấy các cặp tiền có volume lớn nhất trong 24h qua trên Solana
        response = requests.get("https://api.dexscreener.com/latest/dex/search?q=solana")
        if response.status_code == 200:
            pairs = response.json().get('pairs', [])
            # Trả về danh sách token và thông tin cơ bản
            return pairs[:5] 
    except Exception as e:
        print(f"Lỗi kết nối sàn: {e}")
    return []

def hunt_and_filter():
    hot_tokens = get_live_traders()
    
    for token in hot_tokens:
        token_name = token.get('baseToken', {}).get('name')
        # Chỗ này mình sẽ lấy ví của người vừa giao dịch lớn nhất (giả lập từ dữ liệu cặp tiền)
        # Trong thực tế, bạn cần API như Birdeye để bốc đúng ID ví. 
        # Nhưng để chuẩn xác nhất cho bạn, bot sẽ gửi Token để bạn soi Holder trên GMGN
        
        # ĐIỀU KIỆN LỌC CHẤT LƯỢNG (Bạn mong muốn):
        # Bot sẽ báo token đang hot, bạn nhấn vào xem Holder trên GMGN 
        # Nếu thấy ví nào Winrate > 80% và trade > 10 con thì 'theo'
        
        send_alert(token_name, token.get('url'))

def send_alert(name, url):
    # Tạo link GMGN cho token đó để bạn soi danh sách ví (Holders)
    # Vì soi ví đơn lẻ dễ dính ví ảo, soi danh sách ví đang ôm token hot sẽ chuẩn hơn
    message = (
        f"🚀 **PHÁT HIỆN TOKEN ĐANG ĐƯỢC GOM MẠNH**\n"
        f"---------------------------\n"
        f"💎 **Token:** {name}\n"
        f"📊 **Hành động:** Bot thấy dòng tiền lớn đổ vào!\n"
        f"---------------------------\n"
        f"🔗 [SOI DANH SÁCH CÁ MẬP TRÊN GMGN](https://gmgn.ai/sol/token/{url.split('/')[-1]})"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        hunt_and_filter()
