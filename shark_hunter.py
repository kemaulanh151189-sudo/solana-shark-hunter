import requests

# Tạm thời để trống các biến này, bước sau mình sẽ điền
TOKEN = "DIEN_TOKEN_BOT_CUA_BAN"
CHAT_ID = "DIEN_ID_CHAT_CUA_BAN"

def scan_solana():
    # Quét danh sách token hot nhất để tìm ví xịn
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    try:
        data = requests.get(url).json()
        pairs = data.get('pairs', [])[:5]
        
        for pair in pairs:
            name = pair['baseToken']['name']
            # Thông báo giả lập để kiểm tra xem hệ thống chạy chưa
            msg = f"🛰️ Hệ thống đang soi token: {name}\nĐang lùng sục cá mập..."
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
            break # Thử nghiệm 1 con duy nhất
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    scan_solana()
