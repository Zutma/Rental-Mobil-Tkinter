import tkinter as tk
import theme

class InfoCard(tk.Frame):
    def __init__(self, parent, title, value, color):
        super().__init__(parent, bg=color, height=150) 
        self.pack_propagate(False) 
        
        # Label Atas: Diberi padding atas (pady) yang cukup besar (45) agar teks turun ke tengah kotak
        tk.Label(
            self, 
            text=title.upper(), 
            font=theme.FONT_TITLE, 
            bg=color, 
            fg="white"
        ).pack(anchor="w", padx=30, pady=(45, 0)) # anchor="w" PASTI rata kiri
        
        # Label Bawah: Diberi padding bawah agar seimbang
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

        tk.Label(
            self, 
            text="Selamat Datang, Admin", 
            font=theme.FONT_TITLE, 
            bg=theme.COLOR_WHITE, 
            fg=theme.COLOR_DARK,
            padx=30
        ).pack(anchor="w", pady=(40, 20))

        # GRID 2x2
        stats_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20)
        stats_frame.pack(fill="x")
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        InfoCard(stats_frame, "Jumlah Mobil", "12", theme.COLOR_INFO).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        InfoCard(stats_frame, "Jumlah Pelanggan", "45", theme.COLOR_SUCCESS).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        InfoCard(stats_frame, "Jumlah Pesanan", "8", theme.COLOR_PRIMARY).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        InfoCard(stats_frame, "Jumlah User", "5", theme.COLOR_DANGER).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Frame(self, bg=theme.COLOR_WHITE, height=30).pack()