import tkinter as tk
import theme
from tkinter import ttk, messagebox
from views.components import PrimaryButton, ActionButton, InputField, FormField
from database.brand import get_brands, add_brand, update_brand, delete_brand

class BrandView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        header_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20, pady=20)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="DATA MEREK", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, fg=theme.COLOR_DARK).pack(side="left")

        content_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20)
        content_frame.pack(fill="both", expand=True)

        action_frame = tk.Frame(content_frame, bg=theme.COLOR_WHITE)
        action_frame.pack(fill="x", pady=(0, 15))

        search_container = tk.Frame(action_frame, bg=theme.COLOR_WHITE)
        search_container.pack(side="left")
        tk.Label(search_container, text="Cari :", font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE).pack(side="left")
        self.ent_search = InputField(search_container, width=25)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg=theme.COLOR_WHITE, relief="flat", command=self.do_search).pack(side="left")

        self.btn_delete = ActionButton(action_frame, text="HAPUS", color=theme.COLOR_DANGER, command=self.do_delete)
        self.btn_delete.pack(side="right", padx=5)

        self.btn_edit = ActionButton(action_frame, text="EDIT", color=theme.COLOR_INFO, command=self.do_edit)
        self.btn_edit.pack(side="right", padx=5)

        PrimaryButton(action_frame, text="+ TAMBAH", command=self.do_add).pack(side="right", padx=5)

        table_frame = tk.Frame(content_frame, bg=theme.COLOR_WHITE)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = ("No", "Nama Merek")
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

        self._brand_ids = []

    def on_row_select(self, event):
        selected = self.table.selection()
        is_active = True if selected else False
        self.btn_edit.update_style(is_active)
        self.btn_delete.update_style(is_active)

    def refresh_data(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self._brand_ids = []
        rows = get_brands()
        
        self.table.tag_configure('oddrow', background=theme.COLOR_WHITE)
        self.table.tag_configure('evenrow', background=theme.COLOR_GRAY)

        for i, r in enumerate(rows, 1):
            self._brand_ids.append(r["id"])
            
            row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.table.insert("", "end", values=(i, r["name"]), tags=(row_tag,))
            
        self.btn_edit.update_style(False)
        self.btn_delete.update_style(False)

    def do_search(self):
        keyword = self.ent_search.get().strip()
        for item in self.table.get_children():
            self.table.delete(item)
        self._brand_ids = []
        rows = get_brands(keyword)
        
        self.table.tag_configure('oddrow', background=theme.COLOR_WHITE)
        self.table.tag_configure('evenrow', background=theme.COLOR_GRAY)

        for i, r in enumerate(rows, 1):
            self._brand_ids.append(r["id"])
            
            row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.table.insert("", "end", values=(i, r["name"]), tags=(row_tag,))

    def do_add(self):
        form = self.controller.views["BrandFormView"]
        form.set_mode("add")
        self.controller.show_view("BrandFormView")

    def do_edit(self):
        selected = self.table.selection()
        if not selected: return
        idx = self.table.index(selected[0])
        brand_id = self._brand_ids[idx]
        rows = get_brands()
        data = None
        for r in rows:
            if r["id"] == brand_id:
                data = r
                break
        if data:
            form = self.controller.views["BrandFormView"]
            form.set_mode("edit", data)
            self.controller.show_view("BrandFormView")

    def do_delete(self):
        selected = self.table.selection()
        if not selected: return
        if not messagebox.askyesno("Konfirmasi", "Menghapus merek akan menghapus semua tipe & mobil terkait.\nYakin ingin menghapus?"):
            return
        idx = self.table.index(selected[0])
        brand_id = self._brand_ids[idx]
        try:
            delete_brand(brand_id)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus: {e}")
            return
        self.refresh_data()

class BrandFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)
        self._mode = "add"
        self._edit_id = None

        tk.Label(self, text="Form Data Merek", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")
        container = tk.Frame(self, bg=theme.COLOR_WHITE)
        container.pack(fill="x", padx=20, pady=10)

        self.f_name = FormField(container, "Nama Merek :")

        btn_frame = tk.Frame(self, bg=theme.COLOR_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=30)

        PrimaryButton(btn_frame, "SIMPAN", command=self.do_save).pack(side="right", padx=10)
        tk.Button(btn_frame, text="KEMBALI", font=theme.FONT_SMALL, bg=theme.COLOR_GRAY, fg=theme.COLOR_WHITE, relief="flat", padx=20, pady=10, command=lambda: self.controller.show_view("BrandView")).pack(side="right", padx=10)

    def set_mode(self, mode, data=None):
        self._mode = mode
        self._edit_id = None
        self.f_name.clear()
        if mode == "edit" and data:
            self._edit_id = data["id"]
            self.f_name.set(data["name"])

    def do_save(self):
        name = self.f_name.get().strip()
        if not name:
            messagebox.showwarning("Peringatan", "Nama Merek wajib diisi!")
            return
        try:
            if self._mode == "edit" and self._edit_id:
                update_brand(self._edit_id, name)
            else:
                add_brand(name)
            messagebox.showinfo("Sukses", "Data merek berhasil disimpan!")
            self.controller.show_view("BrandView")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")