import tkinter as tk
import theme
from views.dashboard import DashboardView
from views.car import CarView
from views.customer import CustomerView
from views.transaction import TransactionView
from views.user import UserView

class MainLayout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        self.sidebar = tk.Frame(self, bg=theme.COLOR_PRIMARY, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.right_panel = tk.Frame(self, bg=theme.COLOR_WHITE)
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.top_header = tk.Frame(self.right_panel, bg=theme.COLOR_WHITE, height=60)
        self.top_header.pack(side="top", fill="x")
        
        tk.Label(
            self.top_header, 
            text="👤 Login sebagai: Administrator", 
            font=theme.FONT_MEDIUM, 
            bg=theme.COLOR_WHITE,
            fg=theme.COLOR_DARK
        ).pack(side="right", padx=30, pady=15)

        self.content_area = tk.Frame(self.right_panel, bg=theme.COLOR_WHITE)
        self.content_area.pack(side="bottom", fill="both", expand=True)

        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        tk.Label(
            self.sidebar, 
            text="RENTAL MOBIL", 
            font=theme.FONT_LARGE, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE
        ).pack(pady=(40, 60))

        self.views = {}
        target_views = (
            DashboardView, 
            CarView, 
            CustomerView, 
            TransactionView, 
            UserView
        )
        for ViewClass in target_views:
            view_name = ViewClass.__name__
            frame = ViewClass(parent=self.content_area, controller=self)
            self.views[view_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        def create_nav_button(text, target_view_name):
            btn = tk.Button(
                self.sidebar, 
                text=text.upper(), 
                font=theme.FONT_MEDIUM, 
                bg=theme.COLOR_PRIMARY,
                fg=theme.COLOR_WHITE,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=20, 
                pady=15, 
                command=lambda: self.show_view(target_view_name)
            )
            btn.pack(fill="x")

        create_nav_button("Dashboard", "DashboardView")
        create_nav_button("Data Mobil", "CarView")
        create_nav_button("Data Pelanggan", "CustomerView")
        create_nav_button("Data Transaksi", "TransactionView")
        create_nav_button("Data User", "UserView")

        tk.Button(
            self.sidebar, 
            text="LOGOUT",     
            font=theme.FONT_MEDIUM, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE, 
            relief="flat", 
            cursor="hand2",
            padx=20, 
            pady=15, 
            anchor="w",
            command=lambda: self.controller.show_page("LoginPage") 
        ).pack(side="bottom", fill="x")

        self.show_view("DashboardView")
    
    def show_view(self, view_name):
        if view_name in self.views:
            frame = self.views[view_name]
            frame.tkraise()
