import os
import requests
import time
from datetime import datetime, timezone

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

def brain_check_performance(wallet):
    """
    NÃO BỘ: Phân cấp 3 tầng lớp thợ săn (ple helppp meee!)
    Cấp 1 (🥇): Winrate > 90%, ROI > 500% -> ƯU TIÊN CAO
    Cấp 2 (🥈): Winrate > 80%, ROI > 200% -> ƯU TIÊN TRUNG BÌNH
    Cấp 3 (🥉): Winrate > 70%, ROI > 100% -> ƯU TIÊN THẤP
    """
    try:
        # GIẢ LẬP CHỈ SỐ (Thay bằng API Birdeye/DEX nếu có)
        # Ple helppp meee! Bot đang giả định thông số để bạn thấy cách nó phân cấp
        win_rate = 85  
        avg_roi = 250   
        token_diversity = 10 

        # --- LOGIC PHÂN CẤP (NÃO BỘ LÀM VIỆC) ---
        
        # CẤP 1: HUYỀN THOẠI (🥇)
        if win_rate >= 90 and avg_roi >= 500:
            rank = "🥇 HUYỀN THOẠI (S-RANK)"
            priority = "🔥 CAO NHẤT"
            print(f"✅ [PHÊ DUYỆT]: Ví {wallet[:8]}... là {rank}")
            return True, win_rate, avg_roi, rank, priority

        # CẤP 2: CAO THỦ (🥈)
        elif win_rate >= 80 and avg_roi >= 200:
            rank = "🥈 CAO THỦ (A-RANK)"
            priority = "⚡ TRUNG BÌNH"
            print(f"✅ [PHÊ DUYỆT]: Ví {wallet[:8]}... là {rank}")
            return True, win_rate, avg_roi, rank, priority

        # CẤP 3: TÂN BINH PRO (🥉)
        elif win_rate >= 70 and avg_roi >= 100:
            rank = "🥉 TÂN BINH PRO (B-RANK)"
            priority = "🌱 THẤP"
            print(f"✅ [PHÊ DUYỆT]: Ví {wallet[:8]}... là {rank}")
            return True, win_rate, avg_roi, rank, priority
        
        # KHÔNG ĐẠT CHUẨN
        print(f"❌ [LOẠI]: Ví {wallet[:8]}... (WR: {win_rate}%, ROI: {avg_roi}%) không đủ trình độ.")
        return False, 0, 0, "", ""
    except Exception as e:
        print(f"⚠️ [LỖI NÃO BỘ]: {e}")
        return False, 0, 0, "", ""

def get_pro_traders_24h():
    """Quét 24h và phân loại theo 3 cấp độ (pl hepl meee!)"""
    if not HELIUS_KEY:
        print("🚨 [ERROR]: Thiếu API Key!")
        return []

    url = f"https://api.helius.xyz/v0/addresses/675k1q2AY9zGgXSBMshkGk666vS1Wf3gBdr35L3K37sw/transactions?api-key={HELIUS_KEY}"
    
    try:
        print(f"📡 [{datetime.now().strftime('%H:%M:%S')}] Đang soi lịch trình 24h...")
        response = requests.get(url)
        if response.status_code == 200:
            txs = response.json()
            qualified_wallets = []
            processed_wallets = set()
            now = datetime.now(timezone.utc).timestamp()

            for tx in txs:
                if now - tx.get('timestamp', 0) <= 86400:
                    description = tx.get('description', '')
                    if description:
                        wallet = description.split(' ')[0]
                        if len(wallet) >= 32 and wallet not in processed_wallets:
                            processed_wallets.add(wallet)
                            
                            # NÃO BỘ KIỂM TRA VÀ PHÂN CẤP
                            is_qualified, wr, roi, rank, priority = brain_check_performance(wallet)
                            if is_qualified:
                                qualified_wallets.append({
                                    "address": wallet, "winrate": wr, "roi": roi, 
                                    "rank": rank, "priority": priority
                                })
                else: break
            
            print(f"📊 Kết quả quét: Thẩm định {len(processed_wallets)} ví. Giữ lại {len(qualified_wallets)} ví chất lượng.")
            return qualified_wallets
    except: return []

def send_to_telegram(data):
    """Gửi tin nhắn có đánh dấu độ ưu tiên (ple helppp meee!)"""
    wallet = data["address"]
    gmgn_link = f"https://gmgn.ai/sol/address/{wallet}"
    solscan_dev = f"https://solscan.io/address/{wallet}"
    
    header = f"🚨 **DETECTION: {data['rank']}**"
    
    body = (
        f"👤 **Address:** `{wallet}`\n"
        f"----------------------------------\n"
        f"🎯 **Winrate:** {data['winrate']}% | 📈 **ROI:** {data['roi']}%\n"
        f"🚩 **ĐỘ ƯU TIÊN:** `{data['priority']}`\n"
        f"----------------------------------\n"
        f"🕵️ **Lịch trình:** Ví này đang hoạt động cực năng suất trong 24h qua!"
    )

    footer = (
        f"🚀 [GMGN.AI]({gmgn_link})\n"
        f"💰 [CHECK DEV WALLET]({solscan_dev})"
    )

    full_message = f"{header}\n\n{body}\n\n{footer}"
    
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": full_message, "parse_mode": "Markdown", "disable_web_page_preview": True})
        print(f"📤 [TELEGRAM]: Đã báo cáo ví {data['rank']}...")
    except: pass

def hunt():
    print(f"🚀 === BẮT ĐẦU QUÉT PHÂN CẤP: {datetime.now().strftime('%H:%M:%S')} ===")
    pro_traders = get_pro_traders_24h()
    
    if not pro_traders:
        print("📭 Không tìm thấy ví nào đạt chuẩn 3 cấp độ.")
    else:
        # Sắp xếp để gửi ví xịn nhất lên trước
        pro_traders.sort(key=lambda x: x['winrate'], reverse=True)
        for trader in pro_traders:
            send_to_telegram(trader)
            time.sleep(1.5)
    print(f"😴 === HOÀN THÀNH. ĐANG NGHỈ NGƠI... ===\n")

if __name__ == "__main__":
    if TOKEN and CHAT_ID: hunt()
