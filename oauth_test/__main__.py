import PIL.ImageTk
import PIL.Image
from tkinter import *


def main():
    # start app
    root = Tk()
    img = PIL.ImageTk.PhotoImage(PIL.Image.open("unnamed.jpg"))
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


if __name__ == "__main__":
    main()

