import os
import requests
import time

# --- CẤU HÌNH ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def check_quality_shark():
    """Quét ví và áp dụng bộ lọc CHẤT LƯỢNG (không quan tâm số tiền mua)"""
    print("💎 Đang tìm kiếm các 'Diamond Hand' thực thụ...")
    
    # Giả lập dữ liệu ví lấy về từ API (GMGN/Birdeye)
    # Đây là những chỉ số quan trọng hơn số tiền mua
    detected_wallets = [
        {
            "address": "DeX1pSv1u6P5bP4vG9xR2nQ7zM3wE8tY6bC5aZ4dQ2f1", 
            "winrate": 88,          # Tỉ lệ thắng (Quan trọng)
            "total_pnl": 150.5,     # Tổng lãi ròng (Cực quan trọng - Tiền thật cầm về)
            "unique_tokens": 12,    # Số token khác nhau đã chơi (Tránh ví Dev lùa gà)
            "avg_roi": 450,         # Trung bình lãi 450% mỗi kèo (Đánh là thắng lớn)
            "last_trade": "Vừa xong"
        },
        {
            "address": "LazY7...abc", 
            "winrate": 90, 
            "total_pnl": 2.0,       # Lãi quá bé -> Loại
            "unique_tokens": 1,     # Chỉ chơi 1 con -> Ví Dev/Bot -> Loại
            "avg_roi": 10
        }
    ]
    
    for shark in detected_wallets:
        # --- BỘ LỌC CHẤT LƯỢNG CAO (LOGIC MỚI) ---
        # 1. Winrate > 80% (Giữ nguyên)
        # 2. Tổng lãi (PnL) > 50 SOL (Chứng tỏ kiếm tiền thật)
        # 3. Đã chơi > 5 Token khác nhau (Chứng tỏ là Trader chuyên nghiệp, không phải Bot 1 coin)
        
        is_high_quality = (
            shark['winrate'] >= 80 and 
            shark['total_pnl'] >= 50 and 
            shark['unique_tokens'] >= 5
        )
        
        if is_high_quality:
            print(f"💎 Tìm thấy ví KIM CƯƠNG: {shark['address']}")
            send_quality_alert(shark)
        else:
            print(f"🗑️ Loại ví rác/ít kinh nghiệm: {shark['address'][:8]}...")

def send_quality_alert(data):
    gmgn_link = f"https://gmgn.ai/sol/address/{data['address']}"
    message = (
        f"💎 **PHÁT HIỆN VÍ CHẤT LƯỢNG CAO (VIP)**\n"
        f"---------------------------\n"
        f"👤 **Ví:** `{data['address']}`\n"
        f"🏆 **Winrate:** `{data['winrate']}%`\n"
        f"💰 **Tổng Lãi:** `+{data['total_pnl']} SOL` (Uy tín)\n"
        f"📚 **Kinh nghiệm:** Đã trade `{data['unique_tokens']}` token khác nhau\n"
        f"🚀 **ROI Trung bình:** `{data['avg_roi']}%`/lệnh\n"
        f"---------------------------\n"
        f"🌟 [XEM LỊCH SỬ GIAO DỊCH TRÊN GMGN]({gmgn_link})"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        check_quality_shark()
    else:
        print("ple helppp meee! Cài lại Secrets đi bạn ơi!")
