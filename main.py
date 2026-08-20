import customtkinter as ctk

from ui.main_window import MainWindow


def main():
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
