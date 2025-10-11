import hashlib
import os
import re
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MainInterface:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.setup_main_interface()

    def setup_main_interface(self):
        # Clear the previous screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Welcome, {self.username}!")
        self.root.geometry("600x500")

        # Top section with a title
        title = tk.Label(self.root, text="Welcome to the Hotel Reservation System!",
                         font=("Arial", 15, "bold"))
        title.pack(pady=20)

        try:
            hotel_img = Image.open("hotelPlan.jpg").resize((400, 300)) # open and resize the phtoto
            photo = ImageTk.PhotoImage(hotel_img)
            img_label = tk.Label(self.root, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(self.root, text=f"Could not load image: {e}", fg="red")
            error_label.pack()

        # **placeholder**s
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Log Out", command=self.logout).pack()

    def logout(self):
        from main import Main  
        # Return to main screen 
        Main(self.root)  # return to main screen    

