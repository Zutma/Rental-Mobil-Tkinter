import tkinter as tk
import theme
from database.db_helper import get_dashboard_stats

class InfoCard(tk.Frame):
    def __init__(self, parent, title, value, color):
        super().__init__(parent, bg=color, height=150) 
        self.pack_propagate(False) 
        
        tk.Label(
            self, 
            text=title.upper(), 
            font=theme.FONT_TITLE, 
            bg=color, 
            fg="white"
        ).pack(anchor="w", padx=30, pady=(45, 0))
        
        self.lbl_value = tk.Label(
            self, 
            text=str(value), 
            font=theme.FONT_TITLE, 
            bg=color, 
            fg="white"
        )
        self.lbl_value.pack(anchor="w", padx=30, pady=(5, 45))

    def update_nilai(self, nilai_baru):
        self.lbl_value.config(text=str(nilai_baru))

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        self.lbl_welcome = tk.Label(
            self, 
            text="Selamat Datang, Admin", 
            font=theme.FONT_TITLE, 
            bg=theme.COLOR_WHITE, 
            fg=theme.COLOR_DARK,
            padx=30
        )
        self.lbl_welcome.pack(anchor="w", pady=(40, 20))

        stats_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20)
        stats_frame.pack(fill="x")
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        self.card_mobil = InfoCard(stats_frame, "Jumlah Mobil", "0", theme.COLOR_INFO)
        self.card_mobil.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.card_pelanggan = InfoCard(stats_frame, "Jumlah Pelanggan", "0", theme.COLOR_SUCCESS)
        self.card_pelanggan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_transaksi = InfoCard(stats_frame, "Jumlah Pesanan", "0", theme.COLOR_PRIMARY)
        self.card_transaksi.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.card_user = InfoCard(stats_frame, "Jumlah User", "0", theme.COLOR_DANGER)
        self.card_user.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Frame(self, bg=theme.COLOR_WHITE, height=30).pack()

    def refresh_data(self):
        stats = get_dashboard_stats()
        self.card_mobil.update_nilai(stats["mobil"])
        self.card_pelanggan.update_nilai(stats["pelanggan"])
        self.card_transaksi.update_nilai(stats["transaksi"])
        self.card_user.update_nilai(stats["user"])

        app = self.controller.controller
        if app.current_user:
            name = app.current_user.get("name", "User")
            self.lbl_welcome.config(text=f"Selamat Datang, {name}")