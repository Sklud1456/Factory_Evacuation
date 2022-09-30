from tkinter import *
import tkinter as tk


#
#
# root = Tk()
# cv = Canvas(root, width=1000, height=500)
# cv.button_start = tk.Button(cv, text="开始", width=5, font='Arial -30 bold',
#                               command=bind())
# cv.button_end = tk.Button(cv, text="结束", width=5, font='Arial -30 bold',
#                               command=unbind())
# # cv.pack(expand=YES, fill=BOTH)
# cv.button_start.pack()
# cv.button_end.pack()


class GUI:
    # GUI
    # 图像比例
    Pic_Ratio = 10

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("疏散模拟")
        self.root.geometry("1100x950")
        self.root.resizable(width=True, height=True)

        self.canvas = tk.Canvas(self.root, width=1000, height=500, bg="grey")
        self.canvas.pack()

        self.button_start = tk.Button(self.root, text="开始", width=5, font='Arial -30 bold',
                                      command=lambda: self.bind())
        self.button_end = tk.Button(self.root, text="结束", width=5, font='Arial -30 bold',
                                    command=lambda: self.unbind())

        self.button_start.place(x=925, y=760)
        self.button_end.place(x=925, y=830)

    def bind(self):
        print("sss")
        self.canvas.bind("<Button-1>", self.paint)

    def unbind(self):
        print("eee")
        self.canvas.unbind("<Button-1>")

    def paint(self, event):
        print("x:", event.x, "y:", event.y)


UI = GUI()

UI.root.mainloop()
