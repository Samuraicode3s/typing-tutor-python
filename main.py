import customtkinter as ctk
from ui.main_app import MainApp

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
