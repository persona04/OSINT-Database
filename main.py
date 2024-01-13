import customtkinter as ctk
import tkinter as tk
from gui import *


# Main window's configration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
window = ctk.CTk()
WIDTH = window.winfo_screenwidth()
HEIGHT = window.winfo_screenheight()
screen_size = (WIDTH,HEIGHT)
window.geometry(f"{WIDTH}x{HEIGHT}+0+0")
window.title("OSINT-Database")

LoginPage(window,screen_size=screen_size)

window.mainloop()