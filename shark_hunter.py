import os
import requests
import time
from datetime import datetime, timezone

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
BIRDEYE_KEY = os.getenv("BIRDEYE_API_KEY", "public")  # Default public, nhưng recommend đăng ký key

def calculate_real_performance(wallet):
    """Calc real winrate (% unique tokens win) và avg ROI từ Birdeye trade history."""
    try:
        url = f"https://public-api.birdeye.so/defi/history_trade_address?address={wallet}&address_type=owner&type=ALL&tx_num=100&offset=0"
        headers = {"X-API-KEY": BIRDEYE_KEY, "x-chain": "solana"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[LỖI BIRDEYE]: {response.text}")
            return 0, 0

        trades = response.json().get('data', {}).get('items', [])
        if not trades:
            return 0, 0

        unique_tokens = {}  # token_address: profit (nếu >0 thì win)
        for trade in trades:
            token = trade.get('token_address')
            profit = trade.get('value_change', 0)  # Profit in USD or SOL, tùy
            if token not in unique_tokens or profit > unique_tokens[token]:
                unique_tokens[token] = profit

        total_tokens = len(unique_tokens)
        win_tokens = sum(1 for p in unique_tokens.values() if p > 0)
        winrate = (win_tokens / total_tokens * 100) if total_tokens > 0 else 0

        win_rois = [p for p in unique_tokens.values() if p > 0]
        avg_roi = (sum(win_rois) / len(win_rois) * 100) if win_rois else 0  # % ROI avg từ wins

        return winrate, avg_roi
    except Exception as e:
        print(f"[LỖI CALC]: {e}")
        return 0, 0

def brain_check_performance(wallet):
    """
    NÃO BỘ: Phân cấp 3 tầng lớp thợ săn
    Cấp 1 (🥇): Winrate > 90%, ROI > 500% -> ƯU TIÊN CAO
    Cấp 2 (🥈): Winrate > 80%, ROI > 200% -> ƯU TIÊN TRUNG BÌNH
    Cấp 3 (🥉): Winrate > 70%, ROI > 100% -> ƯU TIÊN THẤP
    Winrate = % unique tokens win (profit >0), ROI avg từ wins.
    """
    win_rate, avg_roi = calculate_real_performance(wallet)

    if win_rate > 90 and avg_roi > 500:
        rank = "🥇 Gold Medal HUYỀN THOẠI (S-RANK)"
        priority = "CAO NHẤT"
    elif win_rate > 80 and avg_roi > 200:
        rank = "🥈 Silver Medal CAO THỦ (A-RANK)"
        priority = "TRUNG BÌNH"
    elif win_rate > 70 and avg_roi > 100:
        rank = "🥉 Bronze Medal TÂN BINH PRO (B-RANK)"
        priority = "THẤP"
    else:
        print(f"[LOẠI]: Ví {wallet[:8]}... (WR: {win_rate:.1f}%, ROI: {avg_roi:.1f}%) không đủ.")
        return False, win_rate, avg_roi, "", ""

    print(f"[PHÊ DUYỆT]: Ví {wallet[:8]}... là {rank}")
    return True, win_rate, avg_roi, rank, priority

def get_pro_traders_24h():
    """Quét top traders 24h từ Birdeye, filter theo level."""
    if not BIRDEYE_KEY:
        print("[ERROR]: Thiếu BIRDEYE_API_KEY!")
        return []

    url = "https://public-api.birdeye.so/defi/traders?sort_by=win_rate&sort_type=desc&limit=50&offset=0&time_from=24h"
    headers = {"X-API-KEY": BIRDEYE_KEY, "x-chain": "solana"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[LỖI TOP TRADERS]: {response.text}")
            return []

        traders = response.json().get('data', {}).get('items', [])
        qualified_wallets = []
        for trader in traders:
            wallet = trader.get('wallet_address')
            is_qualified, wr, roi, rank, priority = brain_check_performance(wallet)
            if is_qualified:
                qualified_wallets.append({
                    "address": wallet, "winrate": wr, "roi": roi, 
                    "rank": rank, "priority": priority
                })
        print(f"Kết quả: {len(qualified_wallets)} ví đạt cấp.")
        return qualified_wallets
    except Exception as e:
        print(f"[LỖI QUÉT]: {e}")
        return []

def send_to_telegram(data):
    """Gửi tin nhắn với level + priority."""
    wallet = data["address"]
    gmgn_link = f"https://gmgn.ai/sol/address/{wallet}"
    solscan_link = f"https://solscan.io/address/{wallet}"

    header = f"**DETECTION: {data['rank']}**"
    body = (
        f"**Address:** `{wallet}`\n"
        f"**Winrate:** {data['winrate']:.1f}% | **ROI:** {data['roi']:.1f}%\n"
        f"**ƯU TIÊN:** `{data['priority']}`\n"
        f"Hoạt động 24h: High performer!"
    )
    footer = f"[GMGN]({gmgn_link}) | [Solscan]({solscan_link})"

    full_message = f"{header}\n\n{body}\n\n{footer}"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": full_message, "parse_mode": "Markdown", "disable_web_page_preview": True})
        print(f"[TELEGRAM]: Sent {data['rank']} ví...")
    except Exception as e:
        print(f"[LỖI TELEGRAM]: {e}")

def hunt():
    print(f"=== QUÉT WHALE: {datetime.now().strftime('%H:%M:%S')} ===")
    pro_traders = get_pro_traders_24h()
    if pro_traders:
        pro_traders.sort(key=lambda x: x['winrate'], reverse=True)
        for trader in pro_traders:
            send_to_telegram(trader)
            time.sleep(2)  # Anti-spam
    else:
        print("No qualified whales.")
    print("=== DONE ===\n")

if __name__ == "__main__":
    if TOKEN and CHAT_ID and BIRDEYE_KEY:
        hunt()
    else:
        print("[ERROR]: Thiếu env vars!")
