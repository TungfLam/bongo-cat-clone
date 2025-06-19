# 🐾 BongoCat Desktop - by Tùng Lâm

Hiển thị chú mèo gõ phím dễ thương dưới góc màn hình Windows, tương tác khi nhấn phím hoặc click chuột, luôn nổi trên các cửa sổ khác. Có icon khay hệ thống (System Tray) → click chuột phải để **Thoát** chương trình.

 

## ✅ Yêu cầu môi trường

- **Python**: >= 3.8 (Đã kiểm tra ổn định trên Python 3.9 → 3.13)
- **Hệ điều hành**: Windows 10 / 11 (khuyến nghị)
- **Gói cần cài:**

 
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

Build với UPX:

pyinstaller --noconsole --onefile --add-data "img;img" --upx-dir "C:\upx" main.py
📁 Cấu trúc thư mục dự án
 
bongo_cat_clone/
├── img/
│   ├── 11.png     # Ảnh idle (mặc định)
│   ├── 22.png     # Ảnh nhấn phím 1
│   └── 33.png     # Ảnh nhấn phím 2
├── main.py        # Code chính
├── README.md      # (File hướng dẫn này)
✨ Tính năng chính
🖥️ Hiển thị ở góc dưới bên phải màn hình, không bị che bởi taskbar

🎹 Đổi ảnh ngẫu nhiên khi ấn phím hoặc click chuột

🖱️ Di chuyển tự do bằng cách kéo chuột

📌 Luôn nổi trên mọi cửa sổ

🖼️ Có icon ở khay hệ thống → Chuột phải Thoát chương trình

🔖 Bản quyền & Tác giả
by Tùng Lâm
Ảnh mèo sử dụng: bongo cat 

 