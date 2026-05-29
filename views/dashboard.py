import theme
import tkinter as tk
import theme
from tkinter import ttk
from database.dashboard import get_dashboard_stats, get_rented_cars

class InfoCard(tk.Frame):
    def __init__(self, parent, title, value, color):
        super().__init__(parent, bg=color, height=150) 
        self.pack_propagate(False) 
        
        tk.Label(
            self, 
            text=title.upper(), 
            font=theme.FONT_TITLE, 
            bg=color, 
            fg=theme.COLOR_DARK
        ).pack(anchor="w", padx=30, pady=(45, 0))
        
        self.lbl_value = tk.Label(
            self, 
            text=str(value), 
            font=theme.FONT_TITLE, 
            bg=color, 
            fg=theme.COLOR_DARK
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

        self.card_mobil = InfoCard(stats_frame, "Jumlah Mobil", "0", theme.COLOR_GRAY)
        self.card_mobil.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.card_pelanggan = InfoCard(stats_frame, "Jumlah Pelanggan", "0", theme.COLOR_GRAY)
        self.card_pelanggan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_transaksi = InfoCard(stats_frame, "Jumlah Transaksi", "0", theme.COLOR_GRAY)
        self.card_transaksi.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.card_user = InfoCard(stats_frame, "Jumlah User", "0", theme.COLOR_GRAY)
        self.card_user.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        rented_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=30)
        rented_frame.pack(fill="both", expand=True, pady=(20, 20))

        tk.Label(rented_frame, text="Mobil Sedang Disewa", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, fg=theme.COLOR_DARK).pack(anchor="w", pady=(0, 10))

        style = ttk.Style()
        style.configure("Dashboard.Treeview", rowheight=28, background=theme.COLOR_WHITE, fieldbackground=theme.COLOR_WHITE, font=("Arial", 10))
        style.configure("Dashboard.Treeview.Heading", font=("Arial", 10, "bold"), background=theme.COLOR_PRIMARY, foreground=theme.COLOR_WHITE)

        table_container = tk.Frame(rented_frame, bg=theme.COLOR_WHITE)
        table_container.pack(fill="both", expand=True)

        columns = ("No", "Plat Nomor", "Merek", "Tipe", "Warna")
        self.rented_table = ttk.Treeview(table_container, columns=columns, show="headings", style="Dashboard.Treeview", height=6)
        for col in columns:
            self.rented_table.heading(col, text=col)
            self.rented_table.column(col, anchor="center", width=120)
        self.rented_table.column("No", width=40)

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.rented_table.yview)
        self.rented_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.rented_table.pack(side="left", fill="both", expand=True)

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

        for item in self.rented_table.get_children():
            self.rented_table.delete(item)
        rented_cars = get_rented_cars()
        for i, car in enumerate(rented_cars, 1):
            self.rented_table.insert("", "end", values=(i, car["plate_number"], car["brand"], car["type"], car["color"] or "-"))
