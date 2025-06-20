import tkinter as tk
from PIL import Image, ImageTk, Image as PILImage
from pynput import keyboard, mouse
import threading
import sys
import os
import pystray
from tkinter import filedialog, messagebox


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # khi chạy .exe
    except Exception:
        base_path = os.path.abspath(".")  # khi chạy Python bình thường
    return os.path.join(base_path, relative_path)

IMG_IDLE = resource_path("img/11.png")
IMG_PRESS = [resource_path("img/22.png"), resource_path("img/33.png")]
def select_images(bongo_cat=None):
    global IMG_IDLE, IMG_PRESS, IMG_SIZE
    paths = filedialog.askopenfilenames(
        title="Chọn 3 ảnh (1 Idle, 2 Press, theo thứ tự)",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if not paths or len(paths) != 3:
        messagebox.showwarning(
            "Thông báo",
            "Bạn chưa chọn đủ 3 ảnh (1 Idle, 2 Press). Sẽ sử dụng ảnh mặc định!"
        )
        return False

    # Hỏi người dùng nhập kích thước
    size_win = tk.Toplevel()
    size_win.title("Chọn kích thước ảnh")
    tk.Label(size_win, text="Chiều rộng:").grid(row=0, column=0, padx=5, pady=5)
    width_entry = tk.Entry(size_win)
    width_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(size_win, text="Chiều cao:").grid(row=1, column=0, padx=5, pady=5)
    height_entry = tk.Entry(size_win)
    height_entry.grid(row=1, column=1, padx=5, pady=5)
    width_entry.insert(0, "400")
    height_entry.insert(0, "300")
    def set_size():
        try:
            w = int(width_entry.get())
            h = int(height_entry.get())
            size_win.destroy()
            global IMG_IDLE, IMG_PRESS, IMG_SIZE
            IMG_IDLE = paths[0]
            IMG_PRESS = [paths[1], paths[2]]
            IMG_SIZE = (w, h)
            if bongo_cat:
                bongo_cat.update_images(IMG_IDLE, IMG_PRESS, IMG_SIZE)
            messagebox.showinfo("Thành công", "Đã cập nhật ảnh và kích thước thành công!")
        except Exception:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho kích thước!")
    tk.Button(size_win, text="OK", command=set_size).grid(row=2, column=0, columnspan=2, pady=10)
    size_win.grab_set()
    size_win.wait_window()
    return True

def show_image_selector(bongo_cat=None):
    selector = tk.Toplevel() if bongo_cat else tk.Tk()
    selector.title("Chọn ảnh cho Bongo Cat")
    selector.geometry("350x150")
    tk.Label(selector, text="Vui lòng chọn 3 ảnh (1 Idle, 2 Press) cho Bongo Cat.\nNếu không chọn sẽ dùng ảnh mặc định.", wraplength=320).pack(pady=10)
    btn = tk.Button(selector, text="Chọn ảnh", command=lambda: [selector.destroy(), select_images(bongo_cat)])
    btn.pack(expand=True, fill="both", padx=20, pady=10)
    selector.grab_set()
    selector.wait_window()

# Giá trị mặc định cho kích thước ảnh
IMG_SIZE = (400, 300)

# Hiển thị chọn ảnh khi khởi động, nếu không chọn sẽ dùng mặc định
root = tk.Tk()
root.withdraw()
show_image_selector()
root.destroy()


# # Danh sách ảnh
# IMG_IDLE = "img/11.png"
# IMG_PRESS = ["img/22.png", "img/33.png"]

class BongoCat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "pink")
        self.root.configure(bg="pink")
        
        self.img_idle = ImageTk.PhotoImage(PILImage.open(IMG_IDLE))
        self.img_press = [ImageTk.PhotoImage(PILImage.open(p)) for p in IMG_PRESS]
        self.current_index = 0

        self.label = tk.Label(self.root, image=self.img_idle, bg="pink")
        self.label.pack()
        self.root.geometry("+100+100")
        # self.root.geometry("+1400+976")

        self.root.update_idletasks()  # Đảm bảo ảnh đã load kích thước

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img_width = self.img_idle.width()
        img_height = self.img_idle.height()

        x = screen_width - img_width - 10
        y = screen_height - img_height - 50
        self.root.geometry(f"+{x}+{y}")


        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        self.setup_listeners()
        threading.Thread(target=self.create_tray_icon, daemon=True).start()
        self.refresh_topmost()
        self.root.mainloop()

    def create_tray_icon(self):
        icon_image = PILImage.open(IMG_IDLE).resize((64, 64))
        menu = pystray.Menu(pystray.MenuItem("Thoát", self.exit_program))
        icon = pystray.Icon("bongo_cat", icon_image, "by Tùng Lâm", menu)
        icon.run()

    def setup_listeners(self):
        def start_listeners():
            self.listener_keyboard = keyboard.Listener(on_press=self.on_press)
            self.listener_mouse = mouse.Listener(on_click=self.on_click)
            self.listener_keyboard.start()
            self.listener_mouse.start()
        threading.Thread(target=start_listeners, daemon=True).start()

    def refresh_topmost(self):
        try:
            self.root.wm_attributes("-topmost", True)
        except:
            pass
        self.root.after(1000, self.refresh_topmost)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def show_press(self):
        img = self.img_press[self.current_index]
        self.label.config(image=img)
        self.current_index = (self.current_index + 1) % len(self.img_press)
        self.root.after(100, lambda: self.label.config(image=self.img_idle))

    def on_press(self, key):
        self.root.after(0, self.show_press)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.root.after(0, self.show_press)

    def exit_program(self, icon=None, item=None):
        try:
            self.listener_keyboard.stop()
            self.listener_mouse.stop()
        except:
            pass
        self.root.quit()
        os._exit(0)

if __name__ == "__main__":
    BongoCat()