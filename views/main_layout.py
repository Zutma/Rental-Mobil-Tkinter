import tkinter as tk
from tkinter import messagebox
import theme
from views.dashboard import DashboardView
from views.car import CarView, CarFormView
from views.customer import CustomerView, CustomerFormView
from views.transaction import TransactionView, TransactionFormView
from views.user import UserView, UserFormView
from views.brand import BrandView, BrandFormView
from views.car_type import CarTypeView, CarTypeFormView

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
        
        self.lbl_user_info = tk.Label(
            self.top_header, 
            text="👤 Login sebagai: Administrator", 
            font=theme.FONT_MEDIUM, 
            bg=theme.COLOR_WHITE,
            fg=theme.COLOR_DARK
        )
        self.lbl_user_info.pack(side="right", padx=30, pady=15)

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
            BrandView, BrandFormView,
            CarTypeView, CarTypeFormView,
            CarView, CarFormView,
            CustomerView, CustomerFormView,
            TransactionView, TransactionFormView,
            UserView, UserFormView
        )
        for ViewClass in target_views:
            view_name = ViewClass.__name__
            frame = ViewClass(parent=self.content_area, controller=self)
            self.views[view_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.nav_buttons = {}
        self._sidebar_items = []

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
            self.nav_buttons[target_view_name] = btn
            return btn

        def create_section_label(text):
            return tk.Label(
                self.sidebar,
                text=text.upper(),
                font=("Arial", 8, "bold"),
                bg=theme.COLOR_PRIMARY,
                fg=theme.COLOR_WHITE,
                anchor="center",
                pady=4
            )

        def add_item(widget, admin_only=False):
            self._sidebar_items.append((widget, admin_only))
            widget.pack(fill="x")

        add_item(create_nav_button("Dashboard", "DashboardView"))
        add_item(create_section_label("---------------------------------------------------------------------------------"), True)
        add_item(create_nav_button("Data Merek", "BrandView"), True)
        add_item(create_nav_button("Data Tipe", "CarTypeView"), True)
        add_item(create_section_label("---------------------------------------------------------------------------------"))
        add_item(create_nav_button("Data Mobil", "CarView"))
        add_item(create_nav_button("Data Pelanggan", "CustomerView"))
        add_item(create_nav_button("Data Transaksi", "TransactionView"))
        add_item(create_nav_button("Data User", "UserView"), True)

        self.btn_logout = tk.Button(
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
            command=self.do_logout
        )
        self.btn_logout.pack(side="bottom", fill="x")

        self.show_view("DashboardView")

    def do_logout(self):
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.controller.current_user = None
            self.controller.show_page("LoginPage")

    def setup_for_role(self, user):
        role = user.get("role", "petugas")
        name = user.get("name", "User")
        role_display = "Administrator" if role == "admin" else "Petugas"
        self.lbl_user_info.config(text=f"👤 Login sebagai: {role_display} ({name})")

        for widget, _ in self._sidebar_items:
            widget.pack_forget()
        for widget, admin_only in self._sidebar_items:
            if admin_only and role != "admin":
                continue
            widget.pack(fill="x")

        car_view = self.views.get("CarView")
        if car_view and hasattr(car_view, "setup_role"):
            car_view.setup_role(role)

        self.show_view("DashboardView")
    
    def show_view(self, view_name):
        if view_name in self.views:
            frame = self.views[view_name]
            frame.tkraise()
            if hasattr(frame, "refresh_data"):
                frame.refresh_data()
