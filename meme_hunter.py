import os
import requests
import time
from datetime import datetime, timezone

# --- THÔNG SỐ CÁ NHÂN HÓA (PLE HELPPP MEEE!) ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

import requests

def check_security_quality(ca):
    """Não bộ của Bot: Tự check Mint, Freeze, LP Lock và Tax (ple helppp meee!)"""
    try:
        # 1. Check LP và Volume qua DexScreener
        dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{ca}"
        data = requests.get(dex_url).json()
        pair = data.get('pairs', [{}])[0]
        
        lp_sol = pair.get('liquidity', {}).get('quote', 0)
        # BỘ LỌC 1: THANH KHOẢN >= 5 SOL
        if lp_sol < 5: return False 

        # 2. Check bảo mật qua RugCheck (Giả lập gọi API)
        # Pl hepl meee: Đoạn này bot sẽ check No Mint, No Freeze, Tax < 30%
        rug_url = f"https://api.rugcheck.xyz/v1/tokens/{ca}/report"
        report = requests.get(rug_url).json()
        
        # BỘ LỌC 2: KHÔNG ĐƯỢC MINT/FREEZE
        if report.get('mintAuthority') is not None or report.get('freezeAuthority') is not None:
            return False
            
        # BỘ LỌC 3: LP PHẢI KHÓA > 7 NGÀY
        lp_lock_days = report.get('lpLockDays', 0)
        if lp_lock_days < 7: return False
        
        # BỘ LỌC 4: TAX < 30%
        if report.get('sellTax', 0) > 30: return False

        return True
    except:
        return False

def get_exclusive_pools():
    """Bot săn Meme Siêu Tươi < 5p & Đã qua kiểm định (pl hepl meee!)"""
    url = f"https://api.helius.xyz/v0/addresses/675k1q2AY9zGgXSBMshkGk666vS1Wf3gBdr35L3K37sw/transactions?api-key={HELIUS_KEY}"
    try:
        txs = requests.get(url).json()
        found_items = []
        now = datetime.now(timezone.utc).timestamp()
        
        for tx in txs:
            # CHỈ LẤY ĐỘ TƯƠI < 5 PHÚT
            if now - tx.get('timestamp', 0) <= 300:
                description = tx.get('description', '')
                if "swapped" in description.lower():
                    # Tự động bóc tách CA từ description
                    ca = description.split(' ')[-1] 
                    
                    # NẾU VƯỢT QUA TẤT CẢ BỘ LỌC THÌ MỚI BÁO
                    if check_security_quality(ca):
                        found_items.append(ca)
            else: break
        return list(set(found_items))
    except: return []

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
