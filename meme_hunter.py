import os
import requests
import time
from datetime import datetime, timezone

# --- THÔNG SỐ CÁ NHÂN HÓA (PLE HELPPP MEEE!) ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

def get_exclusive_pools():
    """Lọc cực gắt: < 5 phút & bắt được địa chỉ Token (CA)"""
    if not HELIUS_KEY: return []
    url = f"https://api.helius.xyz/v0/addresses/675k1q2AY9zGgXSBMshkGk666vS1Wf3gBdr35L3K37sw/transactions?api-key={HELIUS_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            txs = response.json()
            found_items = []
            now = datetime.now(timezone.utc).timestamp()
            for tx in txs:
                if now - tx.get('timestamp', 0) <= 300: # LỌC 5 PHÚT
                    description = tx.get('description', '')
                    if description and "swapped" in description.lower():
                        # Bóc tách địa chỉ ví và bối cảnh giao dịch
                        wallet = description.split(' ')[0]
                        found_items.append(wallet)
                else: break
            return list(set(found_items))
    except: return []
    return []

def send_ultimate_alert(wallet):
    """Gửi báo cáo săn Meme hoàn chỉnh (ple helppp meee!)"""
    gmgn_wallet = f"https://gmgn.ai/sol/address/{wallet}"
    rugcheck_url = "https://rugcheck.xyz/"
    solanafm_url = f"https://solana.fm/address/{wallet}"

    header = "🚀 **MEME SNIPER V3: EXCLUSIVE FILTER** 🚀"
    
    body = (
        f"👤 **Cá mập/Insider:** `{wallet}`\n"
        f"⏱️ **Độ tươi:** < 5 phút (Vừa 'bắn' lệnh)\n"
        f"----------------------------------\n"
        f"🎯 **TIÊU CHUẨN RIÊNG CỦA BẠN:**\n"
        f"❌ **HOLDERS:** Top 10 PHẢI < 5% (Check GMGN)\n"
        f"🔥 **LP:** Phải Burned & > 5 SOL\n"
        f"🚫 **SCAM:** Tax < 30% | No Freeze | No Mint\n"
        f"⚠️ **DANGER:** Tuyệt đối KHÔNG ký 'Approve Access'\n"
        f"----------------------------------\n"
        f"🕵️ **SOI DEV:** Check ví Deployer xem có 'vết' không!"
        f"----------------------------------\n"
        f"💰 [CHECK DEV WALLET](https://solscan.io/address/{wallet})"
    )

    footer = (
        f"🔍 [SOI HOLDERS & DEV]({gmgn_wallet})\n"
        f"🛡️ [CHECK SCAM/TAX]({rugcheck_url})\n"
        f"🌐 [LỊCH SỬ VÍ (SOLANAFM)]({solanafm_url})\n"
        f"💰 [CHECK DEV WALLET](https://solscan.io/address/{wallet})"
    )
    
    msg = f"{header}\n\n{body}\n\n{footer}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})
    except: 
        pass

    # Nút bấm hành động
    footer = (
        f"🔍 [SOI HOLDERS & DEV]({gmgn_wallet})\n"
        f"🛡️ [CHECK SCAM/TAX]({rugcheck_url})\n"
        f"🌐 [LỊCH SỬ VÍ (SOLANAFM)]({solanafm_url})"
    )
    
    msg = f"{header}\n\n{body}\n\n{footer}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})
    except: pass

if __name__ == "__main__":
    print(f"🔥 [{datetime.now().strftime('%H:%M:%S')}] Đang săn Meme theo tiêu chuẩn riêng...")
    targets = get_exclusive_pools()
    for t in targets:
        send_ultimate_alert(t)
        time.sleep(1.2)
