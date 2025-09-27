import tkinter as tk

class LoginAccountWin:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Login")
        self.window.geometry("400x200")
        self.window.resizable(False, False)

        panel = tk.Frame(self.window, padx=20, pady=20)
        panel.pack(expand=True)

        tk.Label(panel, text="",
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))

        tk.Label(panel, text="Username:").pack(anchor="w")
        self.username_entry = tk.Entry(panel, width=30)
        self.username_entry.pack()

        tk.Label(panel, text="Password:").pack(anchor="w", pady=(10, 0))
        self.password_entry = tk.Entry(panel, show="*", width=30)
        self.password_entry.pack()

        button_frame = tk.Frame(panel)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side="left", padx=5)
        tk.Button(button_frame, text="Login", command=self.login).pack(side="left", padx=5)

    def login(self):
        self.window.destroy()
