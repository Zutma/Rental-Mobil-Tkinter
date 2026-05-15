import theme
import tkinter as tk

class PrimaryButton(tk.Button):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent, 
            text=text.upper(), 
            command=command, 
            bg=theme.COLOR_PRIMARY, 
            fg=theme.COLOR_WHITE, 
            font=theme.FONT_MEDIUM, 
            relief="flat", 
            cursor="hand2", 
            padx=20, 
            pady=10, 
            **kwargs
        )

class TitleLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(
            parent, 
            text=text, 
            font=theme.FONT_LARGE, 
            # bg=theme.COLOR_PRIMARY, 
            # fg=theme.COLOR_WHITE, 
            **kwargs
        )

class InputField(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=theme.FONT_NORMAL,
            relief="flat",
            bg=theme.COLOR_WHITE,
            fg=theme.COLOR_DARK,
            highlightthickness=1,
            highlightbackground=theme.COLOR_GRAY,
            highlightcolor=theme.COLOR_PRIMARY,
            **kwargs
        )
