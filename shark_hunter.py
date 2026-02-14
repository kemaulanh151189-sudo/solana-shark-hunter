import os
import requests
import time
from datetime import datetime

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

def get_live_traders():
    """Sử dụng API Helius để lấy các giao dịch thực tế trên Solana"""
    if not HELIUS_KEY:
        print("ple helppp meee! Bạn quên cài HELIUS_API_KEY trong Secrets rồi!")
        return []

    # Địa chỉ Raydium Authority để bắt các lệnh Swap mới nhất
    url = f"https://api.helius.xyz/v0/addresses/6EF8rrecthR5DkZJvyu7VpP6S06m7431/transactions?api-key={HELIUS_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            txs = response.json()
            found_wallets = []
            
            for tx in txs[:8]: # Lấy 8 giao dịch mới nhất để lọc
                description = tx.get('description', '')
                if description:
                    # Bốc tách ví từ mô tả giao dịch của Helius
                    parts = description.split(' ')
                    wallet = parts[0]
                    # Chỉ lấy địa chỉ ví hợp lệ (độ dài Solana chuẩn)
                    if len(wallet) >= 32 and wallet not in found_wallets:
                        found_wallets.append(wallet)
            return found_wallets
    except Exception as e:
        print(f"❌ Lỗi kết nối API: {e}")
    return []

def send_heartbeat():
    """Gửi thông báo định kỳ để bạn biết bot vẫn đang sống"""
    # Chỉ gửi thông báo 'Sống' vào phút thứ 0 của mỗi giờ để tiết kiệm credit
    now = datetime.now()
    if now.minute < 2: # Vì bot chạy mỗi 2 phút, nên check khoảng này
        msg = f"🟢 **SYSTEM STATUS: ACTIVE**\n🕒 Time: `{now.strftime('%H:%M')}`\n📡 Scanner is working properly."
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        except:
            pass

def hunt():
    print("🚀 Bot đang bắt đầu ca trực săn cá mập...")
    
    # Gửi tin nhắn xác nhận hệ thống online (Heartbeat)
    send_heartbeat()
    
    wallets = get_live_traders()
    
    if not wallets:
        print("📭 Chưa tìm thấy giao dịch nào mới, đợi nhịp sau nhé!")
        return

    for addr in wallets:
        # Gửi thông tin về Telegram
        send_to_telegram(addr)
        # Nghỉ 1s giữa các lần gửi để tránh bị Telegram chặn (Spam)
        time.sleep(1)

def send_to_telegram(wallet):
    gmgn_link = f"https://gmgn.ai/sol/address/{wallet}"
    
    # Đổi tiêu đề cho chuyên nghiệp hơn
    message = (
        f"🔍 **STRATEGY: ELITE TRADER DETECTED**\n"
        f"----------------------------------\n"
        f"👤 **Address:** `{wallet}`\n"
        f"📈 **Activity:** High-Frequency Swap\n"
        f"----------------------------------\n"
        f"🚀 [ANALYZE ON GMGN.AI]({gmgn_link})"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except:
        pass

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        hunt()
    else:
        print("ple helppp meee! Check lại cấu hình Token/ChatID!")
