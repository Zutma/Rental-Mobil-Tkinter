import tkinter as tk

class MobilPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")

        tk.Label(
            self, 
            text="WELCOME TO MOBIL", 
            font=("Arial", 24, "bold"), 
            bg="white", 
            fg="#333333"
        ).pack(expand=True)