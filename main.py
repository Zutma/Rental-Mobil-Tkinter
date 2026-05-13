import tkinter as tk
from views.login import LoginPage
from tkinter import ttk

class RentalMobilApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Sistem Rental Mobil")
        self.state('zoomed')

        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        page = LoginPage(parent=self.main_container, controller=self)

        self.frames[LoginPage] = page
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = RentalMobilApp()
    app.mainloop()