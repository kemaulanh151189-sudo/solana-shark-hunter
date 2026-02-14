import requests
import os

# Lấy thông tin từ két sắt GitHub Secrets bạn vừa tạo
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def scan_solana():
    # Kiểm tra xem đã có chìa khóa chưa
    if not TOKEN or not CHAT_ID:
        print("❌ Lỗi: Chưa tìm thấy TOKEN hoặc CHAT_ID trong Secrets!")
        return

    # Quét top 5 token đang hot nhất trên Solana từ DexScreener
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    try:
        response = requests.get(url)
        data = response.json()
        pairs = data.get('pairs', [])[:5]
        
        for pair in pairs:
            name = pair['baseToken']['name']
            price = pair.get('priceUsd', 'N/A')
            volume = pair.get('volume', {}).get('h24', 0)
            
            # Nội dung tin nhắn gửi về Telegram
            msg = (
                f"🛰️ **Hệ thống đang soi:** {name}\n"
                f"💰 Giá: ${price}\n"
                f"📊 Volume 24h: ${volume:,.0f}\n"
                f"👉 Đang quét tìm các ví thắng đậm..."
            )
            
            # Gửi tin nhắn qua Telegram
            tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            params = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
            requests.get(tele_url, params=params)
            break # Chỉ báo thử 1 con để kiểm tra kết nối
            
    except Exception as e:
        print(f"Lỗi rồi bạn ơi: {e}")

if __name__ == "__main__":
    scan_solana()
