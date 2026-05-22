import tkinter as tk
import theme
from tkinter import ttk, messagebox
from views.components import PrimaryButton, ActionButton, InputField, FormField, DropdownField
from database.db_helper import get_all_users, add_user, update_user, delete_user

class UserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)

        header_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20, pady=20)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="DATA USER", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, fg=theme.COLOR_DARK).pack(side="left")

        content_frame = tk.Frame(self, bg=theme.COLOR_WHITE, padx=20)
        content_frame.pack(fill="both", expand=True)

        action_frame = tk.Frame(content_frame, bg=theme.COLOR_WHITE)
        action_frame.pack(fill="x", pady=(0, 15))

        search_container = tk.Frame(action_frame, bg=theme.COLOR_WHITE)
        search_container.pack(side="left")
        tk.Label(search_container, text="Cari :", font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE).pack(side="left")
        self.ent_search = InputField(search_container, width=25)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg="white", relief="flat", command=self.do_search).pack(side="left")

        self.btn_delete = ActionButton(action_frame, text="HAPUS", color=theme.COLOR_DANGER, command=self.do_delete)
        self.btn_delete.pack(side="right", padx=5)

        self.btn_edit = ActionButton(action_frame, text="EDIT", color=theme.COLOR_INFO, command=self.do_edit)
        self.btn_edit.pack(side="right", padx=5)

        PrimaryButton(action_frame, text="+ TAMBAH", command=self.do_add).pack(side="right", padx=5)

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

        self._user_ids = []

    def on_row_select(self, event):
        selected = self.table.selection()
        is_active = True if selected else False
        self.btn_edit.update_style(is_active)
        self.btn_delete.update_style(is_active)

    def refresh_data(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self._user_ids = []
        rows = get_all_users()
        for i, r in enumerate(rows, 1):
            self._user_ids.append(r["id"])
            self.table.insert("", "end", values=(i, r["name"], r["role"]))
        self.btn_edit.update_style(False)
        self.btn_delete.update_style(False)

    def do_search(self):
        keyword = self.ent_search.get().strip()
        for item in self.table.get_children():
            self.table.delete(item)
        self._user_ids = []
        rows = get_all_users(keyword)
        for i, r in enumerate(rows, 1):
            self._user_ids.append(r["id"])
            self.table.insert("", "end", values=(i, r["name"], r["role"]))

    def do_add(self):
        form = self.controller.views["UserFormView"]
        form.set_mode("add")
        self.controller.show_view("UserFormView")

    def do_edit(self):
        selected = self.table.selection()
        if not selected: return
        idx = self.table.index(selected[0])
        user_id = self._user_ids[idx]
        rows = get_all_users()
        data = None
        for r in rows:
            if r["id"] == user_id:
                data = r
                break
        if data:
            form = self.controller.views["UserFormView"]
            form.set_mode("edit", data)
            self.controller.show_view("UserFormView")

    def do_delete(self):
        selected = self.table.selection()
        if not selected: return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus user ini?"):
            return
        idx = self.table.index(selected[0])
        user_id = self._user_ids[idx]
        try:
            delete_user(user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus: {e}")
            return
        self.refresh_data()

class UserFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)
        self._mode = "add"
        self._edit_id = None

        tk.Label(self, text="Form Data User", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")
        container = tk.Frame(self, bg=theme.COLOR_WHITE)
        container.pack(fill="x", padx=20, pady=10)

        self.f_name     = FormField(container, "Nama :")
        self.f_password = FormField(container, "Password :", show="*")
        self.f_role     = DropdownField(container, "Role :", values=["admin", "petugas"])

        btn_frame = tk.Frame(self, bg=theme.COLOR_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=30)
        
        PrimaryButton(btn_frame, "SIMPAN", command=self.do_save).pack(side="right", padx=10)
        tk.Button(btn_frame, text="KEMBALI", font=theme.FONT_SMALL, bg=theme.COLOR_GRAY, fg="white", relief="flat", padx=20, pady=10, command=lambda: self.controller.show_view("UserView")).pack(side="right", padx=10)

    def set_mode(self, mode, data=None):
        self._mode = mode
        self._edit_id = None
        self.f_name.clear()
        self.f_password.clear()
        self.f_role.clear()
        if mode == "edit" and data:
            self._edit_id = data["id"]
            self.f_name.set(data["name"])
            self.f_role.set(data["role"])

    def do_save(self):
        name = self.f_name.get().strip()
        password = self.f_password.get().strip()
        role = self.f_role.get().strip()
        if not name or not role:
            messagebox.showwarning("Peringatan", "Nama dan Role wajib diisi!")
            return
        if self._mode == "add" and not password:
            messagebox.showwarning("Peringatan", "Password wajib diisi untuk user baru!")
            return
        try:
            if self._mode == "edit" and self._edit_id:
                update_user(self._edit_id, name, password, role)
            else:
                add_user(name, password, role)
            messagebox.showinfo("Sukses", "Data user berhasil disimpan!")
            self.controller.show_view("UserView")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")
