import customtkinter as ctk
from src.ui.main_window import PyVersionerApp

__version__ = "1.0.0"


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = PyVersionerApp(version=__version__)
    app.mainloop()

if __name__ == "__main__":
    main()
 