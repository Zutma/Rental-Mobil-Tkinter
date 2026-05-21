import tkinter as tk
import theme
from tkinter import ttk
from views.components import InputField, FormField

class UserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        # Header
        tk.Label(self, text="DATA USER", font=("Arial", 18, "bold"), bg=theme.COLOR_WHITE, fg=theme.COLOR_DARK, anchor="w", padx=20, pady=20).pack(fill="x")

        # Content Frame
        content_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20)
        content_frame.pack(fill="both", expand=True)

        # Action Frame
        action_frame = tk.Frame(content_frame, bg=theme.COLOR_WHITE)
        action_frame.pack(fill="x", pady=(0, 15))

        search_container = tk.Frame(action_frame, bg=theme.COLOR_WHITE)
        search_container.pack(side="left")

        tk.Label(search_container, text="Cari :", font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE).pack(side="left")
        self.ent_search = InputField(search_container, width=25)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg="white", relief="flat").pack(side="left")

        # Buttons (Sesuai Gaya Mobil/Pelanggan/Transaksi)
        btn_add = tk.Button(
            action_frame, text="+ TAMBAH", 
            font=("Arial", 10, "bold"), bg=theme.COLOR_PRIMARY, fg="white", 
            relief="flat", padx=15, pady=8,
            command=lambda: self.controller.show_view("UserFormView")
        )
        btn_add.pack(side="right", padx=5)

        self.btn_edit = tk.Button(
            action_frame, text="EDIT", 
            font=("Arial", 10, "bold"), bg=theme.COLOR_INFO, fg="white", 
            relief="flat", padx=15, pady=8, state="disabled",
            command=lambda: self.controller.show_view("UserFormView")
        )
        self.btn_edit.pack(side="right", padx=5)

        self.btn_delete = tk.Button(
            action_frame, text="HAPUS", 
            font=("Arial", 10, "bold"), bg=theme.COLOR_DANGER, fg="white", 
            relief="flat", padx=15, pady=8, state="disabled"
        )
        self.btn_delete.pack(side="right", padx=5)

        # Table Frame
        table_frame = tk.Frame(content_frame, bg=theme.COLOR_WHITE)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = ("No", "Username", "Role")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")
        
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

class UserFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        tk.Label(self, text="Form Data User", font=theme.FONT_MEDIUM, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")
        container = tk.Frame(self, bg=theme.COLOR_WHITE)
        container.pack(fill="x", padx=20, pady=10)

        self.f_name     = FormField(container, "Nama :")
        self.f_password = FormField(container, "Password :", show="*")
        self.f_role     = FormField(container, "Role :")

        btn_frame = tk.Frame(self, bg=theme.COLOR_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=30)
        
        # Tombol Simpan & Kembali
        tk.Button(btn_frame, text="SIMPAN", font=("Arial", 10, "bold"), bg=theme.COLOR_PRIMARY, fg="white", relief="flat", padx=20, pady=10, 
                  command=lambda: self.controller.show_view("UserView")).pack(side="right", padx=10)
        tk.Button(btn_frame, text="KEMBALI", font=("Arial", 10, "bold"), bg=theme.COLOR_GRAY, fg="white", relief="flat", padx=20, pady=10, 
                  command=lambda: self.controller.show_view("UserView")).pack(side="right", padx=10)
