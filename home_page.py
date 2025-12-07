import hashlib
import os
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk

def center_windows(window, width, height):
    window.update_idletasks()
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    #x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (450 // 2)
    #y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

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
        self.root.geometry("600x670")

        # Top section with a title
        title = tk.Label(self.root, text="Welcome to the Hotel Reservation System!",
                         font=("Times New Roman", 15, "bold"))
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
        self.floor_menu = tk.OptionMenu(selector_frame, self.floor_var, "1st Floor", "2nd Floor", "3rd Floor")
        self.floor_menu.grid(row=0, column=1)
        tk.Label(selector_frame, text="Select Room Type:").grid(row=1, column=0, padx=8, pady=5)
        self.room_var = tk.StringVar(value="Select Type")
        self.room_menu = tk.OptionMenu(selector_frame, self.room_var, "")
        self.room_menu.grid(row=1, column=1)
        tk.Label(selector_frame, text="Quantity:").grid(row=2, column=0, padx=8, pady=5)
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_menu = tk.OptionMenu(selector_frame, self.quantity_var, 1, 2, 3, 4)
        self.quantity_menu.grid(row=2, column=1)
        self.quantity_var.trace("w", lambda *args: self.update_price_display())
        self.floor_status_label = tk.Label(selector_frame, text="", fg="red", font=("Times New Roman", 11, "bold"))
        self.floor_status_label.grid(row=0, column=2, padx=10)
        self.room_status_label = tk.Label(selector_frame, text="", fg="red", font=("Times New Roman", 11, "bold"))
        self.room_status_label.grid(row=0, column=2, padx=10)
        self.room_price_label = tk.Label(selector_frame, text="", font=("Times New Roman", 12))
        self.room_price_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_floor_options()

        #self.room_var = tk.StringVar(value="KR - King Room ($59)")
        # tk.OptionMenu(
        #     selector_frame, self.room_var,
        #     *[f"{code} - {info['name']} (${info['price']:.2f})" for code, info in room_info.items()]
        # ).grid(row=1, column=1)

        """Buttons"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        self.reserve_button = tk.Button(button_frame, text="Reserve Room", command=self.reserve_room, width=15)
        self.reserve_button.grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel Reservation", command=self.cancel_reservation, width=18).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Available Room Info", command=self.show_manager_info, width=15).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Log Out", command=self.logout, width=10).grid(row=1, column=1, pady=10)
        #tk.Button(selector_frame, text="Show Selection", command=self.show_selection).grid(row=2, column=0, columnspan=2, pady=10)
        self.floor_var.trace("w", self.update_room_types)
        self.room_var.trace("w", self.update_reservation_button)
        self.update_room_types()
      # logout frame
        # button_frame = tk.Frame(self.root)
        # button_frame.pack(pady=10)
        # tk.Button(button_frame, text="Log Out", command=self.logout).pack()
        self.check_hotel_fullness()

    def update_floor_options(self):
        self.floor_status_label.config(text="")
        counts = self.reserved_counting()
        floor_menu = self.floor_menu["menu"]
        floor_menu.delete(0, "end")

        first_available = None

        for floor in ["1st Floor", "2nd Floor", "3rd Floor"]:
            floor_available = any(counts[(floor, j)] < room_info[j]["per_floor"]
                                  for j in room_info)
            
            if floor_available:
                floor_menu.add_command(label=floor, command=lambda value=floor:
                                     self.floor_var.set(value))
                if first_available is None:
                    first_available = floor
            else:
                floor_menu.add_command(
                    label=f"{floor} (Sold Out)",
                    command=lambda value=floor: self.sold_out_floor_selected(value)
                )
                if self.floor_var.get() == floor:
                    self.floor_status_label.config(text="SOLD OUT")

        current = self.floor_var.get()
        current_has_space = current in ["1st Floor", "2nd Floor", "3rd Floor"] and any(
            counts[(current, j)] < room_info[j]["per_floor"] for j in room_info
        )
        if not current_has_space:
            if first_available:
                self.floor_var.set(first_available)
            else:
                self.floor_var.set("Sold Out")
                                    
                                  

    def sold_out_floor_selected(self, floor_chosen):
        messagebox.showwarning(
            "Floor & Room Out",
            f"Apologies - {floor_chosen} is current booked and sold out. Please select a different selection."
        )

        self.update_floor_options()
        self.room_var.set("Select Type")
        self.room_status_label.config(text="")
        self.update_room_types()
    
    def update_price_display(self):
        room_text = self.room_var.get()
        if " - " not in room_text:
            self.room_price_label.config(text="")
            return
        selected_room = room_text.split(" - ")[0]
        quantity = int(self.quantity_var.get())
        base_price = room_info[selected_room]["price"]
        total_price = base_price * quantity
        self.room_price_label.config(text=f"Total Price: ${total_price:2f}")
 

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
        counts = {
            (floor, rtype): 0
            for floor in ["1st Floor", "2nd Floor", "3rd Floor"]
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
        if self.room_var.get() in ("Select Type", "Sold Out"):
            messagebox.showinfo("No selection", "Please choose a valid room type before reserving.")
            return
        selected_room = self.room_var.get().split(" - ")[0]

        all_reservations = self.load_reservations()
        counts = self.reserved_counting()
        room_information = room_info[selected_room]

        
        """
        Below commented out to allow users to be able to book multiple rooms.
        """
        # user_res = next((j for j in all_reservations
        #                  if j.startswith(f"{self.username}")), None)
        # # Prevent duplicate reservation per user
        # if user_res:
        #     messagebox.showinfo("Notice", "You already have a reservation. Cancel it first to book another.")
        #     return
        
        quantity = self.quantity_var.get()
        room_count = counts[(selected_floor, selected_room)]
        remaining = room_information["per_floor"] - room_count

        if quantity > remaining:
            messagebox.showwarning(
                "Sold out", 
                f"Apologies, {room_information['name']}s on {selected_floor} are currently booked.")
            self.update_room_types()
            return

        for i in range(quantity):
            new_entry = f"{self.username},{selected_floor},{selected_room},{room_information['price']}"
            all_reservations.append(new_entry)
        self.save_reservation(all_reservations)
        # messagebox.showinfo(
        #     "Success", 
        #     f"You have been reserved for the {room_information['name']} on the {selected_floor} for ${room_information['price']:.2f}.")
        
        total_price = room_information['price'] * quantity
        confirm_window = Toplevel(self.root)
        confirm_window.title("e-ticket Confirmation")
        center_windows(confirm_window, 400, 250)
        #confirm_window.geometry("400x250")
        tk.Label(confirm_window, text="Reservation Confirmed!", font=("Times New Roman", 15, "bold")).pack(pady=10)
        tk.Label(confirm_window, text=f"Name: {self.username}").pack(pady=5)
        tk.Label(confirm_window, text=f"Floor: {selected_floor}").pack(pady=5)
        tk.Label(confirm_window, text=f"Room: {room_information['name']} ({selected_room})").pack(pady=5)
        tk.Label(confirm_window, text=f"Quantity: {quantity}").pack(pady=5)
        tk.Label(confirm_window, text=f"Total Price: ${total_price:.2f}", font=("Times New Roman", 11, "bold")).pack(pady=10)
        tk.Button(confirm_window, text="Close", command=confirm_window.destroy).pack(pady=10)
        self.update_floor_options()
        self.update_room_types()
        self.check_hotel_fullness()

        if hasattr(self, "manager_window_labels"):
            self.update_manager_window()

    def cancel_reservation(self):
        """Cancel current user's reservation."""
        all_res = self.load_reservations()
        new_res = [r for r in all_res if not r.startswith(f"{self.username},")]

        if len(new_res) == len(all_res):
            messagebox.showinfo("Cancel Reservation", "No reservation found under your name.")
        else:
            self.save_reservation(new_res)
            messagebox.showinfo("Cancelled", "Your reservation has been cancelled.")
            self.update_floor_options()
            self.update_room_types()
            self.check_hotel_fullness()
        if hasattr(self, "manager_window_labels"):
            self.update_manager_window()

    def show_manager_info(self):
        if hasattr(self, "manager_window") and self.manager_window.winfo_exists():
            self.manager_window.lift()
            return
        # function to display window showing availble floors and type
        self.manager_window = Toplevel(self.root)
        self.manager_window.title("Room Information")
        #self.manager_window.update()
        #center_windows(self.manager_window, 400, 450)
        self.manager_window.geometry("450x450")
        self.manager_window.resizable(False, False)
        self.manager_window.transient(self.root)


        tk.Label(self.manager_window, text="Current Room Availability", font=("Times New Roman", 13, "bold")).pack(pady=10)
        container = tk.Frame(self.manager_window)
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

        manager_window_labels = []
        counts = self.reserved_counting()

        for floor in ["1st Floor", "2nd Floor", "3rd Floor"]:
            tk.Label(scrollable_frame, text=f"{floor}", font=("Times New Roman", 11, "bold")).pack(pady=3)
            for code, info in room_info.items():
                reserved = counts[(floor, code)]
                remaining = info["per_floor"] - reserved
                label = tk.Label(scrollable_frame, text=f"  {info['name']} ({code}): {remaining} available")
                label.pack(anchor="w")
                manager_window_labels.append((floor, code, label))

        tk.Button(self.manager_window, text="Cancel", command=self.manager_window.destroy, width=12).pack(pady=10)
    
    def update_manager_window(self):
        if not hasattr(self, "manager_window_labels"):
            return
        counts = self.reserved_counting()
        for floor, code, label in self.manager_window_labels:
            remaining = room_info[code]["per_floor"] - counts[(floor, code)]
            label.config(text=f"  {room_info[code]['name']} ({code}): {remaining} available")

    def update_room_types(self, *args):
        self.room_price_label.config(text="")
        self.room_status_label.config(text="")
        floor = self.floor_var.get()
        counts = self.reserved_counting()
        self.room_menu["menu"].delete(0, "end")

        all_res = self.load_reservations()
        user_res = None

        for j in all_res:
            if j.startswith(f"{self.username},"):
                try:
                    _, user_floor, user_room, _ = j.split(",")
                    user_res = (user_floor, user_room)
                except ValueError:
                    continue
                
        floor_sold_out = True
        for room_type in room_info:
            room_count = counts[(floor, room_type)]
            if user_res and user_res == (floor, room_type):
                room_count -=1
            if room_count < room_info[room_type]["per_floor"]:
                floor_sold_out = False
                break

        if floor_sold_out:
            self.room_var.set("Sold Out")
            self.reserve_button.config(state="disabled")
            self.room_status_label.config(text="Floor sold out")
            return
        for room_type, info in room_info.items():
            room_count = counts[(floor, room_type)]
            # check for user's own reservation availability
            is_user_room = user_res and user_res == (floor, room_type)
            remaining = info["per_floor"] - room_count
            
            if is_user_room:
                remaining += 1

            if remaining <= 0:
                self.room_menu["menu"].add_command(
                    label=f"{room_type} - {info['name']} (Sold Out)",  
                    command=lambda ft=room_type: self.sold_out_room_selected(floor, ft)
                )
            else:
                self.room_menu["menu"].add_command(
                    label=f"{room_type} - {info['name']} (${info['price']:.2f})",
                    command=lambda value=f"{room_type} - {info['name']} (${info['price']:.2f})": 
                        self.room_var.set(value)
                )
        if user_res and user_res[0] == floor:
            room_type = user_res[1]
            room_label = f"{room_type} - {room_info[room_type]['name']} (${room_info[room_type]['price']:.2f})"
            self.room_var.set(room_label)
        else:
            self.room_var.set("Select Type")
            self.update_price_display()
        
        self.update_reservation_button()
    def sold_out_room_selected(self, floor_chosen, room_type):
        messagebox.showwarning(
            "Room Sold Out",
            f"Sorry — {room_info[room_type]['name']} on {floor_chosen} is sold out. Please choose another option."
        )
        self.room_status_label.config(text="SOLD OUT")
        self.room_var.set("Select Type")
        self.update_room_types()
        self.update_floor_options()

    def update_reservation_button(self, *args):
        if not hasattr(self, "reserve_button"):
            return
        floor = self.floor_var.get()
        #room = self.room_var.get().split(" - ")[0]
        room_text = self.room_var.get()

        if room_text == "Select Type" or room_text == "Sold Out":
            self.reserve_button.config(state="disabled")
            return
        room = room_text.split(" - ")[0]
        counts = self.reserved_counting()
        available = room_info[room]["per_floor"] - counts[(floor, room)]

        all_res = self.load_reservations()
        is_user_res = any(j.startswith(f"{self.username},{floor},{room},")
                          for j in all_res)
        self.reserve_button.config(
            state="normal"
            if available > 0 or is_user_res
            else "disabled"
        )
        # if available <= 0:
        #     self.reserve_button.config(state="disabled")
        #     # messagebox.showwarning(
        #     #     "Sold Out",
        #     #     f"Sorry, {room_info[room]['name']} on {floor} is fully booked. Please come back later.",
        #     #     icon="warning"
        #     # )
        # else:
        #     self.reserve_button.config(state="normal")
    
    def check_hotel_fullness(self):
        counts = self.reserved_counting()
        total_availability = sum(
            room_info[r]["per_floor"] - counts[(f, r)]
            for f in [
                "1st Floor", "2nd Floor", "3rd Floor"
            ]
            for r in room_info
        )

        if total_availability <= 0:
            for children in self.root.winfo_children():
                try:
                    children.config(state="disabled")
                except:
                    pass
            tk.Label(self.root, text=
                     "Unfortnuately, the hotel is FULL. Please come back later", 
                     fg="red", font=("Times New Roman", 15, "bold")).pack(pady=10)
            

    def logout(self):
        # function to return user to main home
        from main import Main
        Main(self.root)

