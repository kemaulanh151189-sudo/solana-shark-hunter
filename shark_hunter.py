import os
import requests

# --- CẤU HÌNH (Lấy từ GitHub Secrets) ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

def get_live_sharks():
    """Bot dùng API Helius để quét ví thật đang giao dịch"""
    if not HELIUS_KEY:
        print("ple helppp meee! Bạn quên chưa dán API Key vào GitHub Secrets rồi!")
        return []
    
    print("🔎 Bot đang 'ngửi' mùi cá mập trên Raydium...")
    # Quét các giao dịch mới nhất trên sàn Raydium
    url = f"https://api.helius.xyz/v0/addresses/6EF8rrecthR5DkZJvyu7VpP6S06m7431/transactions?api-key={HELIUS_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            txs = response.json()
            wallets = []
            for tx in txs[:10]: # Quét 10 giao dịch gần nhất
                # Bóc tách địa chỉ ví (người thực hiện lệnh)
                description = tx.get('description', '')
                if description:
                    parts = description.split(' ')
                    wallet = parts[0]
                    # Kiểm tra định dạng ví Solana (thường dài 43-44 ký tự)
                    if len(wallet) >= 32:
                        wallets.append(wallet)
            return list(set(wallets)) # Loại bỏ ví trùng lặp
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
    return []

def hunt():
    live_wallets = get_live_sharks()
    
    for addr in live_wallets:
        # Gửi báo động về Telegram kèm link soi cao thủ
        send_to_telegram(addr)

def send_to_telegram(wallet):
    # Link GMGN chuẩn 100% để bạn soi Winrate và PnL thực tế
    gmgn_link = f"https://gmgn.ai/sol/address/{wallet}"
    
    message = (
        f"🚨 **PHÁT HIỆN CAO THỦ THỰC CHIẾN** 🚨\n"
        f"---------------------------\n"
        f"👤 **Ví vừa mua:** `{wallet}`\n"
        f"📊 **Hành động:** Hệ thống phát hiện giao dịch On-chain!\n"
        f"---------------------------\n"
        f"🚀 [SOI WINRATE TRÊN GMGN.AI]({gmgn_link})"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        hunt()
    else:
        print("ple helppp meee! Kiểm tra lại Token Bot nhé!")
