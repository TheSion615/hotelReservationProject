import tkinter as tk
from tkinter import messagebox


class CreateAccountWin:
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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if len(username) == 0 or len(password) < 9:
            messagebox.showerror("Invalid Input", "Refer to username and password requirements.", parent=self.window)
            return

        messagebox.showinfo("Success", f"Account has been created for {username}!", parent=self.window)
        self.window.destroy()
        self.main_app.display_home_screen()

    def cancel(self):
        self.window.destroy()
        self.main_app.display_home_screen()
