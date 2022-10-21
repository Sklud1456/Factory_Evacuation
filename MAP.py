import numpy as np
from queue import Queue
import random

Direction = {
    "RIGHT": 0, "UP": 1, "LEFT": 2, "DOWN": 3, "NONE": -1
}

MoveTO = []
MoveTO.append(np.array([1, 0]))  # RIGHT
MoveTO.append(np.array([0, -1]))  # UP
MoveTO.append(np.array([-1, 0]))  # LEFT
MoveTO.append(np.array([0, 1]))  # DOWN

MoveTO.append(np.array([1, -1]))
MoveTO.append(np.array([-1, -1]))
MoveTO.append(np.array([-1, 1]))
MoveTO.append(np.array([1, 1]))


# 输入：一条线段的两个端点
# 输出：整点集合
def Init_Exit(P1, P2):
    exit = list()

    if P1[0] == P2[0]:
        x = P1[0]
        for y in range(P1[1], P2[1] + 1):
            exit.append((x, y))
    elif P1[1] == P2[1]:
        y = P1[1]
        for x in range(P1[0], P2[0] + 1):
            exit.append((x, y))
    # 斜线
    else:
        pass

    return exit


# 两点坐标围成的矩形区域
def Init_Barrier(A, B):
    if A[0] > B[0]:
        A, B = B, A

    x1, y1 = A[0], A[1]
    x2, y2 = B[0], B[1]

    if y1 < y2:
        return ((x1, y1), (x2, y2))
    else:
        return ((x1, y2), (x2, y1))


def Init_Barrier1(A, B, C):
    if A[0] > B[0]:
        A, B = B, A

    x1, y1 = int(A[0] / 3), 75 - int(A[1] / 3)
    x2, y2 = int(B[0] / 3), 75 - int(B[1] / 3)

    if y1 < y2:
        return ((x1, y1), (x2, y2), C)
    else:
        return ((x1, y2), (x2, y1), C)


# 
# 外墙宽度 
# Size
Outer_Size = 1


# 障碍 	-1
# LEFT 	0
# UP	1
# RIGHT 2
# DOWN  3


