import tkinter as tk
from views.login import LoginPage
from views.main_layout import MainLayout
from tkinter import ttk

class RentalMobilApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Sistem Rental Mobil")
        self.state('zoomed')

        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for PageClass in (LoginPage, MainLayout):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("LoginPage")

    def show_page(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = RentalMobilApp()
    app.mainloop()