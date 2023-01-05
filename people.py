from MAP import MoveTO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
import random


class Person:
    # 标准速度设置
    Normal_Speed = 1.0

    def __init__(self, id, pos_x, pos_y, tpye="normal"):
        self.id = id
        self.pos = (pos_x, pos_y)
        self.speed = Person.Normal_Speed
        self.savety = False
        self.membertype = tpye
        if tpye == "hurt":
            self.hurt = random.uniform(0, 1)
        else:
            self.hurt = 0
        self.scared = False

    def name(self):
        return "ID_" + str(self.id)

    def __str__(self):
        return self.name() + " (%d, %d)" % (self.pos[0], self.pos[1])


class People:
    def __init__(self, cnt, myMap, tpye):
        self.list = []
        self.tot = cnt
        if len(myMap.newB) != 0:
            myMap.newB = list()
        # 实际地图
        self.map = myMap
        self.Length = myMap.Length
        self.Width = myMap.Width
        # 某时刻 map 上站的人的个数
        # 反映人流密度
        self.rmap = np.zeros((myMap.Length + 2, myMap.Width + 2))
        self.sacreseed = (24, 60)
        # 扩散的初始范围
        self.sacrescale = [(23, 59), (25, 61)]
        # 恐惧扩散地图
        self.sacremap = np.zeros((myMap.Length + 2, myMap.Width + 2))
        # map 上总的经过人数
        # 热力图
        self.thmap = np.zeros(((myMap.Length + 2), (myMap.Width + 2)))

        if tpye == 1:  # 正常生成
            for i in range(cnt):
                pos_x, pos_y = myMap.Random_Valid_Point()
                if myMap.CheckHurt((pos_x, pos_y)) == True:  # 判断是否受伤
                    self.list.append(Person(i + 1, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
        else:  # 按比例生成
            cnt1 = int(cnt * 0.2)  # 行政
            cnt2 = int(cnt * 0.2)  # 化验
            cnt3 = int(cnt * 0.05)  # 仓库
            cnt4 = int(cnt * 0.15)  # 储罐
            cnt5 = int(cnt * 0.25)  # 车间
            cnt6 = int(cnt * 0.05)  # 消防
            cnt7 = cnt - cnt1 - cnt2 - cnt3 - cnt4 - cnt5 - cnt6  # 机房
            # 行政区域
            for i in range(cnt1):
                pos_x, pos_y = myMap.Random_Valid_Point_S(78, 96, 5, 27)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 化验区域
            for i in range(cnt2):
                pos_x, pos_y = myMap.Random_Valid_Point_S(45, 74, 5, 28)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1, pos_x, pos_y, "hurt"))  # 通过不断累加来保证id的唯一性
                else:
                    self.list.append(Person(i + 1 + cnt1, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 仓库区域
            for i in range(cnt3):
                pos_x, pos_y = myMap.Random_Valid_Point_S(2, 41, 4, 28)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1 + cnt2, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1 + cnt1 + cnt2, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 储罐区域
            for i in range(cnt4):
                pos_x, pos_y = myMap.Random_Valid_Point_S(5, 33, 33, 69)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 车间区域
            for i in range(cnt5):
                pos_x, pos_y = myMap.Random_Valid_Point_S(36, 70, 31, 70)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 消防区域
            for i in range(cnt6):
                pos_x, pos_y = myMap.Random_Valid_Point_S(72, 97, 30, 50)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4 + cnt5, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4 + cnt5, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)
            # 机房区域
            for i in range(cnt7):
                pos_x, pos_y = myMap.Random_Valid_Point_S(73, 97, 52, 72)
                if myMap.CheckHurt((pos_x, pos_y)) == True:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4 + cnt5 + cnt6, pos_x, pos_y, "hurt"))
                else:
                    self.list.append(Person(i + 1 + cnt1 + cnt2 + cnt3 + cnt4 + cnt5 + cnt6, pos_x, pos_y))
                self.addMapValue(self.rmap, pos_x, pos_y)
                self.addMapValue(self.thmap, pos_x, pos_y)

    # 初始化地图的值
    def setMapValue(self, mp, x, y, val=0):
        x, y = int(x), int(y)
        mp[x][y] = val

    # 增加对应地图的值
    def addMapValue(self, mp, x, y, add=1):
        if mp is self.rmap:
            x, y = int(x), int(y)
            mp[x][y] += add
        else:
            x, y = int(x), int(y)
            mp[x][y] += add

    def getMapValue(self, mp, x, y):
        x, y = int(x), int(y)
        return mp[x][y]

    def getSpeed(self, p):

        x, y = int(p.pos[0]), int(p.pos[1])
        tot = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if self.map.Check_Valid(nx, ny):
                    tot += self.rmap[nx][ny]
        # ratio = random.uniform(math.exp(-2*tot/(5*5)), 1.5*math.exp(-2*tot/(5*5)))
        # 根据人群密度来适当降低速度
        if tot < 2:
            ratio = random.uniform(1.1, 1.3)
        elif tot < 4:
            ratio = random.uniform(0.9, 1.1)
        elif tot < 7:
            ratio = random.uniform(0.7, 1.0)
        else:
            ratio = random.uniform(0.6, 0.7)
        # 受伤之后也会降低速度
        if p.membertype == "hurt":
            ratio -= 0.3 * p.hurt
        return Person.Normal_Speed * ratio

    def getdensity(self, p):
        x, y = int(p.pos[0]), int(p.pos[1])
        tot = 0
        # 查看临近单元格中的人数
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if self.map.Check_Valid(nx, ny):
                    tot += self.rmap[nx][ny]
        return tot

    def move(self, p, dire, show=False):
        # 移动
        if show:
            print(p, end=' ')
            print("to", end=' ')
        # 当前位置
        (now_x, now_y) = p.pos
        # 及时在map上更新
        self.addMapValue(self.rmap, now_x, now_y, -1)
        # 移动后的位置
        (next_x, next_y) = p.pos + MoveTO[dire]  # MoveTO为方向数组
        self.addMapValue(self.rmap, next_x, next_y, 1)
        p.pos = (next_x, next_y)

        # 检查是否安全
        if self.map.checkSavefy(p.pos):
            p.savety = True
            self.setMapValue(self.rmap, next_x, next_y, 0)

        addThVal = self.getMapValue(self.rmap, next_x, next_y)
        # 热力图的记录只增不减
        self.addMapValue(self.thmap, next_x, next_y, addThVal)

    # 恐惧扩散的实现
    def scarediffuse(self):
        # 这四个变量和障碍的意义一致，分别表示左下角和右上角的坐标
        startx = self.sacrescale[0][0]
        endx = self.sacrescale[1][0]
        starty = self.sacrescale[0][1]
        endy = self.sacrescale[1][1]
        for i in range(startx, endx + 1):
            for j in range(starty, endy + 1):
                self.sacremap[i][j] = 1
        # 逐步扩散
        newstartx = startx - 2
        newendx = endx + 2
        newstarty = starty - 2
        newendy = endy + 2
        # 判断边界
        if newstartx < 0:
            newstartx = 0
        if newendx > self.Length + 1:
            newendx = self.Length
        if newstarty < 0:
            newstarty = 0
        if newendy > self.Width + 1:
            newendy = self.Width
        self.sacrescale = [(newstartx, newstarty), (newendx, newendy)]
        # 将恐惧范围内的人群状态及时更新
        for p in self.list:
            x = int(p.pos[0])
            y = int(p.pos[1])
            if self.sacremap[x][y] == 1:
                p.scared = True

        # sns.heatmap(self.sacremap.T, cmap='Reds', vmax=self.sacremap.max(), vmin=self.sacremap.min())
        # plt.axis('equal')
        # plt.show()

    def run(self):
        cnt = 0
        self.scarediffuse()
        dead = 0
        hurt = 0
        for p in self.list:
            # 计数
            if p.savety and p.membertype != "hurt":
                cnt = cnt + 1
                continue

            if p.membertype == "dead":
                dead = dead + 1
                continue

            if p.membertype == "hurt":
                hurt = hurt + 1

            if p.scared == False:
                continue
            # speed = 1
            speed = self.getSpeed(p)
            choice = []
            weigh = []

            # 八个方向
            Dire = [0, 1, 2, 3, 4, 5, 6, 7]
            random.shuffle(Dire)  # 随机选择

            # 确认死亡
            if self.map.CheckDead(p.pos[0], p.pos[1]) == True:
                p.membertype = "dead"
                continue
            while len(choice) == 0:
                # 遍历方向，方便之后选择
                if (speed <= 0.2):
                    break
                for dire in Dire:
                    dx, dy = MoveTO[dire][0] * speed, MoveTO[dire][1] * speed
                    (next_x, next_y) = p.pos[0] + dx, p.pos[1] + dy
                    # 下一步能走
                    if (self.map.Check_Valid(next_x, next_y)) and (
                            self.getMapValue(self.rmap, next_x, next_y) < 1):  # 下一步合理且人数小于1
                        choice.append(dire)
                        weigh.append(self.map.getDeltaP(p.pos, (next_x, next_y)))
                # 当速度过大导致没有路可走时，通过降速来实现路径的选择
                speed -= 0.1
            # for dire in Dire:
            #     dx, dy = MoveTO[dire][0] * speed, MoveTO[dire][1] * speed
            #     (next_x, next_y) = p.pos[0] + dx, p.pos[1] + dy
            #     # 下一步能走
            #     if (self.map.Check_Valid(next_x, next_y)) and (self.getMapValue(self.rmap, next_x, next_y) < 1):
            #         choice.append(dire)
            #         weigh.append(self.map.getDeltaP(p.pos, (next_x, next_y)))

            # 在可行的选择列表中选择下降最快的
            if len(choice) > 0:
                index = weigh.index(max(weigh))
                self.move(p, choice[index])
                p.speed = speed
            else:
                self.addMapValue(self.thmap, p.pos[0], p.pos[1])
                p.speed = speed

            if p.savety:
                cnt = cnt + 1

        return cnt, hurt, dead  # 分别代表安全人数，受伤人数，死亡人数

# Total_People = 2
# P = People(Total_People, myMap)

# Eva_Number = 0
# while Eva_Number<Total_People:
# 	Eva_Number = P.run()