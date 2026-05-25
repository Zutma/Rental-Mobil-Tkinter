import tkinter as tk
import theme
from datetime import date, datetime
from tkinter import ttk, messagebox
from views.components import PrimaryButton, ActionButton, InputField, FormField, DropdownField, DateField
from database.transaction import get_all_transactions, add_transaction, update_transaction, delete_transaction,  get_available_cars, get_car_by_id
from database.customer import get_all_customers
from database.car import update_car_status

class TransactionView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Set tema clam untuk mengaktifkan grid pada treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=theme.COLOR_PRIMARY, foreground="white")

        header_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="DATA TRANSAKSI", font=theme.FONT_TITLE, bg="white", fg=theme.COLOR_DARK).pack(side="left")

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

        PrimaryButton(action_frame, text="+ TAMBAH", command=self.do_add).pack(side="right", padx=5)

        table_frame = tk.Frame(content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        columns = ("No", "Pelanggan", "Mobil", "Tgl. Pinjam", "Tgl. Kembali", "Jaminan", "Total Harga", "Status", "Metode Bayar")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=100)
        self.table.column("No", width=40)
        
        self.table.tag_configure("evenrow", background="#f9f9f9")
        self.table.tag_configure("oddrow", background="#ffffff")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

        self._trans_ids = []
        self._trans_data = []

    def on_row_select(self, event):
        selected = self.table.selection()
        is_active = True if selected else False
        self.btn_edit.update_style(is_active)
        self.btn_delete.update_style(is_active)

    def refresh_data(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self._trans_ids = []
        self._trans_data = []
        rows = get_all_transactions()
        for i, r in enumerate(rows, 1):
            self._trans_ids.append(r["id"])
            self._trans_data.append(r)
            price = f"{r['total_price']:,.0f}" if r["total_price"] else "0"
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.table.insert("", "end", values=(
                i, r["customer_name"], r["car_label"],
                str(r["pickup_date"] or ""), str(r["return_date"] or ""),
                r["guarantee_item"] or "", price, r["status"], r.get("payment_method", "-")
            ), tags=(tag,))
        self.btn_edit.update_style(False)
        self.btn_delete.update_style(False)

    def do_search(self):
        keyword = self.ent_search.get().strip()
        for item in self.table.get_children():
            self.table.delete(item)
        self._trans_ids = []
        self._trans_data = []
        rows = get_all_transactions(keyword)
        for i, r in enumerate(rows, 1):
            self._trans_ids.append(r["id"])
            self._trans_data.append(r)
            price = f"{r['total_price']:,.0f}" if r["total_price"] else "0"
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.table.insert("", "end", values=(
                i, r["customer_name"], r["car_label"],
                str(r["pickup_date"] or ""), str(r["return_date"] or ""),
                r["guarantee_item"] or "", price, r["status"], r.get("payment_method", "-")
            ), tags=(tag,))

    def do_add(self):
        form = self.controller.views["TransactionFormView"]
        form.set_mode("add")
        self.controller.show_view("TransactionFormView")

    def do_edit(self):
        selected = self.table.selection()
        if not selected: return
        idx = self.table.index(selected[0])
        data = self._trans_data[idx]
        form = self.controller.views["TransactionFormView"]
        form.set_mode("edit", data)
        self.controller.show_view("TransactionFormView")

    def do_delete(self):
        selected = self.table.selection()
        if not selected: return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data transaksi ini?"):
            return
        idx = self.table.index(selected[0])
        trans_id = self._trans_ids[idx]
        data = self._trans_data[idx]
        try:
            delete_transaction(trans_id)
            update_car_status(data["car_id"], "available")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus: {e}")
            return
        self.refresh_data()

class TransactionFormView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=theme.COLOR_WHITE)
        self._mode = "add"
        self._edit_id = None
        self._old_car_id = None
        self._car_prices = {}

        tk.Label(self, text="Form Data Transaksi", font=theme.FONT_TITLE, bg=theme.COLOR_WHITE, anchor="w", padx=20, pady=20).pack(fill="x")
        container = tk.Frame(self, bg=theme.COLOR_WHITE)
        container.pack(fill="x", padx=20, pady=10)

        self.f_pelanggan = DropdownField(container, "Pelanggan :")
        self.f_mobil     = DropdownField(container, "Mobil :")
        self.f_pinjam    = DateField(container, "Tgl. Pinjam :")
        self.f_kembali   = DateField(container, "Tgl. Kembali :")
        self.f_jaminan   = FormField(container, "Jaminan :")
        self.f_total     = FormField(container, "Total Harga :")
        self.f_pembayaran= DropdownField(container, "Metode Bayar :", values=["Cash", "Transfer"])
        self.f_status    = DropdownField(container, "Status :", values=["booked", "on_going", "finished", "cancelled"])

        # Buat field total harga readonly karena akan dihitung otomatis
        self.f_total.set_readonly(True)

        self.f_pinjam.bind("<<DateEntrySelected>>", self._on_date_or_car_change)
        self.f_kembali.bind("<<DateEntrySelected>>", self._on_date_or_car_change)
        self.f_mobil.bind("<<ComboboxSelected>>", self._on_date_or_car_change)

        btn_frame = tk.Frame(self, bg=theme.COLOR_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=30)
        
        PrimaryButton(btn_frame, "SIMPAN", command=self.do_save).pack(side="right", padx=10)
        tk.Button(btn_frame, text="KEMBALI", font=theme.FONT_SMALL, bg=theme.COLOR_GRAY, fg="white", relief="flat", padx=20, pady=10, command=lambda: self.controller.show_view("TransactionView")).pack(side="right", padx=10)

    def _calculate_total(self):
        car_id = self.f_mobil.get_id()
        if not car_id:
            self.f_total.set("0")
            return
            
        try:
            pickup = self.f_pinjam.entry.get_date()
            ret = self.f_kembali.entry.get_date()
            delta = (ret - pickup).days
            days = max(1, delta) # Minimal hitung 1 hari
            
            car_price = self._car_prices.get(car_id, 0)
            total = days * car_price
            
            # Format angkanya saja ke form (agar tersimpan dengan benar di DB)
            self.f_total.set(str(int(total)))
        except:
            self.f_total.set("0")

    def _on_date_or_car_change(self, event=None):
        try:
            pickup = self.f_pinjam.entry.get_date()
            self.f_kembali.set_mindate(pickup)
            try:
                ret = self.f_kembali.entry.get_date()
                if ret < pickup:
                    self.f_kembali.entry.set_date(pickup)
            except:
                pass
        except:
            pass
            
        self._calculate_total()

    def _load_dropdowns(self, include_car_id=None):
        customers = get_all_customers()
        cust_names = [c["name"] for c in customers]
        cust_map = {c["name"]: c["id"] for c in customers}
        self.f_pelanggan.set_values(cust_names, cust_map)

        cars = get_available_cars()
        if include_car_id:
            existing_ids = [c["id"] for c in cars]
            if include_car_id not in existing_ids:
                extra = get_car_by_id(include_car_id)
                if extra:
                    cars.append(extra)
                    
        self._car_prices = {c["id"]: c["rental_price"] for c in cars}
        car_labels = [c["label"] for c in cars]
        car_map = {c["label"]: c["id"] for c in cars}
        self.f_mobil.set_values(car_labels, car_map)

    def set_mode(self, mode, data=None):
        self._mode = mode
        self._edit_id = None
        self._old_car_id = None
        self.f_pelanggan.clear()
        self.f_mobil.clear()
        self.f_pinjam.clear()
        self.f_kembali.clear()
        self.f_jaminan.clear()
        self.f_total.set("0")
        self.f_pembayaran.clear()
        self.f_status.clear()

        if mode == "add":
            self._load_dropdowns()
            today = date.today()
            self.f_pinjam.set_mindate(today)
            self.f_kembali.set_mindate(today)
            self.f_pinjam.set(today)
            self.f_kembali.set(today)
            self.f_pembayaran.set("Cash")
            self.f_status.set("on_going")
        elif mode == "edit" and data:
            self._edit_id = data["id"]
            self._old_car_id = data.get("car_id")
            self._load_dropdowns(include_car_id=data.get("car_id"))

            pickup_val = data["pickup_date"]
            if pickup_val:
                if isinstance(pickup_val, str):
                    pickup_val = datetime.strptime(str(pickup_val), "%Y-%m-%d").date()
                self.f_pinjam.clear_mindate()
                self.f_kembali.clear_mindate()

            self.f_pelanggan.set(data["customer_name"])
            self.f_mobil.set(data["car_label"])
            self.f_pinjam.set(str(data["pickup_date"] or ""))
            self.f_kembali.set(str(data["return_date"] or ""))
            self.f_jaminan.set(data["guarantee_item"] or "")
            self.f_total.set(str(data["total_price"] or ""))
            self.f_pembayaran.set(data.get("payment_method") or "Cash")
            self.f_status.set(data["status"] or "booked")

    def do_save(self):
        pelanggan = self.f_pelanggan.get().strip()
        mobil = self.f_mobil.get().strip()
        pinjam = self.f_pinjam.get().strip()
        kembali = self.f_kembali.get().strip()
        jaminan = self.f_jaminan.get().strip()
        total = self.f_total.get().strip()
        pembayaran = self.f_pembayaran.get().strip()
        status = self.f_status.get().strip()

        if not pelanggan or not mobil or not pinjam or not kembali:
            messagebox.showwarning("Peringatan", "Pelanggan, Mobil, Tanggal Pinjam & Kembali wajib diisi!")
            return

        cust_id = self.f_pelanggan.get_id()
        car_id = self.f_mobil.get_id()
        if not cust_id or not car_id:
            messagebox.showwarning("Peringatan", "Pelanggan atau Mobil tidak valid!")
            return

        try:
            pinjam_date = datetime.strptime(pinjam, "%Y-%m-%d").date()
            kembali_date = datetime.strptime(kembali, "%Y-%m-%d").date()
            if kembali_date < pinjam_date:
                messagebox.showwarning("Peringatan", "Tanggal kembali tidak boleh sebelum tanggal pinjam!")
                return
        except ValueError:
            messagebox.showwarning("Peringatan", "Format tanggal harus YYYY-MM-DD!")
            return

        try:
            total_val = float(total) if total else 0
        except ValueError:
            messagebox.showwarning("Peringatan", "Total Harga harus angka!")
            return

        if not status:
            status = "on_going"

        try:
            if self._mode == "edit" and self._edit_id:
                if self._old_car_id and self._old_car_id != car_id:
                    update_car_status(self._old_car_id, "available")
                update_transaction(self._edit_id, cust_id, car_id, pinjam, kembali, jaminan, total_val, status, pembayaran)
            else:
                add_transaction(cust_id, car_id, pinjam, kembali, jaminan, total_val, status, pembayaran)

            if status in ("booked", "on_going"):
                update_car_status(car_id, "rented")
            elif status in ("finished", "cancelled"):
                update_car_status(car_id, "available")

            messagebox.showinfo("Sukses", "Data transaksi berhasil disimpan!")
            self.controller.show_view("TransactionView")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")
