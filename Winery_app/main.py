import  tkinter as tk
import atexit

from login import create_login_frame, on_exit


def main():
    root = tk.Tk()
    root.configure(bg = "#202020")
    icon = tk.PhotoImage(file = "logo.png")
    root.iconphoto(False, icon)
    atexit.register(on_exit)
    # Create login frame within the main window
    create_login_frame(root)
    root.mainloop()


if __name__ == "__main__":
    main()

   
