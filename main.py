#!/usr/bin/env python3
import tkinter as tk
from PIL import Image, ImageTk
from create_account import CreateAccountWin
from login_account import LoginAccountWin

class Main:
    def __init__(self, root):
        self.root = root
        self.create_account_window = None
        self.login_account_window = None
        self.display_home_screen()

    def display_home_screen(self):
        # clear  widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Hotel Reservation System")
        self.root.geometry("600x600")

        panel = tk.Frame(self.root)
        panel.pack(expand=True)

        title_label = tk.Label(panel, text="Hotel Reservation System", font=("Georgia", 20, "bold"))
        title_label.pack(pady=10)

        # try image.
        try:
            img = Image.open("hotel.jpg")
            img = img.resize((300, 300))
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(panel, image=photo)
            image_label.image = photo  # Keep reference
            image_label.pack(pady=5)
        except Exception as e:
            print("Image load in has failed:", e)

        # buttons
        button_frame = tk.Frame(panel)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Create Account", command=self.open_create_account).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Login", command=self.open_login).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancel", command=self.quit_app).pack(side=tk.LEFT, padx=10)

    def open_create_account(self):
        if self.create_account_window is None or not self.create_account_window.winfo_exists():
            self.create_account_window = CreateAccountWin(self.root, self)
    
    def open_login(self):
        if (self.login_account_window is None 
            or not self.login_account_window.window.winfo_exists()):
            self.login_account_window = LoginAccountWin(self.root, self)
    def quit_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
