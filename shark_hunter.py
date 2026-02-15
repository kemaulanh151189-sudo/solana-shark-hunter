import os
import requests
import time
from datetime import datetime, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
BIRDEYE_KEY = os.getenv("BIRDEYE_API_KEY", "public")  # Dùng public để test

def get_top_traders_24h():
    url = "https://public-api.birdeye.so/defi/traders?sort_by=win_rate&sort_type=desc&limit=50&offset=0&time_from=24h"
    headers = {"X-API-KEY": BIRDEYE_KEY, "x-chain": "solana"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[LỖI BIRDEYE]: {response.status_code} - {response.text}")
            return []
        data = response.json().get('data', {}).get('items', [])
        return data
    except Exception as e:
        print(f"[LỖI QUÉT TOP]: {e}")
        return []

def calculate_real_performance(trader_data):
    winrate = trader_data.get('win_rate', 0) * 100  # Birdeye thường cho 0-1, convert %
    roi = trader_data.get('pnl_roi', 0) or trader_data.get('pnl', 0)  # Dùng PNL nếu no ROI, nhưng approx

    return winrate, roi

def brain_check_performance(wallet, winrate, roi):
    # Hạ filter thấp để test gửi ngay (winrate >50%, ROI >50%)
    if winrate > 90 and roi > 500:
        rank = "🥇 CẤP 1 - ƯU TIÊN CAO"
        prio = "CAO"
        level = 1
    elif winrate > 80 and roi > 200:
        rank = "🥈 CẤP 2 - ƯU TIÊN TRUNG BÌNH"
        prio = "TRUNG BÌNH"
        level = 2
    elif winrate > 50 and roi > 50:  # Thấp để test
        rank = "🥉 CẤP 3 - ƯU TIÊN THẤP"
        prio = "THẤP"
        level = 3
    else:
        print(f"[LOẠI]: {wallet[:8]}... WR:{winrate:.1f}% ROI:{roi:.1f}% không đạt.")
        return None

    print(f"[OK]: {wallet[:8]}... {rank}")
    return {"wallet": wallet, "winrate": winrate, "roi": roi, "rank": rank, "prio": prio, "level": level}

def hunt_top_10():
    traders = get_top_traders_24h()
    results = []
    for t in traders:
        wallet = t.get('wallet_address')
        if wallet:
            wr, roi = calculate_real_performance(t)
            perf = brain_check_performance(wallet, wr, roi)
            if perf:
                results.append(perf)
        time.sleep(0.5)  # Anti-rate

    # Sort theo level cao, rồi winrate desc
    results.sort(key=lambda x: (x['level'], -x['winrate']))
    top_10 = results[:10]
    print(f"Tìm {len(top_10)} ví xuất sắc 24h qua.")
    return top_10

def send_telegram(whale):
    msg = (
        f"**TOP WHALE 24H: {whale['rank']}**\n"
        f"**Ví:** `{whale['wallet']}`\n"
        f"Winrate: {whale['winrate']:.1f}% | ROI: {whale['roi']:.1f}%\n"
        f"**Ưu tiên:** {whale['prio']}\n"
        f"[GMGN](https://gmgn.ai/sol/address/{whale['wallet']}) | [Birdeye](https://birdeye.so/solana/wallet-analyzer/{whale['wallet']})"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        print(f"Gửi TG: {whale['wallet'][:8]}...")
    except Exception as e:
        print(f"Lỗi TG: {e}")

if __name__ == "__main__":
    print(f"--- Quét 24h: {datetime.now().strftime('%H:%M')} ---")
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Thiếu TG env!")
    else:
        top = hunt_top_10()
        for w in top:
            send_telegram(w)
            time.sleep(3)
    print("Done.")
