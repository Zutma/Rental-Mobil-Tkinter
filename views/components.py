import theme
import tkinter as tk
from tkinter import ttk
from datetime import date as date_cls, datetime as datetime_cls
from tkcalendar import DateEntry

class PrimaryButton(tk.Button):
    def __init__(self, parent, text, command=None, **kwargs):
        params = {
            "text": text.upper(),
            "command": command,
            "bg": theme.COLOR_PRIMARY,
            "fg": theme.COLOR_WHITE,
            "font": theme.FONT_SMALL,
            "relief": "flat",
            "cursor": "hand2",
            "padx": 15,
            "pady": 8
        }
        params.update(kwargs)
        super().__init__(parent, **params)

class ActionButton(tk.Button):
    def __init__(self, parent, text, color, command=None, **kwargs):
        self.active_color = color
        params = {
            "text": text.upper(),
            "command": command,
            "font": theme.FONT_SMALL,
            "relief": "flat",
            "cursor": "hand2",
            "padx": 15,
            "pady": 8
        }
        params.update(kwargs)
        super().__init__(parent, **params)
        self.update_style(False)

    def update_style(self, is_active):
        if is_active:
            self.config(state="normal", bg=self.active_color, fg=theme.COLOR_WHITE)
        else:
            self.config(state="disabled", bg="#E0E0E0", fg="#A0A0A0")

class TitleLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        params = {
            "text": text,
            "font": theme.FONT_TITLE,
            "bg": theme.COLOR_WHITE,
            "fg": theme.COLOR_DARK
        }
        params.update(kwargs)
        super().__init__(parent, **params)

class InputField(tk.Entry):
    def __init__(self, parent, **kwargs):
        params = {
            "font": theme.FONT_NORMAL,
            "relief": "flat",
            "bg": theme.COLOR_WHITE,
            "fg": theme.COLOR_DARK,
            "highlightthickness": 1,
            "highlightbackground": theme.COLOR_GRAY,
            "highlightcolor": theme.COLOR_PRIMARY
        }
        params.update(kwargs)
        super().__init__(parent, **params)

class FormField:
    def __init__(self, parent, label_text, **kwargs):
        self.frame = tk.Frame(parent, bg=theme.COLOR_WHITE)
        self.frame.pack(fill="x", pady=8)
        
        tk.Label(self.frame, text=label_text, font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE, width=15, anchor="w").pack(side="left")
        self.entry = InputField(self.frame, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True, ipady=5)

    def get(self): return self.entry.get()
    
    def set(self, val):
        state = self.entry.cget("state")
        if state in ("readonly", "disabled"):
            self.entry.config(state="normal")
            
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)
        
        if state in ("readonly", "disabled"):
            self.entry.config(state=state)
            
    def clear(self):
        state = self.entry.cget("state")
        if state in ("readonly", "disabled"):
            self.entry.config(state="normal")
            
        self.entry.delete(0, tk.END)
        
        if state in ("readonly", "disabled"):
            self.entry.config(state=state)

    def set_readonly(self, is_readonly=True):
        if is_readonly:
            self.entry.config(state="readonly", bg="#F0F0F0")
        else:
            self.entry.config(state="normal", bg=theme.COLOR_WHITE)

    def set_disabled(self, is_disabled=True):
        """Disable/enable field"""
        if is_disabled:
            self.entry.config(state="disabled", disabledbackground="#F0F0F0", disabledforeground="#999999")
        else:
            self.entry.config(state="normal", bg=theme.COLOR_WHITE)

