from tkinter import *


def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="green")


root = Tk()
cv = Canvas(root, width=600, height=250)
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

mainloop()
