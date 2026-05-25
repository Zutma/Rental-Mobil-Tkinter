import tkinter as tk
import theme
from tkinter import ttk, messagebox
from views.components import PrimaryButton, ActionButton, InputField, FormField, DropdownField
from database.car import get_all_cars, add_car, update_car, delete_car
from database.brand import get_brands, add_brand
from database.car_type import get_types_by_brand, add_type

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
        tk.Button(search_container, text="🔍", font=theme.FONT_NORMAL, bg=theme.COLOR_PRIMARY, fg="white", relief="flat", command=self.do_search).pack(side="left")

        self.btn_delete = ActionButton(action_frame, text="HAPUS", color=theme.COLOR_DANGER, command=self.do_delete)
        self.btn_delete.pack(side="right", padx=5)

        self.btn_edit = ActionButton(action_frame, text="EDIT", color=theme.COLOR_INFO, command=self.do_edit)
        self.btn_edit.pack(side="right", padx=5)

        self.btn_add = PrimaryButton(action_frame, text="+ TAMBAH", command=self.do_add)
        self.btn_add.pack(side="right", padx=5)

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

        self._car_ids = []

    def on_row_select(self, event):
        selected = self.table.selection()
        is_active = True if selected else False
        self.btn_edit.update_style(is_active)
        self.btn_delete.update_style(is_active)

    def setup_role(self, role):
        self.btn_add.pack_forget()
        self.btn_edit.pack_forget()
        self.btn_delete.pack_forget()
        if role == "admin":
            self.btn_delete.pack(side="right", padx=5)
            self.btn_edit.pack(side="right", padx=5)
            self.btn_add.pack(side="right", padx=5)

    def refresh_data(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self._car_ids = []
        rows = get_all_cars()
        for i, r in enumerate(rows, 1):
            self._car_ids.append(r["id"])
            price = f"{r['rental_price']:,.0f}" if r["rental_price"] else "0"
            self.table.insert("", "end", values=(i, r["plate_number"], r["brand"], r["type"], r["color"], r["year"], price, r["status"]))
        self.btn_edit.update_style(False)
        self.btn_delete.update_style(False)

    def do_search(self):
        keyword = self.ent_search.get().strip()
        for item in self.table.get_children():
            self.table.delete(item)
        self._car_ids = []
        rows = get_all_cars(keyword)
        for i, r in enumerate(rows, 1):
            self._car_ids.append(r["id"])
            price = f"{r['rental_price']:,.0f}" if r["rental_price"] else "0"
            self.table.insert("", "end", values=(i, r["plate_number"], r["brand"], r["type"], r["color"], r["year"], price, r["status"]))

    def do_add(self):
        form = self.controller.views["CarFormView"]
        form.set_mode("add")
        self.controller.show_view("CarFormView")

    def do_edit(self):
        selected = self.table.selection()
        if not selected: return
        idx = self.table.index(selected[0])
        car_id = self._car_ids[idx]
        rows = get_all_cars()
        car_data = None
        for r in rows:
            if r["id"] == car_id:
                car_data = r
                break
        if car_data:
            form = self.controller.views["CarFormView"]
            form.set_mode("edit", car_data)
            self.controller.show_view("CarFormView")

    def do_delete(self):
        selected = self.table.selection()
        if not selected: return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data mobil ini?"):
            return
        idx = self.table.index(selected[0])
        car_id = self._car_ids[idx]
        try:
            delete_car(car_id)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus: {e}")
            return
        self.refresh_data()

class CarFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)
        self._mode = "add"
        self._edit_id = None

        tk.Label(self, text="Form Data Mobil", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")
        container = tk.Frame(self, bg=theme.COLOR_WHITE)
        container.pack(fill="x", padx=20, pady=10)

        self.f_plat     = FormField(container, "Plat Nomor :")
        self.f_merek    = DropdownField(container, "Merek :")
        self.f_tipe     = DropdownField(container, "Tipe :")
        self.f_warna    = FormField(container, "Warna :")
        self.f_tahun    = FormField(container, "Tahun :")
        self.f_harga    = FormField(container, "Harga Sewa :")
        self.f_status   = DropdownField(container, "Status :", values=["available", "rented", "maintenance"])

        self.f_merek.bind("<<ComboboxSelected>>", self._on_brand_change)

        btn_frame = tk.Frame(self, bg=theme.COLOR_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=30)
        
        PrimaryButton(btn_frame,"SIMPAN", command=self.do_save).pack(side="right", padx=10)
        tk.Button(btn_frame, text="KEMBALI", font=theme.FONT_SMALL, bg=theme.COLOR_GRAY, fg="white", relief="flat", padx=20, pady=10, command=lambda: self.controller.show_view("CarView")).pack(side="right", padx=10)

    def _load_brands(self):
        brands = get_brands()
        names = [b["name"] for b in brands]
        mapping = {b["name"]: b["id"] for b in brands}
        self.f_merek.set_values(names, mapping)

    def _on_brand_change(self, event=None):
        brand_id = self.f_merek.get_id()
        if brand_id:
            types = get_types_by_brand(brand_id)
            names = [t["name"] for t in types]
            mapping = {t["name"]: t["id"] for t in types}
            self.f_tipe.set_values(names, mapping)

    def set_mode(self, mode, data=None):
        self._mode = mode
        self._edit_id = None
        self.f_plat.clear()
        self.f_merek.clear()
        self.f_tipe.clear()
        self.f_warna.clear()
        self.f_tahun.clear()
        self.f_harga.clear()
        self.f_status.clear()
        self._load_brands()

        if mode == "edit" and data:
            self._edit_id = data["id"]
            self.f_plat.set(data["plate_number"])
            self.f_merek.set(data["brand"])
            self._on_brand_change()
            self.f_tipe.set(data["type"])
            self.f_warna.set(data["color"] or "")
            self.f_tahun.set(data["year"] or "")
            self.f_harga.set(str(data["rental_price"] or ""))
            self.f_status.set(data["status"] or "available")

    def do_save(self):
        plat = self.f_plat.get().strip()
        merek_name = self.f_merek.get().strip()
        tipe_name = self.f_tipe.get().strip()
        warna = self.f_warna.get().strip()
        tahun = self.f_tahun.get().strip()
        harga = self.f_harga.get().strip()
        status = self.f_status.get().strip()

        if not plat or not merek_name or not tipe_name:
            messagebox.showwarning("Peringatan", "Plat Nomor, Merek, dan Tipe wajib diisi!")
            return

        brand_id = self.f_merek.get_id()
        if not brand_id:
            brand_id = add_brand(merek_name)
            self._load_brands()
            self.f_merek.set(merek_name)

        type_id = self.f_tipe.get_id()
        if not type_id:
            type_id = add_type(brand_id, tipe_name)
            self._on_brand_change()
            self.f_tipe.set(tipe_name)

        try:
            tahun_val = int(tahun) if tahun else None
            harga_val = float(harga) if harga else 0
        except ValueError:
            messagebox.showwarning("Peringatan", "Tahun harus angka, Harga harus angka!")
            return

        try:
            if self._mode == "edit" and self._edit_id:
                update_car(self._edit_id, type_id, plat, warna, tahun_val, harga_val, status or "available")
            else:
                add_car(type_id, plat, warna, tahun_val, harga_val, status or "available")
            messagebox.showinfo("Sukses", "Data mobil berhasil disimpan!")
            self.controller.show_view("CarView")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")