class DropdownField:
    def __init__(self, parent, label_text, values=None):
        self.frame = tk.Frame(parent, bg=theme.COLOR_WHITE)
        self.frame.pack(fill="x", pady=8)

        tk.Label(self.frame, text=label_text, font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE, width=15, anchor="w").pack(side="left")
        self.var = tk.StringVar()

        style = ttk.Style()
        style.configure("White.TCombobox",
                        fieldbackground=theme.COLOR_WHITE,
                        background=theme.COLOR_WHITE,
                        foreground=theme.COLOR_DARK)

        self.combo = ttk.Combobox(self.frame, textvariable=self.var, font=theme.FONT_NORMAL, state="readonly", style="White.TCombobox")
        if values:
            self.combo["values"] = values
        self.combo.pack(side="left", fill="x", expand=True, ipady=5)
        self._map = {}

    def set_values(self, display_list, map_dict=None):
        self.combo["values"] = display_list
        self._map = map_dict or {}
        self.var.set("")

    def get(self): return self.var.get()
    def get_id(self): return self._map.get(self.var.get())
    def set(self, val): self.var.set(val)
    def clear(self): self.var.set("")
    def bind(self, event, handler): self.combo.bind(event, handler)

    def set_disabled(self, is_disabled=True):
        """Disable/enable dropdown"""
        if is_disabled:
            self.combo.config(state="disabled")
        else:
            self.combo.config(state="readonly")

class DateField:
    def __init__(self, parent, label_text):
        self.frame = tk.Frame(parent, bg=theme.COLOR_WHITE)
        self.frame.pack(fill="x", pady=8)

        tk.Label(self.frame, text=label_text, font=theme.FONT_NORMAL, bg=theme.COLOR_WHITE, width=15, anchor="w").pack(side="left")
        self.entry = DateEntry(self.frame, font=theme.FONT_NORMAL, date_pattern="yyyy-mm-dd",
                               background=theme.COLOR_PRIMARY, foreground=theme.COLOR_WHITE,
                               headersbackground=theme.COLOR_PRIMARY, headersforeground=theme.COLOR_WHITE,
                               selectbackground=theme.COLOR_SECONDARY, selectforeground=theme.COLOR_WHITE,
                               borderwidth=1, width=20)
        self.entry.pack(side="left", fill="x", expand=True, ipady=5)

    def get(self): return self.entry.get()

    def set(self, val):
        if val:
            try:
                if isinstance(val, date_cls):
                    self.entry.set_date(val)
                elif isinstance(val, str) and val:
                    d = datetime_cls.strptime(val, "%Y-%m-%d").date()
                    self.entry.set_date(d)
            except:
                pass

    def clear(self):
        self.entry.set_date(date_cls.today())

    def set_mindate(self, d):
        self.entry.configure(mindate=d)

    def clear_mindate(self):
        self.entry.configure(mindate=None)

    def bind(self, event, handler):
        self.entry.bind(event, handler)

    def set_disabled(self, is_disabled=True):
        """Disable/enable date field"""
        if is_disabled:
            self.entry.config(state="disabled")
        else:
            self.entry.config(state="normal")

class NumberField(FormField):
    def __init__(self, parent, label_text, **kwargs):
        super().__init__(parent, label_text, **kwargs)
        self.entry.bind("<KeyRelease>", self._format_nominal)

    def set(self, val):
        """Format angka secara otomatis saat nilai di-set dari sistem/kode"""
        try:
            val_str = str(val).replace("Rp.", "").replace("Rp", "").replace(".", "").replace(",", "").strip()
            if val_str and val_str != "None":
                nilai = int(float(val_str))
                val = f"Rp. {nilai:,}".replace(",", ".")
        except ValueError:
            pass
        
        super().set(val)

    def _format_nominal(self, event=None):
        try:
            nilai_str = self.entry.get().replace("Rp.", "").replace("Rp", "").replace(".", "").replace(",", "").strip()
            if not nilai_str:
                self.entry.delete(0, tk.END)
                return
            
            nilai = int(float(nilai_str))
            
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"Rp. {nilai:,}".replace(",", "."))
        except ValueError:
            pass

    def get_value(self):
        """Ambil angka bersih (tanpa Rp dan tanpa titik) untuk disimpan ke DB"""
        val = self.entry.get().replace("Rp.", "").replace("Rp", "").replace(".", "").replace(",", "").strip()
        return val if val else "0"