class Map:
    def __init__(self, L, W, E, B):
        self.Length = L
        self.Width = W
        self.Exits = E
        self.Barrier = B
        self.barrier_list = []
        self.Exit = list()
        for num in range(len(self.Exits)):
            for (x, y) in Exits[num]:
                self.Exit.append((x, y))
        # 0~L+1
        # 0~W+1
        # 势能
        # 出口为 1
        # 障碍为 inf
        self.space = np.zeros((self.Length + Outer_Size * 2, self.Width + Outer_Size * 2))
        for j in range(0, self.Width + Outer_Size * 2):
            self.space[0][j] = self.space[L + 1][j] = float("inf")
            self.barrier_list.append((0, j))
            self.barrier_list.append((L + 1, j))

        for i in range(0, self.Length + Outer_Size * 2):
            self.space[i][0] = self.space[i][W + 1] = float("inf")
            self.barrier_list.append((i, 0))
            self.barrier_list.append((i, W + 1))

        #设立障碍

        for (A, B, C) in self.Barrier:
            for i in range(A[0], B[0] + 1):
                for j in range(A[1], B[1] + 1):
                    self.space[i][j] = float("inf")
                    self.barrier_list.append((i, j))

        # 出口
        for exit in self.Exits:
            for (ex, ey) in exit:
                self.space[ex][ey] = 1
                if ex == self.Length:
                    self.space[ex + 1][ey] = 1
                if ey == self.Width:
                    self.space[ex][ey + 1] = 1
                # #print("%d %d"%(ex, ey))
                if (ex, ey) in self.barrier_list:
                    self.barrier_list.remove((ex, ey))

        # #print(self.barrier_list)

        # #print(type(self.space))
        #
        # 显示全部
        # #print(self.space)

        self.Init_Potential()

    # self.print(self.space)

    def print(self, mat):
        for line in mat:
            for v in line:
                print(v, end=' ')
            print("")

    def Check_Valid(self, x, y):
        # pass
        x, y = int(x), int(y)
        # 边缘
        if x > self.Length + 1 or x < 0 or y > self.Width + 1 or y < 0:
            return False
        # 障碍
        if self.space[x][y] == float("inf"):
            return False
        else:
            return True

    def checkSavefy(self, pos):
        x, y = int(pos[0]), int(pos[1])
        if x == self.Length + 1:
            x -= 1
        elif x == -1:
            x += 1
        if y == self.Width + 1:
            y -= 1
        elif y == -1:
            y -= 0

        if (x, y) in self.Exit:
            return True
        else:
            return False

    def getDeltaP(self, P1, P2):
        x1, y1 = int(P1[0]), int(P1[1])
        x2, y2 = int(P2[0]), int(P2[1])
        return self.space[x1][y1] - self.space[x2][y2]

    def Init_Potential(self):
        minDis = np.zeros((self.Length + Outer_Size * 2, self.Width + Outer_Size * 2))
        for i in range(self.Length + Outer_Size * 2):
            for j in range(self.Width + Outer_Size * 2):
                minDis[i][j] = float("inf")

        # #print(minDis)
        for num in range(len(self.Exits)):
            for (sx, sy) in Exits[num]:
                # print(sx, sy)
                tmp = self.BFS(sx, sy)
                # self.#print(tmp)
                # print("----")
                for i in range(self.Length + Outer_Size * 2):
                    for j in range(self.Width + Outer_Size * 2):
                        minDis[i][j] = min(minDis[i][j], tmp[i][j])

        self.space = minDis
        print(minDis.shape)

    # return minDis
    # #print(minDis)

    # 确立势能地图
    def BFS(self, x, y):
        if not self.Check_Valid(x, y):
            return

        tmpDis = np.zeros((self.Length + Outer_Size * 2, self.Width + Outer_Size * 2))
        for i in range(self.Length + Outer_Size * 2):
            for j in range(self.Width + Outer_Size * 2):
                tmpDis[i][j] = self.space[i][j]

        queue = Queue()
        queue.put((x, y))
        tmpDis[x][y] = 1
        while not queue.empty():
            (x, y) = queue.get()
            dis = tmpDis[x][y]
            # if dis>0:
            # 	continue

            for i in range(8):
                move = MoveTO[i]
                (nx, ny) = (x, y) + move
                if self.Check_Valid(nx, ny) and tmpDis[nx][ny] == 0:
                    queue.put((nx, ny))
                    tmpDis[nx][ny] = dis + (1.0 if i < 4 else 1.4)

        return tmpDis

    def Random_Valid_Point(self):
        x = random.uniform(1, self.Length + 2)
        y = random.uniform(1, self.Width + 2)
        while not myMap.Check_Valid(x, y):
            x = random.uniform(1, self.Length + 2)
            y = random.uniform(1, self.Width + 2)

        return x, y


def Init_Map():
    # 房间长宽
    Length = 60
    Width = 10

    # 出口
    # 点集
    Exit = Init_Exit(P1=(60, 2), P2=(60, 4))
    Exit.extend(Init_Exit(P1=(0, 8), P2=(0, 9)))

    # 障碍 矩形区域
    Barrier = list()
    Barrier.append(Init_Barrier(A=(3, 5), B=(60, 7)))
    Barrier.append(Init_Barrier(A=(10, 6), B=(15, 8)))

    return Map(L=Length, W=Width, E=Exit, B=Barrier)


# # 房间长宽
# Length = 30
# Width = 20

# # 出口 
# # 点集
# Exit = Init_Exit(P1=(30, 4), P2=(30, 7))
# Exit.extend(Init_Exit(P1=(30, 15), P2=(30, 18)))

# # 障碍 矩形区域
# Barrier = list()
# Barrier.append(Init_Barrier(A=(3, 5), B=(10, 12)))
# Barrier.append(Init_Barrier(A=(14, 0), B=(16, 15)))
# Barrier.append(Init_Barrier(A=(20, 9), B=(21, 20)))


# myMap = Map(L=Length, W=Width, E=Exit, B=Barrier)


# # 出口
# # 点集
# Exit = Init_Exit(P1=(100, 28), P2=(100, 32))
# Exit.extend(Init_Exit(P1=(0, 28), P2=(0, 32)))

