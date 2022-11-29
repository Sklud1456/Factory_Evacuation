from MAP import MoveTO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
import random


class Person:
    Normal_Speed = 1.0

    def __init__(self, id, pos_x, pos_y,tpye="normal"):
        self.id = id
        self.pos = (pos_x, pos_y)
        self.speed = Person.Normal_Speed
        self.savety = False
        self.membertype = tpye
        self.scared = False

    def name(self):
        return "ID_" + str(self.id)

    def __str__(self):
        return self.name() + " (%d, %d)" % (self.pos[0], self.pos[1])


class People:
    def __init__(self, cnt, myMap):
        self.list = []
        self.tot = cnt
        self.map = myMap
        # 某时刻 map 上站的人的个数
        # 反映人流密度
        self.Length = myMap.Length
        self.Width = myMap.Width
        self.rmap = np.zeros((myMap.Length + 2, myMap.Width + 2))
        self.sacreseed = (24, 60)
        self.sacrescale = [(23, 59), (25, 61)]
        self.sacremap = np.zeros((myMap.Length + 2, myMap.Width + 2))
        # map 上总的经过人数
        # 热力图
        self.thmap = np.zeros(((myMap.Length + 2), (myMap.Width + 2)))
        for i in range(cnt):
            pos_x, pos_y = myMap.Random_Valid_Point()
            self.list.append(Person(i + 1, pos_x, pos_y))
            self.addMapValue(self.rmap, pos_x, pos_y)
            self.addMapValue(self.thmap, pos_x, pos_y)

    def setMapValue(self, mp, x, y, val=0):
        x, y = int(x), int(y)
        mp[x][y] = val

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
        if tot < 2:
            ratio = random.uniform(1.1, 1.5)
        elif tot < 4:
            ratio = random.uniform(0.9, 1.1)
        elif tot < 7:
            ratio = random.uniform(0.9, 1.0)
        else:
            ratio = random.uniform(0.7, 0.9)
        return Person.Normal_Speed * ratio

    def getdensity(self, p):
        x, y = int(p.pos[0]), int(p.pos[1])
        tot = 0
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
        (now_x, now_y) = p.pos
        self.addMapValue(self.rmap, now_x, now_y, -1)

        (next_x, next_y) = p.pos + MoveTO[dire]
        self.addMapValue(self.rmap, next_x, next_y, 1)
        p.pos = (next_x, next_y)

        if self.map.checkSavefy(p.pos):
            p.savety = True
            self.setMapValue(self.rmap, next_x, next_y, 0)

        addThVal = self.getMapValue(self.rmap, next_x, next_y)
        self.addMapValue(self.thmap, next_x, next_y, addThVal)

        if show:
            print(p)

    def scarediffuse(self):
        startx = self.sacrescale[0][0]
        endx = self.sacrescale[1][0]
        starty = self.sacrescale[0][1]
        endy = self.sacrescale[1][1]
        for i in range(startx, endx + 1):
            for j in range(starty, endy + 1):
                self.sacremap[i][j] = 1
        newstartx = startx - 2
        newendx = endx + 2
        newstarty = starty - 2
        newendy = endy + 2
        if newstartx < 0:
            newstartx = 0
        if newendx > self.Length + 1:
            newendx = self.Length
        if newstarty < 0:
            newstarty = 0
        if newendy > self.Width + 1:
            newendy = self.Width
        self.sacrescale = [(newstartx, newstarty), (newendx, newendy)]
        for p in self.list:
            x=int(p.pos[0])
            y=int(p.pos[1])
            if self.sacremap[x][y]==1:
                p.scared=True

        # sns.heatmap(self.sacremap.T, cmap='Reds', vmax=self.sacremap.max(), vmin=self.sacremap.min())
        # plt.axis('equal')
        # plt.show()

    def run(self):
        cnt = 0
        self.scarediffuse()

        for p in self.list:
            # time.sleep(0.0011)
            if p.savety:
                cnt = cnt + 1
                continue

            if p.scared == False:
                continue
            speed = 1
            # speed=self.getSpeed(p)
            # speed = p.speed #random.uniform(p.speed-0.1, p.speed+0.1)
            # (now_x, now_y) = p.pos
            choice = []
            weigh = []

            # 八个方向
            Dire = [0, 1, 2, 3, 4, 5, 6, 7]
            random.shuffle(Dire)

            dens = self.getdensity(p)

            # while len(choice) == 0:
            #     # 遍历方向，方便之后选择
            #     if (speed <= 0.2):
            #         break
            #     for dire in Dire:
            #         dx, dy = MoveTO[dire][0] * speed, MoveTO[dire][1] * speed
            #         (next_x, next_y) = p.pos[0] + dx, p.pos[1] + dy
            #         # 下一步能走
            #         if (self.map.Check_Valid(next_x, next_y)) and (self.getMapValue(self.rmap, next_x, next_y) < 1):
            #             choice.append(dire)
            #             weigh.append(self.map.getDeltaP(p.pos, (next_x, next_y)))
            #     speed -= 0.1
            for dire in Dire:
                dx, dy = MoveTO[dire][0] * speed, MoveTO[dire][1] * speed
                (next_x, next_y) = p.pos[0] + dx, p.pos[1] + dy
                # 下一步能走
                if (self.map.Check_Valid(next_x, next_y)) and (self.getMapValue(self.rmap, next_x, next_y) < 1):
                    choice.append(dire)
                    weigh.append(self.map.getDeltaP(p.pos, (next_x, next_y)))

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

        return cnt

# Total_People = 2
# P = People(Total_People, myMap)


# Eva_Number = 0
# while Eva_Number<Total_People:
# 	Eva_Number = P.run()

# time.sleep(0.5)
