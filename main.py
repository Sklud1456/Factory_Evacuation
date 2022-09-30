import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import time
import random

from MAP import myMap
from people import People


class GUI:
    # GUI
    # 图像比例
    Pic_Ratio = 10

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("疏散模拟")
        self.root.geometry("1100x950")
        self.root.resizable(width=True, height=True)

        width = myMap.Length * GUI.Pic_Ratio
        height = myMap.Width * GUI.Pic_Ratio
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="grey")
        self.canvas.pack()

        self.label_text = tk.Label(self.root, text="疏散人数:", font='Arial -37 bold')
        self.label_time = tk.Label(self.root, text="耗时 = 0.00s", font='Arial -37 bold')
        self.label_evac = tk.Label(self.root, text="已疏散: 0", font='Arial -37 bold')
        self.entry_peoplenumber = tk.Entry(self.root, font=(None, 35), width=6)
        self.button_start = tk.Button(self.root, text="开始", width=5, font='Arial -30 bold',
                                      command=lambda: self.Cellular_Automata(int(self.entry_peoplenumber.get())))
        self.button_createpeople = tk.Button(self.root, text="生成", width=5, font='Arial -30 bold',
                                             command=lambda: self.create_people(int(self.entry_peoplenumber.get())))
        self.button_bindmouse = tk.Button(self.root, text="绑定鼠标", width=7, font='Arial -30 bold',
                                          command=lambda: self.bind())
        self.button_unbindmouse = tk.Button(self.root, text="解绑鼠标", width=7, font='Arial -30 bold',
                                            command=lambda: self.unbind())

        self.label_time.place(x=40, y=760)
        self.label_evac.place(x=40, y=810)
        self.button_start.place(x=925, y=820)
        self.button_createpeople.place(x=925, y=760)
        self.button_bindmouse.place(x=500, y=830)
        self.button_unbindmouse.place(x=650, y=830)
        self.label_text.place(x=580, y=770)
        self.entry_peoplenumber.place(x=760, y=770)

        self.setBarrier()
        self.setExit()

    # 查询鼠标位置
    def bind(self):
        print("sss")
        self.canvas.bind("<Button-1>", self.paint)

    def unbind(self):
        print("eee")
        self.canvas.unbind("<Button-1>")

    def addpeoplebymouse(self):
        print("none")

    def paint(self, event):
        print("x:", event.x, "y:", event.y)

    # 障碍
    def setBarrier(self):
        for (A, B, C) in myMap.Barrier:
            x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            str = ""
            text = ""
            if C == 1:
                str = "#FF0000"  # 红色
                text = "甲类"
            elif C == 2:
                str = "#B22222"  # 砖红色
                text = "乙类"
            elif C == 3:
                str = "#FF8C00"  # 橙色
                text = "丙类"
            elif C == 4:
                str = "#FFFF00"  # 黄色
                text = "丁类"
            elif C == 5:
                str = "#0000FF"  # 蓝色
                text = "戊类"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=str, outline=str)
            self.canvas.create_text(int((x1 + x2) / 2), int((y1 + y2) / 2), text=text, fill='#7CCD7C', anchor="center",
                                    font=('微软雅黑', 15, 'bold'))

    # 出口
    def setExit(self):
        print(myMap.Exits)
        for num in range(len(myMap.Exits)):
            for (x, y) in myMap.Exits[num]:
                sx, sy = x - 1, y - 1
                ex, ey = x + 1, y + 1
                [sx, sy, ex, ey] = map(lambda x: x * GUI.Pic_Ratio, [sx, sy, ex, ey])
                self.canvas.create_rectangle(sx, sy, ex, ey, fill="green", outline="green")

    def Update_People(self, People_List):
        for p in People_List:
            # print(p.id)
            self.canvas.delete(p.name())

        self.Show_People(People_List)

    def Show_People(self, People_List):
        for p in People_List:
            if p.savety:
                continue
            ox, oy = p.pos[0], p.pos[1]
            x1, y1 = ox - 0.2, oy - 0.2
            x2, y2 = ox + 0.2, oy + 0.2
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", tag=p.name())

    def Cellular_Automata(self, Total_People):
        # UI = GUI()

        # Total_People = 200
        # P = People(Total_People, myMap)
        # UI.Show_People(P.list)
        P = self.People

        Time_Start = time.time()
        Eva_Number = 0
        while Eva_Number < Total_People:
            Eva_Number = P.run()

            UI.Update_People(P.list)

            # time.sleep(random.uniform(0.05, 0.15))
            time.sleep(0.01)
            UI.canvas.update()
            UI.root.update()

            Time_Pass = time.time() - Time_Start
            UI.label_time['text'] = "Time = " + "%.2f" % Time_Pass + "s"
            UI.label_evac['text'] = "Evacution People: " + str(Eva_Number)
        # print("%.2fs" % (Time_Pass) + " 已疏散人数:" +str(Eva_Number))

        Time_Pass = time.time() - Time_Start
        UI.label_time['text'] = "Time = " + "%.2f" % Time_Pass + "s"
        UI.label_evac['text'] = "Evacution People: " + str(Eva_Number)

        # 热力图
        sns.heatmap(P.thmap.T, cmap='Reds')
        plt.axis('equal')
        plt.show()

    def create_people(self, Total_People):
        self.People = People(Total_People, myMap)
        UI.Update_People(self.People.list)


# UI.root.mainloop()


UI = GUI()

UI.root.mainloop()
# Cellular_Automata(Total_People=1000)
