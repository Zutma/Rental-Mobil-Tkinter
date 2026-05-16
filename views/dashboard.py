import tkinter as tk

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")

        tk.Label(
            self, 
            text="WELCOME TO DASHBOARD", 
            font=("Arial", 24, "bold"), 
            bg="white", 
            fg="#333333"
        ).pack(expand=True)