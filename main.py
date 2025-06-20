import tkinter as tk
from PIL import Image, ImageTk, Image as PILImage
from pynput import keyboard, mouse
import threading
import sys
import os
import pystray


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # khi chạy .exe
    except Exception:
        base_path = os.path.abspath(".")  # khi chạy Python bình thường
    return os.path.join(base_path, relative_path)

IMG_IDLE = resource_path("img/11.png")
IMG_PRESS = [resource_path("img/22.png"), resource_path("img/33.png")]


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