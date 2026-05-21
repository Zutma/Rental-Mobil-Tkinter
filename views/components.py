import theme
import tkinter as tk

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
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)
    def clear(self): self.entry.delete(0, tk.END)
