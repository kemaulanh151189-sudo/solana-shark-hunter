# 🦈 Solana Whale & Meme Sniper Pro

Hệ thống săn tìm Smart Money và các Meme Token tiềm năng trên mạng Solana với bộ lọc bảo mật tối đa.

## 🎯 Chiến thuật săn mồi (Personal Strategy)
Bot được thiết lập theo tiêu chuẩn khắt khe nhất để loại bỏ 95% dự án scam:
- ✅ **Liquidity Pool (LP):** Tối thiểu > 15 SOL.
- ✅ **Top 10 Holders:** Tổng lượng nắm giữ PHẢI < 5% (Chống xả thanh khoản).
- ✅ **Recency:** Chỉ quét các Token vừa list trong vòng < 5 phút.
- ✅ **Security:** Tự động check quyền Freeze, Mint và Tax (> 30% là bỏ).

## 🛠️ Cấu trúc hệ thống
1. **Shark Hunter (`shark_hunter.py`):** Theo dõi ví cá mập có ROI > 200% và Winrate > 80%.
2. **Meme Hunter (`meme_hunter_pro.py`):** Săn tìm các dự án mới vừa "ra lò" đạt chuẩn an toàn.

## 🛡️ Luật sinh tồn (Security Rules)
- **Tuyệt đối KHÔNG** ký các lệnh "Approve Access" hoặc "Set Authority" trên các dApp lạ.
- Chỉ giao dịch thông qua các Trading Bot uy tín hoặc ví Burner.
- Luôn kiểm tra trạng thái **LP Burned** trước khi xuống tiền.

## 🚀 Khởi chạy
Hệ thống chạy tự động qua **GitHub Actions** mỗi 2 phút.
