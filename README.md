
# 🐾 BongoCat Desktop - by Tùng Lâm

<img width="876" height="316" alt="image" src="https://github.com/user-attachments/assets/f52e9d92-559c-412e-b02a-dea2257bf61e" />

Hiển thị chú mèo gõ phím dễ thương dưới góc màn hình Windows, tương tác khi nhấn phím hoặc click chuột, luôn nổi trên các cửa sổ khác. Có icon khay hệ thống (System Tray) → click chuột phải để **Thoát** chương trình.

---

## ✅ Yêu cầu môi trường

- **Python**: >= 3.8 (Đã kiểm tra ổn định trên Python 3.9 → 3.13)
- **Hệ điều hành**: Windows 10 / 11 (khuyến nghị)
- **Gói cần cài:**

```bash
pip install pillow pynput pystray
🚀 Hướng dẫn chạy
1️⃣ Chạy trực tiếp từ mã nguồn Python:
 
python main.py
📦 Đóng gói thành file .exe (Windows)
2️⃣ Cài đặt PyInstaller (nếu chưa có):
 
pip install pyinstaller
3️⃣ Build file .exe:
 
pyinstaller --noconsole --onefile --add-data "img;img" main.py
--noconsole: Ẩn cửa sổ console

--onefile: Gói tất cả thành 1 file duy nhất

--add-data "img;img": Đưa thư mục img/ vào file thực thi