# # 障碍 矩形区域
# Barrier = list()
# Barrier.append(Init_Barrier(A=(24, 0), B=(26, 38)))
# Barrier.append(Init_Barrier(A=(49, 20), B=(51, 60)))
# Barrier.append(Init_Barrier(A=(74, 0), B=(76, 30)))


# myMap =  Map(L=Length, W=Width, E=Exit, B=Barrier)

# 厂区长宽
Length = 100
Width = 75

# 出口 
# 点集
Exits = list()
Exit = Init_Exit(P1=(100, 27), P2=(100, 29))
Exits.append(Init_Exit(P1=(100, 27), P2=(100, 29)))
Exits.append(Init_Exit(P1=(75, 0), P2=(77, 0)))

# Exit.extend(Init_Exit(P1=(0, 25), P2=(0, 35)))

# 甲乙丙丁戊危险划分 1-5
# 障碍 矩形区域
Barrier = list()
# 事故应急池，污水收集池
Barrier.append(Init_Barrier1(A=(33, 35), B=(53, 50), C=3))
# 正丁醇储罐
Barrier.append(Init_Barrier1(A=(65, 33), B=(85, 53), C=1))
# 甲醛储罐1
Barrier.append(Init_Barrier1(A=(33, 64), B=(53, 84), C=1))
# 甲醛储罐2
Barrier.append(Init_Barrier1(A=(65, 64), B=(85, 84), C=1))
# 丁二醇储罐1
Barrier.append(Init_Barrier1(A=(33, 96), B=(53, 116), C=1))
# 丁二醇储罐2
Barrier.append(Init_Barrier1(A=(65, 96), B=(85, 116), C=1))
# 装卸区
Barrier.append(Init_Barrier1(A=(22, 154), B=(52, 198), C=1))
# 仓库
Barrier.append(Init_Barrier1(A=(79, 154), B=(108, 198), C=1))
# 泡沫站
Barrier.append(Init_Barrier1(A=(135, 183), B=(147, 198), C=5))
# 循环水站
Barrier.append(Init_Barrier1(A=(159, 183), B=(171, 198), C=5))
# 公用工程中转站
Barrier.append(Init_Barrier1(A=(137, 154), B=(170, 170), C=5))
# 化验室
Barrier.append(Init_Barrier1(A=(183, 183), B=(215, 198), C=1))
# 中控室
Barrier.append(Init_Barrier1(A=(182, 154), B=(215, 171), C=5))
# 行政楼
Barrier.append(Init_Barrier1(A=(242, 186), B=(278, 198), C=5))
# 食堂
Barrier.append(Init_Barrier1(A=(242, 154), B=(254, 174), C=5))
# 停车场
Barrier.append(Init_Barrier1(A=(266, 154), B=(278, 174), C=5))
# 炔醛反应车间
Barrier.append(Init_Barrier1(A=(117, 80), B=(153, 125), C=1))
# 加氢车间
Barrier.append(Init_Barrier1(A=(169, 80), B=(205, 125), C=1))
# 精制车间
Barrier.append(Init_Barrier1(A=(117, 24), B=(153, 64), C=1))
# 预留用地
Barrier.append(Init_Barrier1(A=(169, 24), B=(205, 64), C=4))
# 消防中心
Barrier.append(Init_Barrier1(A=(234, 112), B=(254, 127), C=5))
# 消防车库
Barrier.append(Init_Barrier1(A=(239, 86), B=(254, 101), C=5))
# 维修站
Barrier.append(Init_Barrier1(A=(266, 112), B=(280, 127), C=5))
# 消防水池
Barrier.append(Init_Barrier1(A=(266, 86), B=(280, 101), C=5))
# 配电室
Barrier.append(Init_Barrier1(A=(234, 46), B=(248, 57), C=3))
# 压缩机房
Barrier.append(Init_Barrier1(A=(234, 22), B=(248, 34), C=1))
# 三废处理站
Barrier.append(Init_Barrier1(A=(260, 22), B=(278, 57), C=2))

# 第一种情况
myMap = Map(L=Length, W=Width, E=Exits, B=Barrier)
