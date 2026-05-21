import tkinter as tk
import theme
from tkinter import ttk
from views.components import PrimaryButton, ActionButton, InputField

class CarView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        header_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="DATA MOBIL", font=theme.FONT_TITLE, bg="white", fg=theme.COLOR_DARK).pack(side="left")

        content_frame = tk.Frame(self, bg="white", padx=20)
        content_frame.pack(fill="both", expand=True)

        action_frame = tk.Frame(content_frame, bg="white")
        action_frame.pack(fill="x", pady=(0, 15))

        search_container = tk.Frame(action_frame, bg="white")
        search_container.pack(side="left")
        tk.Label(search_container, text="Cari :", font=theme.FONT_NORMAL, bg="white").pack(side="left")
        self.ent_search = InputField(search_container, width=25)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg="white", relief="flat").pack(side="left")

        # Menggunakan ActionButton
        self.btn_delete = ActionButton(action_frame, text="HAPUS", color=theme.COLOR_DANGER)
        self.btn_delete.pack(side="right", padx=5)

        self.btn_edit = ActionButton(action_frame, text="EDIT", color=theme.COLOR_INFO, command=lambda: self.controller.show_view("CarFormView"))
        self.btn_edit.pack(side="right", padx=5)

        PrimaryButton(action_frame, text="+ TAMBAH", command=lambda: self.controller.show_view("CarFormView")).pack(side="right", padx=5)

        table_frame = tk.Frame(content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = ("No", "Plat Nomor", "Merek", "Tipe", "Warna", "Tahun", "Harga Sewa", "Status")
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
        is_active = True if selected else False
        self.btn_edit.update_style(is_active)
        self.btn_delete.update_style(is_active)

class CarFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)
        tk.Label(self, text="Form Data Mobil", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")