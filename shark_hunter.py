import os
import requests
import time

# --- THÔNG TIN TỪ SECRETS ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(wallet, winrate, pnl, trades_per_month, token_name):
    """Gửi cảnh báo về Telegram chỉ khi cá mập hoạt động chăm chỉ"""
    message = (
        f"🔥 **PHÁT HIỆN TRADER MEME THỰC THỤ** 🔥\n"
        f"---------------------------\n"
        f"👤 **Ví:** `{wallet}`\n"
        f"📊 **Winrate (30d):** `{winrate}%`\n"
        f"🔄 **Tần suất:** `{trades_per_month} lệnh/tháng` (Rất tích cực)\n"
        f"💰 **Tổng lãi:** `+{pnl} SOL`\n"
        f"💎 **Kèo mới nhất:** {token_name}\n"
        f"---------------------------\n"
        f"🔗 [Soi ví ngay](https://solscan.io/account/{wallet})"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def heavy_trader_scan():
    print("🔎 Đang lọc danh sách cá mập chăm chỉ...")
    
    # Giả lập dữ liệu quét được từ hệ thống
    # TRADES_COUNT là số lệnh trong 1 tháng
    scan_results = [
        {"address": "5tz69nnU9NBP3sre6YnyW69G58X8r6T1", "winrate": 85, "pnl": 150, "trades": 120, "token": "$SOLAMA"},
        {"address": "7Yv5Hq6U9...abc", "winrate": 90, "pnl": 10, "trades": 2, "token": "$PEPE"}, # Con này lười, sẽ bị loại
    ]
    
    for shark in scan_results:
        # BỘ LỌC THÔNG MINH: Winrate > 80% VÀ phải đánh trên 50 lệnh/tháng
        if shark['winrate'] >= 80 and shark['trades'] >= 50:
            print(f"✅ Đã tìm thấy cao thủ: {shark['address']} với {shark['trades']} lệnh.")
            send_alert(shark['address'], shark['winrate'], shark['pnl'], shark['trades'], shark['token'])
        else:
            print(f"❌ Loại ví {shark['address'][:8]} vì quá lười hoặc winrate thấp.")

if __name__ == "__main__":
    if not TOKEN or not CHAT_ID:
        print("ple helppp meee! Secrets chưa chuẩn!")
    else:
        heavy_trader_scan()
