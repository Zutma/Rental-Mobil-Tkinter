import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="#F47B2E")

        label = tk.Label(self, text="halaman login", font=("arial",20,"bold"), bg="#F47B2E", fg="white")
        label.pack(expand=True)