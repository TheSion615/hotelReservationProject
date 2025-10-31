import hashlib
import os
import tkinter as tk
from tkinter import messagebox
from home_page import MainInterface

credential_file = "./credentials.txt"

class LoginAccountWin:
    # function to handle user login verification
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.window = tk.Toplevel(root)
        self.window.title("Login")
        self.window.geometry("600x300")
        self.window.resizable(False, False)

        panel = tk.Frame(self.window, padx=20, pady=20)
        panel.pack(expand=True)

        tk.Label(panel, text="Login To Your Account" "\n" "Press the 'Login' button or press the ENTER key after entering credentials.", font=("Times New Roman", 12, "bold")).pack(pady=(0, 10))

        tk.Label(panel, text="Username:").pack(anchor="w")
        self.username_entry = tk.Entry(panel, width=30)
        #self.username_entry = tk.Entry(panel, width=30)
        self.username_entry.pack()
        self.username_entry.bind("<Return>", self.enter_key)

        tk.Label(panel, text="Password:").pack(anchor="w", pady=(10, 0))
        self.password_entry = tk.Entry(panel, show="*", width=30)
        self.password_entry.pack()
        self.password_entry.bind("<Return>", self.enter_key)

        button_frame = tk.Frame(panel)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)
        tk.Button(button_frame, text="Login", command=self.login).pack(side="left", padx=5)

        # Center the top window over the root window
        self.window.transient(self.root)
        self.window.grab_set()
        self.root.wait_window(self.window)

    def enter_key(self, event):
        self.login()
    
    def verification(self, username, password):
        # function to verify credentials
        isTrue = True
        found = False
        if not username or not password:
            messagebox.showerror("Login Failed!", "Username and password required.", parent=self.window)
            return
        
        hashed_input = hashlib.sha256(password.encode()).hexdigest()

        if os.path.exists(credential_file):
            try:
                with open(credential_file, "r") as f:
                    for line in f:
                        try:
                            user, pw_hash = line.strip().split(":")
                            if user == username and pw_hash == hashed_input:
                                found = True
                                break
                        except ValueError:
                            continue
            except (IOError, PermissionError) as e:
                messagebox.showerror("File Error", f"Unable to read credentials: {e}", parent=self.window)
                return
        else:
            messagebox.showerror("Login Failed", "No account not found. Please create an account.", parent=self.window)
            return
    
    def login(self):
        # function to login and open main interface 
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username and not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty.", parent=self.window)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            return

        if not username:
            messagebox.showerror("Login Failed", "Username is required.", parent=self.window)
            self.password_entry.delete(0, tk.END)
            return

        if not password:
            messagebox.showerror("Login Failed", "Password is required.", parent=self.window)
            self.username_entry.delete(0, tk.END)
            return

        hashed_input = hashlib.sha256(password.encode()).hexdigest()

        found = False
        if os.path.exists(credential_file):
            with open(credential_file, "r") as f:
                for line in f:
                    try:
                        saved_user, saved_hash = line.strip().split(":")
                        if saved_user == username and saved_hash == hashed_input:
                            found = True
                            break
                    except ValueError:
                        continue  # skip bad lines

        if found:
            messagebox.showinfo("Success", f"Welcome, {username}!", parent=self.window)
            self.window.destroy()
            from home_page import MainInterface
            MainInterface(self.root, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.window)
            self.password_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)

            
            # if self.verification(username, password):
            #     messagebox.showinfo("Success", f"Welcome, {username}!", parent=self.window)
            #     self.window.destroy()
            #     MainInterface(self.root, username)
            # else:
            #     messagebox.showerror("Login Failed", "Invalid username or password", parent=self.window)
            #     for _ in range(2):
            #         self.username_entry.delete(0, tk.END)
            #     self.username_entry.focus_set()

    def cancel(self):
        # function to close login window and return to home
        self.window.destroy()
        self.main_app.display_home_screen()
