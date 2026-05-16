from tkinter import Button
import tkinter as tk
import theme
from views.dashboard import DashboardPage
from views.mobil import MobilPage
from views.pelanggan import PelangganPage
from views.transaksi import TransaksiPage

class MainLayout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        #1. sidebar
        self.sidebar = tk.Frame(self, bg=theme.COLOR_PRIMARY, width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        #2. content
        self.content = tk.Frame(self, bg=theme.COLOR_WHITE)
        self.content.pack(side="right", fill="both", expand=True)

        #grid configuration
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        tk.Label(
            self.sidebar, 
            text="Rental Mobil", 
            font=theme.FONT_LARGE, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE
            ).pack(pady=(30,80))

        #3, register sub frame
        self.sub_frames = {}
        for F in (DashboardPage,MobilPage,PelangganPage,TransaksiPage):
            page_name =F.__name__
            frame = F(parent=self.content, controller=self)
            self.sub_frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        #4.menusystem
        def add_menu(text, view_name):
            btn = tk.Button(
                self.sidebar, 
                text=text, 
                font=theme.FONT_MEDIUM, 
                bg=theme.COLOR_PRIMARY,
                fg=theme.COLOR_WHITE,
                relief="flat",
                cursor="hand2",
                anchor="w",
                command=lambda: self.show_view(view_name)
            ).pack(fill="x")

        #create object menu
        add_menu("Dashboard", "DashboardPage")
        add_menu("Data Mobil", "MobilPage")
        add_menu("Data Pelanggan", "PelangganPage")
        add_menu("Data Transaksi", "TransaksiPage")

        #button logout
        tk.Button(
            self.sidebar, 
            text="LOGOUT",     
            font=theme.FONT_MEDIUM, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE, 
            relief="flat", 
            cursor="hand2",
            padx=10, 
            pady=10, 
            anchor="w",
            command=lambda: controller.show_page("LoginPage") 
            ).pack(side="bottom", fill="x")

        #show dashboard
        self.show_view("DashboardPage")
    
    #show kontent
    def show_view(self, view_name):
        if view_name in self.sub_frames:
            frame = self.sub_frames[view_name]
            frame.tkraise()
