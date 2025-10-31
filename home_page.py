import hashlib
import os
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk

# dict for room type and price
room_info = {
    "KR": {"name": "King Room", "per_floor": 4, "price": 59.00 },
    "TR": {"name": "Twin Room", "per_floor": 2, "price": 69.00 },
    "DR": {"name": "Deluxe King Room", "per_floor": 4, "price": 75.00 },
    "CR": {"name": "Corner King Room", "per_floor": 4, "price": 90.00 },
    "CS": {"name": "Corner Suite", "per_floor": 2, "price": 110.00 }
}

reservation_file = "./reservations.txt"


class MainInterface:
    # main interface after user login
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.setup_main_interface()

    def setup_main_interface(self):
        """logged-in home screen interface"""
        # Clear the previous screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Welcome, {self.username}!")
        self.root.geometry("600x600")

        # Top section with a title
        title = tk.Label(self.root, text="Welcome to the Hotel Reservation System!",
                         font=("Arial", 15, "bold"))
        title.pack(pady=20)

        # load in image
        try:
            hotel_img = Image.open("hotelPlan.jpg").resize((300, 300)) # open and resize the phtoto
            photo = ImageTk.PhotoImage(hotel_img)
            img_label = tk.Label(self.root, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(self.root, text=f"Could not load image: {e}", fg="red")
            error_label.pack()

        # room selectors
        selector_frame = tk.Frame(self.root)
        selector_frame.pack(pady=15)

        tk.Label(selector_frame, text="Select Floor:").grid(row=0, column=0, padx=5, pady=5)
        self.floor_var = tk.StringVar(value="1st Floor")
        tk.OptionMenu(selector_frame, self.floor_var, "1st Floor", "2nd Floor", "3rd Floor").grid(row=0, column=1)

        tk.Label(selector_frame, text="Select Room Type:").grid(row=1, column=0, padx=8, pady=5)
        self.room_var = tk.StringVar(value="KR - King Room ($59)")
        tk.OptionMenu(
            selector_frame, self.room_var,
            *[f"{code} - {info['name']} (${info['price']:.2f})" for code, info in room_info.items()]
        ).grid(row=1, column=1)

        """Buttons"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Reserve Room", command=self.reserve_room, width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel Reservation", command=self.cancel_reservation, width=18).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Available Room Info", command=self.show_manager_info, width=15).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Log Out", command=self.logout, width=10).grid(row=1, column=1, pady=10)
        #tk.Button(selector_frame, text="Show Selection", command=self.show_selection).grid(row=2, column=0, columnspan=2, pady=10)

      # logout frame
        # button_frame = tk.Frame(self.root)
        # button_frame.pack(pady=10)
        # tk.Button(button_frame, text="Log Out", command=self.logout).pack()
    
    def load_reservations(self):
        # function to load reservation file and return hotel specifics
        empty_list = []
        if not os.path.exists(reservation_file):
            return empty_list
        try:
            with open(reservation_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except (IOError, PermissionError):
            messagebox.showerror("Error! Unable to read reservations file!")
            return empty_list
    
    def save_reservation(self, reservations):
        # function to write created reservations to file
        try:
            with open(reservation_file, "w") as f:
                for r in reservations:
                    f.write(r + "\n\n")
        except (IOError, PermissionError):
            messagebox.showerror("Error! Unable to update reservations file!")
    
    def reserved_counting(self):
        # function to return how many of each type is reserved
        counts ={(floor, rtype): 
                 0 for floor in ["1st Floor", "2nd Floor", "3rd Floor"] 
                 for rtype in room_info
                }
        for line in self.load_reservations():
            try: 
                _, floor, room_type, _ = line.split(",")
                counts[(floor, room_type)] +=1
            except ValueError:
                continue
        return counts

    def reserve_room(self):
        # function to reserve a room
        selected_floor = self.floor_var.get()
        selected_room = self.room_var.get().split(" - ")[0]

        all_reservations = self.load_reservations()
        counts = self.reserved_counting()
        room_information = room_info[selected_room]

        if counts[(selected_floor, selected_room)] >= room_information["per_floor"]:
            messagebox.showwarning("Sold out", f"Apologies, {room_information['name']}s on {selected_floor} are currently booked.")

        # Prevent duplicate reservation per user
        if any(r.startswith(f"{self.username},") for r in all_reservations):
            messagebox.showinfo("Notice", "You already have a reservation. Cancel it first to book another.")
            return

        new_entry = f"{self.username},{selected_floor},{selected_room},{room_information['price']}"
        all_reservations.append(new_entry)
        self.save_reservation(all_reservations)
        messagebox.showinfo("Success", f"You have been reserved for the {room_information['name']} on the {selected_floor} for ${room_information['price']:.2f}.")

    def cancel_reservation(self):
        """Cancel current user's reservation."""
        all_res = self.load_reservations()
        new_res = [r for r in all_res if not r.startswith(f"{self.username},")]

        if len(new_res) == len(all_res):
            messagebox.showinfo("Cancel Reservation", "No reservation found under your name.")
        else:
            self.save_reservation(new_res)
            messagebox.showinfo("Cancelled", "Your reservation has been cancelled.")

    def show_manager_info(self):
        # function to display window showing availble floors and type
        win = Toplevel(self.root)
        win.title("Room Information")
        win.geometry("450x450")
        win.resizable(False, False)
        win.transient(self.root)

        tk.Label(win, text="Current Room Availability", font=("Times New Roman", 13, "bold")).pack(pady=10)
        container = tk.Frame(win)
        container.pack(expand=True)
        #container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, width=400, height=220)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        counts = self.reserved_counting()

        for floor in ["1st Floor", "2nd Floor", "3rd Floor"]:
            tk.Label(scrollable_frame, text=f"{floor}", font=("Arial", 11, "bold")).pack(pady=3)
            for code, info in room_info.items():
                reserved = counts[(floor, code)]
                remaining = info["per_floor"] - reserved
                tk.Label(scrollable_frame, text=f"  {info['name']} ({code}): {remaining} available").pack(anchor="w")

        tk.Button(win, text="Cancel", command=win.destroy, width=12).pack(pady=10)

    def logout(self):
        # function to return user to main home
        from main import Main
        Main(self.root)

