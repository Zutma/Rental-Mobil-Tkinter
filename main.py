import tkinter as tk
import theme
from views.login import LoginPage
from views.main_layout import MainLayout

class RentalMobilApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rental Mobil")
        self.geometry("1100x700")
        self.state("zoomed")

        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

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
        if page_name in self.pages:
            frame = self.pages[page_name]
            frame.tkraise()

if __name__ == "__main__":
    app = RentalMobilApp()
    app.mainloop()