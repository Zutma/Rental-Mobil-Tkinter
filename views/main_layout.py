import tkinter as tk
import theme
from views.dashboard import DashboardView
from views.car import CarView, CarFormView
from views.customer import CustomerView, CustomerFormView
from views.transaction import TransactionView, TransactionFormView
from views.user import UserView, UserFormView

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
            self.nav_buttons[target_view_name] = btn

        create_nav_button("Dashboard", "DashboardView")
        create_nav_button("Data Mobil", "CarView")
        create_nav_button("Data Pelanggan", "CustomerView")
        create_nav_button("Data Transaksi", "TransactionView")
        create_nav_button("Data User", "UserView")

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
        self.controller.current_user = None
        self.controller.show_page("LoginPage")

    def setup_for_role(self, user):
        role = user.get("role", "petugas")
        name = user.get("name", "User")
        role_display = "Administrator" if role == "admin" else "Petugas"
        self.lbl_user_info.config(text=f"👤 Login sebagai: {role_display} ({name})")

        admin_only = ["CarView", "UserView"]
        for view_name in admin_only:
            if view_name in self.nav_buttons:
                if role == "admin":
                    self.nav_buttons[view_name].pack(fill="x")
                else:
                    self.nav_buttons[view_name].pack_forget()

        if role != "admin":
            self._reorder_nav()

        self.show_view("DashboardView")

    def _reorder_nav(self):
        for key in ["DashboardView", "CustomerView", "TransactionView"]:
            if key in self.nav_buttons:
                self.nav_buttons[key].pack_forget()
        for key in ["DashboardView", "CustomerView", "TransactionView"]:
            if key in self.nav_buttons:
                self.nav_buttons[key].pack(fill="x")
    
    def show_view(self, view_name):
        if view_name in self.views:
            frame = self.views[view_name]
            frame.tkraise()
            if hasattr(frame, "refresh_data"):
                frame.refresh_data()
