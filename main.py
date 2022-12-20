import tkinter as tk
import matplotlib
from tkinter import *

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import seaborn as sns
import numpy as np
import os
import time
import random

from MAP import myMap
from people import People
from people import Person


class GUI:
    # GUI
    # 图像比例
    Pic_Ratio = 10
    People = People(0, myMap, 1)
    flash = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("疏散模拟")
        self.root.geometry("1100x950")
        self.root.resizable(width=True, height=True)

        width = myMap.Length * GUI.Pic_Ratio
        height = myMap.Width * GUI.Pic_Ratio
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="grey")
        self.canvas.pack()

        global image_file
        image_file = tk.PhotoImage(file='2.gif')

        self.label_text = tk.Label(self.root, text="疏散人数:", font='Arial -37 bold')
        self.label_time = tk.Label(self.root, text="时间 = 0.00s", font='Arial -37 bold')
        self.label_evac = tk.Label(self.root, text="已疏散: 0", font='Arial -37 bold')
        self.label_hurtanddead = tk.Label(self.root, text="伤: 0  亡：0", font='Arial -37 bold')
        self.entry_peoplenumber = tk.Entry(self.root, font=(None, 35), width=6)
        self.button_start = tk.Button(self.root, text="开始", width=5, font='Arial -30 bold',
                                      command=lambda: self.Cellular_Automata(int(self.entry_peoplenumber.get())))
        self.button_createpeople = tk.Button(self.root, text="生成", width=5, font='Arial -30 bold',
                                             command=lambda: self.create_people(int(self.entry_peoplenumber.get())))
        self.button_bindmouse = tk.Button(self.root, text="绑定鼠标", width=7, font='Arial -30 bold',
                                          command=lambda: self.bind())
        self.button_unbindmouse = tk.Button(self.root, text="解绑鼠标", width=7, font='Arial -30 bold',
                                            command=lambda: self.unbind())
        self.button_createpeople2 = tk.Button(self.root, text="比例生成", width=7, font='Arial -30 bold',
                                              command=lambda: self.create_people2(int(self.entry_peoplenumber.get())))

        self.label_time.place(x=40, y=760)
        self.label_evac.place(x=40, y=810)
        self.label_hurtanddead.place(x=40, y=860)
        self.button_start.place(x=925, y=830)
        self.button_createpeople.place(x=925, y=760)
        self.button_bindmouse.place(x=480, y=830)
        self.button_unbindmouse.place(x=620, y=830)
        self.button_createpeople2.place(x=770, y=830)
        self.label_text.place(x=580, y=770)
        self.entry_peoplenumber.place(x=760, y=770)

        self.setBarrier()
        self.setExit()

    # 查询鼠标位置
    def bind(self):
        self.canvas.bind("<Button-1>", self.paint)

    def unbind(self):
        self.canvas.unbind("<Button-1>")

    def addpeoplebymouse(self):
        print("none")

    def paint(self, event):
        pos_x = event.x
        pos_y = event.y
        # print("x:", event.x, "y:", event.y)
        pos_x = pos_x / self.Pic_Ratio
        pos_y = pos_y / self.Pic_Ratio
        self.People.tot += 1
        self.entry_peoplenumber.delete(0, "end")
        self.entry_peoplenumber.insert(0, str(self.People.tot))
        temp = Person(self.People.tot, pos_x, pos_y, "special")
        self.People.list.append(temp)
        # print(temp.name())
        self.People.addMapValue(self.People.rmap, pos_x, pos_y)
        self.People.addMapValue(self.People.thmap, pos_x, pos_y)
        self.Update_People(self.People.list)

    # 障碍
    def setBarrier(self):
        # 遍历障碍列表来构建障碍
        for (A, B, C) in myMap.Barrier:
            # x1,y1,x2,y2分别为左下角和右上角的坐标值，通过这两个值来确定范围
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
            elif C == 0:
                str = "#FF0000"  # 红色
                text = "甲类"

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=str, outline=str)
            if C == 1:
                self.canvas.create_image(int((x2 - 20)), int((y2 - 20)), anchor='nw', image=image_file)
            self.canvas.create_text(int((x1 + x2) / 2), int((y1 + y2) / 2), text=text, fill='#7CCD7C', anchor="center",
                                    font=('微软雅黑', 15, 'bold'))

    def flashboom(self):
        if len(myMap.newB) != 0:
            for (A, B, C) in myMap.newB:
                x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
                [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
                # 通过不断切换颜色来实现闪烁
                if C == 0:
                    if self.flash == 0:
                        str = "#FF0000"  # 红色
                    else:
                        str = "#FF6600"  # 橙红色
                else:
                    continue
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=str, outline=str, tag="newb")
        for (A, B, C) in myMap.Barrier:
            x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            if C == 0:
                if self.flash == 0:
                    str = "#FF0000"  # 红色
                    text = "甲类"
                    self.flash = 1
                else:
                    str = "#FF6600"  # 橙红色
                    text = "甲类"
                    self.flash = 0
            else:
                continue
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=str, outline=str)
            self.canvas.create_text(int((x1 + x2) / 2), int((y1 + y2) / 2), text=text, fill='#7CCD7C', anchor="center",
                                    font=('微软雅黑', 15, 'bold'))

    # 障碍扩散
    def updateBarrier(self):
        # 遍历新的障碍列表来新建障碍
        for (A, B, C) in myMap.newB:
            x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            str = ""
            if C == 1:
                str = "#FF0000"  # 红色
            elif C == 2:
                str = "#B22222"  # 砖红色
            elif C == 3:
                str = "#FF8C00"  # 橙色
            elif C == 4:
                str = "#FFFF00"  # 黄色
            elif C == 5:
                str = "#0000FF"  # 蓝色
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=str, outline=str, tag="newb")

    # 出口
    def setExit(self):
        print(myMap.Exits)
        for num in range(len(myMap.Exits)):
            for (x, y) in myMap.Exits[num]:
                sx, sy = x - 1, y - 1
                ex, ey = x + 1, y + 1
                # 使用map函数将所有值放大相应倍数
                [sx, sy, ex, ey] = map(lambda x: x * GUI.Pic_Ratio, [sx, sy, ex, ey])
                self.canvas.create_rectangle(sx, sy, ex, ey, fill="green", outline="green")

    def Update_People(self, People_List):
        for p in People_List:
            # print(p.id)
            self.canvas.delete(p.name())
            # print(p.pos[0],p.pos[1])

        self.Show_People(People_List)

    def Show_People(self, People_List):
        for p in People_List:
            if p.savety:
                continue
            ox, oy = p.pos[0], p.pos[1]
            x1, y1 = ox - 0.2, oy - 0.2
            x2, y2 = ox + 0.2, oy + 0.2
            # 使用map函数将所有值放大相应倍数
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            if p.membertype == "special":
                self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="blue", tag=p.name())
            elif p.membertype == "dead":
                self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="red", tag=p.name())
            elif p.membertype == "hurt":
                self.canvas.create_oval(x1, y1, x2, y2, fill="yellow", outline="yellow", tag=p.name())
            else:
                self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", tag=p.name())

    def Cellular_Automata(self, Total_People):
        # UI = GUI()
        P = self.People

        Time_Start = time.time()
        Eva_Number = 0  # 逃生人数
        Hurt_Number = 0  # 受伤人数
        Dead_Number = 0  # 死亡人数
        cnt = 1
        while Eva_Number + Dead_Number < Total_People:
            # 实现闪烁
            self.flashboom()
            Time_Pass = time.time() - Time_Start
            temp = random.uniform(0, 1)
            if (Time_Pass >= 10) and (cnt == 1) and temp > 0.9:
                # 实现障碍的扩散
                myMap.update_Potential()
                P.map = myMap
                self.updateBarrier()
                cnt = 0
            # 主要的疏散函数就是P.run()
            Eva_Number, Hurt_Number, Dead_Number = P.run()

            UI.Update_People(P.list)
            # 通过sleep函数实现疏散效果拟真
            if (cnt == 0):
                cnt = 2
            elif cnt == 1:
                time.sleep(0.4)
            else:
                time.sleep(0.4)

            UI.canvas.update()
            UI.root.update()

            Time_Pass = time.time() - Time_Start
            UI.label_time['text'] = "时间 = " + "%.2f" % Time_Pass + "s"
            UI.label_evac['text'] = "已疏散: " + str(Eva_Number)
            UI.label_hurtanddead['text'] = "伤: " + str(Hurt_Number) + "  亡：" + str(Dead_Number)

        Time_Pass = time.time() - Time_Start
        UI.label_time['text'] = "时间 = " + "%.2f" % Time_Pass + "s"
        UI.label_evac['text'] = "已疏散: " + str(Eva_Number)
        UI.label_hurtanddead['text'] = "伤: " + str(Hurt_Number) + "  亡：" + str(Dead_Number)

        # 清空扩散的障碍
        self.canvas.delete("newb")
        # 绘制热力图
        heatmap = np.array(P.thmap)
        see = np.array(P.map.blankspace)
        # 通过加数值的方式来画出地图
        for i in range(see.shape[0]):
            for j in range(see.shape[1]):
                if see[i][j] == float("inf"):
                    see[i][j] = 50
        heatmap += see
        sns.heatmap(heatmap.T, cmap='Reds')
        plt.axis('equal')
        plt.show()

    # 正常生成
    def create_people(self, Total_People):
        self.People = People(Total_People, myMap, 1)
        UI.Update_People(self.People.list)

    # 按比例生成智能体
    def create_people2(self, Total_People):
        self.People = People(Total_People, myMap, 2)
        UI.Update_People(self.People.list)

UI = GUI()

UI.root.mainloop()
# Cellular_Automata(Total_People=1000)