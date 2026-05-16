import tkinter as tk
import theme
from views.dashboard import DashboardView
from views.mobil import MobilView
from views.pelanggan import PelangganView
from views.transaksi import TransaksiView

class MainLayout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        # 1. Sidebar Container
        self.sidebar = tk.Frame(self, bg=theme.COLOR_PRIMARY, width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # 2. Main Content Area
        self.content_area = tk.Frame(self, bg=theme.COLOR_WHITE)
        self.content_area.pack(side="right", fill="both", expand=True)

        # Grid configuration for stacked views
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        # App Title in Sidebar
        tk.Label(
            self.sidebar, 
            text="Rental Mobil", 
            font=theme.FONT_LARGE, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE
        ).pack(pady=(30, 80))

        # 3. Register Views
        self.views = {}
        for ViewClass in (DashboardView, MobilView, PelangganView, TransaksiView):
            view_name = ViewClass.__name__
            frame = ViewClass(parent=self.content_area, controller=self)
            self.views[view_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # 4. Sidebar Menu System
        def create_nav_button(text, target_view):
            btn = tk.Button(
                self.sidebar, 
                text=text, 
                font=theme.FONT_MEDIUM, 
                bg=theme.COLOR_PRIMARY,
                fg=theme.COLOR_WHITE,
                relief="flat",
                cursor="hand2",
                anchor="w",
                command=lambda: self.show_view(target_view)
            )
            btn.pack(fill="x")
            
            # Hover effects
            btn.bind("<Enter>", lambda e: btn.configure(bg=theme.COLOR_SECONDARY))
            btn.bind("<Leave>", lambda e: btn.configure(bg=theme.COLOR_PRIMARY))

        # Create navigation links
        create_nav_button("Dashboard", "DashboardView")
        create_nav_button("Data Mobil", "MobilView")
        create_nav_button("Data Pelanggan", "PelangganView")
        create_nav_button("Data Transaksi", "TransaksiView")

        # Logout Button
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
            command=lambda: self.controller.show_page("LoginPage") 
        ).pack(side="bottom", fill="x")

        # Initialize Default View
        self.show_view("DashboardView")
    
    def show_view(self, view_name):
        if view_name in self.views:
            frame = self.views[view_name]
            frame.tkraise()
