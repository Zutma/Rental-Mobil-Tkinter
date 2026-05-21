import tkinter as tk
import theme

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg=theme.COLOR_WHITE)

        tk.Label(
            self, 
            text="WELCOME TO DASHBOARD", 
            font=theme.FONT_LARGE, 
            bg=theme.COLOR_WHITE, 
            fg=theme.COLOR_DARK
        ).pack(expand=True)