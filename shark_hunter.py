import os
import requests
import time

# --- CẤU HÌNH ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def find_real_pro_traders():
    """Tự động lùng sục các ví đang có lãi đậm trên Solana"""
    print("🔎 Đang kết nối với DEX Data để lùng ví cao thủ...")
    
    # Đây là nơi Bot gọi dữ liệu từ các sàn (Giả lập gọi API DexScreener/GMGN)
    # Nó sẽ trả về danh sách các ví vừa thực hiện lệnh mua/bán
    potential_list = [
        {"address": "H8S9pS...v1", "winrate": 88, "pnl": 250, "trades": 145, "token": "$WIF"},
        {"address": "6nc99...abc", "winrate": 70, "pnl": 50, "trades": 10, "token": "$BONK"}, # Sẽ bị loại
        {"address": "9WzDX...xyz", "winrate": 82, "pnl": 90, "trades": 85, "token": "$SOLAMA"}
    ]
    
    for shark in potential_list:
        # GIỮ LẠI BỘ LỌC CŨ CỦA BẠN:
        # 1. Winrate > 80% 
        # 2. Hoạt động > 50 lệnh/tháng (Tránh ví ảo, ví lười)
        if shark['winrate'] >= 80 and shark['trades'] >= 50:
            send_to_telegram(shark)
            print(f"✅ Đã tìm thấy và báo cáo ví: {shark['address']}")
        else:
            print(f"⏭️ Bỏ qua ví {shark['address'][:5]}... vì không đủ tiêu chuẩn.")

def send_to_telegram(data):
    # Tạo link GMGN chuẩn như bạn vừa soi trong ảnh
    gmgn_link = f"https://gmgn.ai/sol/address/{data['address']}"
    
    message = (
        f"🎯 **PHÁT HIỆN CAO THỦ THỰC CHIẾN**\n"
        f"---------------------------\n"
        f"👤 **Ví:** `{data['address']}`\n"
        f"📈 **Winrate:** `{data['winrate']}%` (30 ngày)\n"
        f"🔥 **Tần suất:** `{data['trades']} lệnh/tháng`\n"
        f"💰 **Lợi nhuận:** `+{data['pnl']} SOL`\n"
        f"💎 **Vừa mua:** {data['token']}\n"
        f"---------------------------\n"
        f"🔗 [SOI CHI TIẾT TRÊN GMGN.AI]({gmgn_link})"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        find_real_pro_traders()
    else:
        print("ple helppp meee! Check lại Secrets đi bạn ơi!")
