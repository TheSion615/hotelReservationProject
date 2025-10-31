import hashlib
import re
import tkinter as tk
import os
from tkinter import messagebox

credential_file = "./credentials.txt"

class CreateAccountWin:
    
    # user account creation in window

    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app

        self.window = tk.Toplevel(root)
        self.window.title("Create Account")
        self.window.geometry("500x300")
        self.window.resizable(False, False)

        self.panel = tk.Frame(self.window)
        self.panel.pack(pady=20)

        # Username
        tk.Label(self.panel, text="Create a username: ").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(self.panel, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password
        tk.Label(self.panel, text="Create a password: ").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.panel, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # password requirements
        tk.Label(
            self.panel,
            text="At least 9 characters, Upper case letter, Lower case letter, At least 1 Number(s)",
            fg="gray"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        # buttons
        button_frame = tk.Frame(self.panel)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=10)
        self.create_button = tk.Button(button_frame, text="Create Account", command=self.create_account)
        self.create_button.pack(side="left", padx=10)

        # Center the top 
        self.window.transient(self.root)
        self.window.grab_set()
        self.root.wait_window(self.window)

    def create_account(self):
        # Function to create a new user after validation
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Invalid Input", "Username and password cannot be empty.", parent=self.window)
            return
        
        existing = {}
        
        # validater path and esnure file is located and then load existing accounts safely
        if os.path.exists(credential_file):
            try:
                with open(credential_file, "r") as f:
                    for line in f:
                        try:
                            user, pw = line.strip().split(":")
                            existing[user] = pw
                        except ValueError:
                            continue
            except (IOError, PermissionError) as e:
                messagebox.showerror("File Error", f"Error reading credentials: {e}", parent=self.window)
                return

        # Validate password           
        if not self.validate_password(password):
            messagebox.showerror("Invalid Input", "Refer to username and password requirements.", parent=self.window)
            return

        # check for duplicate created username
        if username in existing:
            messagebox.showerror("Error", "Username already exists", parent=self.window)
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # save credentials to file
        try:
            with open(credential_file, "a") as f:
                f.write(f"{username}:{hashed_password}\n")
        except (IOError, PermissionError) as e:
            messagebox.showerror("File Error", f"Could not save account: {e}", parent=self.window)
            return

        messagebox.showinfo("Success", f"Account has been created for {username}", parent=self.window)
        self.window.destroy()
        self.main_app.display_home_screen()

    # function 
    def validate_password(self, password):
        # function to check if password meets requirements
        if len(password) < 9:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True
    
    def cancel(self):
        self.window.destroy()
        self.main_app.display_home_screen()
