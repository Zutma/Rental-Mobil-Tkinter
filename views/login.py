import theme
import tkinter as tk
from tkinter import messagebox
from views.components import *
from database.db_helper import authenticate

class LoginPage(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg=theme.COLOR_PRIMARY)

        self.card = tk.Frame(self, bg=theme.COLOR_WHITE, )
        self.card.place(relx=0.5,rely=0,relwidth=0.5,relheight=1.0)

        tk.Label(self.card, text="Rental Mobil", bg=theme.COLOR_WHITE, font=theme.FONT_LOGIN_TITLE).pack(side="top",pady=(70,0))

        self.form_container = tk.Frame(self.card, bg=theme.COLOR_WHITE)
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.form_container, text="Username", bg=theme.COLOR_WHITE, font=theme.FONT_LOGIN_LABEL).pack(pady=(10,0),anchor="w")
        self.ent_user = InputField(self.form_container,width=35)
        self.ent_user.pack(fill="x", pady=(5, 15), ipady=10, ipadx=5)
 
        tk.Label(self.form_container, text="Password", bg=theme.COLOR_WHITE, font=theme.FONT_LOGIN_LABEL).pack(pady=(10,0),anchor="w")
        self.ent_pass = InputField(self.form_container, show="*", width=35)
        self.ent_pass.pack(fill="x", pady=(5, 30), ipady=10, ipadx=5)

        PrimaryButton(
            self.form_container, 
            text="LOGIN", 
            command=self.do_login, 
            width=35,
            font=theme.FONT_LOGIN_LABEL,
            pady=10 
        ).pack(pady=20)

        self.ent_user.bind("<Return>", lambda e: self.do_login())
        self.ent_pass.bind("<Return>", lambda e: self.do_login())

    def do_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password harus diisi!")
            return
        user = authenticate(username, password)
        if user:
            self.controller.current_user = user
            self.ent_user.delete(0, tk.END)
            self.ent_pass.delete(0, tk.END)
            self.controller.show_page("MainLayout")
        else:
            messagebox.showerror("Gagal", "Username atau Password salah!")