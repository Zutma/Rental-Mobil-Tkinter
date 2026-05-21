import tkinter as tk
import theme
from tkinter import ttk
from views.components import PrimaryButton, InputField

class TransactionView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # 1. HEADER
        header_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="DATA TRANSAKSI", font=("Arial", 18, "bold"), bg="white", fg=theme.COLOR_DARK).pack(side="left")

        # 2. CONTENT AREA
        content_frame = tk.Frame(self, bg="white", padx=20)
        content_frame.pack(fill="both", expand=True)

        # 2.a. Action Frame
        action_frame = tk.Frame(content_frame, bg="white")
        action_frame.pack(fill="x", pady=(0, 15))

        search_container = tk.Frame(action_frame, bg="white")
        search_container.pack(side="left")

        tk.Label(search_container, text="Cari :", font=theme.FONT_NORMAL, bg="white").pack(side="left")
        self.ent_search = InputField(search_container, width=25)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg="white", relief="flat").pack(side="left")

        # Buttons
        btn_add = tk.Button(action_frame, text="+ TAMBAH", font=("Arial", 10, "bold"), bg=theme.COLOR_PRIMARY, fg="white", relief="flat", padx=15, pady=8)
        btn_add.pack(side="right", padx=5)

        self.btn_edit = tk.Button(action_frame, text="EDIT", font=("Arial", 10, "bold"), bg=theme.COLOR_INFO, fg="white", relief="flat", padx=15, pady=8, state="disabled")
        self.btn_edit.pack(side="right", padx=5)

        self.btn_delete = tk.Button(action_frame, text="HAPUS", font=("Arial", 10, "bold"), bg=theme.COLOR_DANGER, fg="white", relief="flat", padx=15, pady=8, state="disabled")
        self.btn_delete.pack(side="right", padx=5)

        # 2.b. Table Frame
        table_frame = tk.Frame(content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = ("No", "Pelanggan", "Mobil", "Tgl. Pinjam", "Tgl. Kembali", "Jaminan", "Total Harga", "Status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=100)
        
        self.table.column("No", width=40)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

    def on_row_select(self, event):
        selected = self.table.selection()
        state = "normal" if selected else "disabled"
        self.btn_edit.config(state=state)
        self.btn_delete.config(state=state)