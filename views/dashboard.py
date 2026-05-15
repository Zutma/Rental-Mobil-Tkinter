import tkinter as tk

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="#2ECC71")

        label = tk.Label(self, text="halaman dashboard", font=("Arial", 30, "bold"), bg="#2ECC71", fg="white")
        label.pack(pady=50)

        btn_back=tk.Button(self, text="logout", command=lambda: controller.show_frame("LoginPage"))
        btn_back.pack()