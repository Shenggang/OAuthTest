from tkinter import *

import app


def main():
    # start app
    root = Tk()
    app.MainWindow(root)
    root.geometry('800x400')
    root.mainloop()


if __name__ == "__main__":
    main()
