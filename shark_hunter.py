import os
import requests
import time
from datetime import datetime

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

def get_live_traders():
    """Quét Blockchain Solana qua API Helius"""
    if not HELIUS_KEY:
        print("ple helppp meee! Check lại API Key trong Secrets!")
        return []

    # Raydium Authority: 6EF8rrecthR5DkZJvyu7VpP6S06m7431
    url = f"https://api.helius.xyz/v0/addresses/6EF8rrecthR5DkZJvyu7VpP6S06m7431/transactions?api-key={HELIUS_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            txs = response.json()
            found_wallets = []
            for tx in txs[:10]:
                description = tx.get('description', '')
                if description:
                    wallet = description.split(' ')[0]
                    if len(wallet) >= 32 and wallet not in found_wallets:
                        found_wallets.append(wallet)
            return found_wallets
    except Exception as e:
        print(f"❌ API Error: {e}")
    return []

def send_heartbeat():
    """Báo cáo hệ thống vẫn sống vào đầu mỗi giờ"""
    now = datetime.now()
    if now.minute < 2:
        msg = "🟢 **SYSTEM STATUS: ACTIVE**\n📡 Scanner is hunting for Whales..."
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def send_to_telegram(wallet):
    """Phân cấp tin nhắn theo 3 tầng lớp thợ săn"""
    gmgn_link = f"https://gmgn.ai/sol/address/{wallet}"
    
    # Header dựa trên tuổi đời bạn soi trên GMGN
    # 🌟 LEGENDARY (>6 tháng) | 📈 ELITE (1-6 tháng) | 🌱 NEWBIE PRO (1 tuần-1 tháng)
    
    header = "🔍 **STRATEGY: MULTI-LEVEL FILTER**"
    footer = f"🚀 [VERIFY ON GMGN.AI]({gmgn_link})"
    
    body = (
        f"👤 **Address:** `{wallet}`\n"
        f"----------------------------------\n"
        f"📊 **CHECKLIST THỰC CHIẾN:**\n"
        f"🎯 **Winrate 30D:** > 80% (8/10 Token khác nhau)\n"
        f"📈 **ROI Trung Bình:** > 200% (Bất chấp rút vốn)\n"
        f"🔥 **Status:** Hoạt động trong 7 ngày qua\n"
        f"----------------------------------\n"
        f"💡 *Gợi ý phân cấp:* \n"
        f"🥇 > 6 Tháng: **Huyền thoại**\n"
        f"🥈 1-6 Tháng: **Cao thủ**\n"
        f"🥉 < 1 Tháng: **Tân binh Pro**"
    )

    full_message = f"{header}\n\n{body}\n\n{footer}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": full_message, "parse_mode": "Markdown"})
    except:
        pass

def hunt():
    print("🚀 Bot đang bắt đầu ca trực săn cá mập...")
    send_heartbeat()
    wallets = get_live_traders()
    
    if not wallets:
        print("📭 Chưa tìm thấy giao dịch mới...")
        return

    for addr in wallets:
        send_to_telegram(addr)
        time.sleep(1.5) # Nghỉ để tránh Telegram rate limit

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        hunt()
    else:
        print("ple helppp meee! Thiếu cấu hình Telegram!")
