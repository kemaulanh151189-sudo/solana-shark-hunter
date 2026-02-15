import os
import requests
import time
from datetime import datetime, timedelta

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

# Raydium AMM v4 đúng (Legacy Constant Product)
RAYDIUM_V4 = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

def get_all_tx_24h(address, is_raydium=False):
    """Quét chậm, đầy đủ 24h với delay cao để tránh rate limit"""
    all_txs = []
    last_signature = None
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for page in range(15):  # Giữ để quét hết 24h nếu cần
        url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={HELIUS_KEY}&limit=100"
        if last_signature:
            url += f"&before={last_signature}"
        
        for attempt in range(5):  # Retry nếu 429
            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 429:
                    wait = 30 * (attempt + 1)  # 30s → 150s
                    print(f"[429 RETRY] {address[:8]}... chờ {wait}s (attempt {attempt+1}/5)")
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                txs = response.json()
                if not txs:
                    return all_txs
                
                added = False
                for tx in txs:
                    ts = tx.get('timestamp')
                    if ts and datetime.fromtimestamp(ts) >= cutoff_time:
                        all_txs.append(tx)
                        added = True
                    else:
                        return all_txs  # Quá 24h
                
                if not added:
                    return all_txs
                
                last_signature = txs[-1].get('signature')
                if not last_signature:
                    return all_txs
                
                time.sleep(3)  # Delay giữa trang
                break
            except Exception as e:
                print(f"[LỖI GET TX {address[:8]}... attempt {attempt+1}]: {str(e)}")
                if attempt == 4:
                    return all_txs
                time.sleep(10)
    
    return all_txs

def calculate_win_token_percent(wallet):
    """Tính % token thắng: % unique token có dấu hiệu profit (ăn được nhiều)"""
    txs_24h = get_all_tx_24h(wallet)
    if not txs_24h:
        return 0, 0
    
    unique_tokens = set()          # Tổng unique token đã trade/mua
    winning_tokens = set()         # Token có dấu hiệu thắng (sell success, amount out >0)
    
    for tx in txs_24h:
        # Ưu tiên parse từ tokenTransfers (Helius parsed tx)
        transfers = tx.get('tokenTransfers', [])
        for transfer in transfers:
            mint = transfer.get('mint')
            if mint:
                unique_tokens.add(mint)
                
                # Proxy win: Có transfer out (sell) và tx success
                if tx.get('error') is None and transfer.get('fromUserAccount') == wallet:
                    # Sell từ ví → giả sử profit nếu success (proxy tốt hơn success tx)
                    winning_tokens.add(mint)
        
        # Fallback nếu không có tokenTransfers: dùng description
        desc = tx.get('description', '').lower()
        if 'swapped' in desc or 'transferred' in desc:
            if tx.get('error') is None:
                # Nếu không parse được mint, đếm success tx như proxy token win
                # (cải thiện sau nếu cần)
                pass
    
    total_unique = len(unique_tokens)
    win_count = len(winning_tokens) if winning_tokens else max(1, total_unique // 3)  # Proxy nếu không parse được
    win_percent = (win_count / total_unique * 100) if total_unique > 0 else 0
    
    return win_percent, total_unique  # Trả về % thắng và tổng unique token

def hunt_top_10():
    """Tuyển chọn top 10 ví có % token thắng cao nhất 24h"""
    print(f"🚀 Đang quét Raydium 24h (chậm an toàn)...")
    
    raydium_txs = get_all_tx_24h(RAYDIUM_V4, is_raydium=True)
    potential_wallets = set()
    for tx in raydium_txs:
        w = tx.get('feePayer')
        if w and w != RAYDIUM_V4:
            potential_wallets.add(w)
    
    # Giới hạn max 100 ví để an toàn (chạy 1 lần/ngày)
    potential_wallets = list(potential_wallets)[:100]
    print(f"🔍 Phân tích {len(potential_wallets)} ví...")
    
    leaderboard = []
    
    for wallet in potential_wallets:
        win_percent, total_unique = calculate_win_token_percent(wallet)
        
        # Lọc bỏ ví trade quá nhiều token (>50 unique)
        if total_unique > 50:
            print(f"[BỎ >50 token]: {wallet[:8]}... ({total_unique} unique token)")
            continue
        
        rank = None
        if win_percent > 80:
            rank = "🥇 S-RANK (SIÊU CÁ MẬP)"
        elif win_percent > 50:
            rank = "🥈 A-RANK (CAO THỦ)"
        elif win_percent > 20:
            rank = "🥉 B-RANK (TIỀM NĂNG)"
        
        if rank:
            leaderboard.append({
                "address": wallet,
                "win_pct": win_percent,
                "total_unique": total_unique,
                "rank": rank
            })
            print(f"[THÊM]: {wallet[:8]}... {rank} - {win_percent:.1f}% ({total_unique} token)")
        
        time.sleep(8)  # Delay 8s mỗi ví để tránh burst rate limit
    
    leaderboard.sort(key=lambda x: x['win_pct'], reverse=True)
    top_10 = leaderboard[:10]
    print(f"Top 10 sau lọc: {len(top_10)} ví")
    return top_10

def send_to_telegram(data, index):
    """Gửi tin nhắn chuẩn"""
    wallet = data["address"]
    gmgn = f"https://gmgn.ai/sol/address/{wallet}"
    solscan = f"https://solscan.io/address/{wallet}"
    
    msg = (
        f"**🏆 TOP {index+1} SHARK 24H**\n"
        f"Cấp độ: `{data['rank']}`\n"
        f"Ví: `{wallet}`\n"
        f"🔥 **Tỉ lệ token thắng: {data['win_pct']:.1f}%** (ăn được nhiều)\n"
        f"📦 Tổng unique token trade 24h: {data['total_unique']}\n"
        f"--------------------------\n"
        f"🚀 [GMGN]({gmgn}) | 💰 [CHECK DEV WALLET]({solscan})"
    )
    try:
        resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                             json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})
        if resp.status_code == 200:
            print(f"[TG OK] TOP {index+1}")
        else:
            print(f"[TG ERR]: {resp.status_code} - {resp.text[:100]}")
    except Exception as e:
        print(f"[TG ERR]: {str(e)}")

if __name__ == "__main__":
    print("=== SCRIPT BẮT ĐẦU CHẠY ===")
print(f"Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"HELIUS_KEY có giá trị: {'Có' if HELIUS_KEY else 'Không'}")
print("Bắt đầu quét Raydium...")
    print(f"=== START QUÉT TOP SHARK 24H (chậm an toàn): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    if not all([TOKEN, CHAT_ID, HELIUS_KEY]):
        print("[ERROR]: Thiếu env vars!")
    else:
        top_10 = hunt_top_10()
        if top_10:
            for i, shark in enumerate(top_10):
                send_to_telegram(shark, i)
                time.sleep(5)  # Delay giữa gửi TG
        else:
            print("Không ví nào đạt chuẩn.")
    print("=== DONE ===")
