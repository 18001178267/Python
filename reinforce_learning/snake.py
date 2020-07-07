import numpy as np
import pickle
import pygame as pg
SW = 500
SH = 500
pg.init()                    #初始化所有导入的 pygame 模块
clock = pg.time.Clock()      #创建一个对象来帮助跟踪时间
win = pg.display.set_mode((SW, SH))  #初始化一个准备显示的窗口
SIZE = 15
EPOCHS = 160000
LOSE_PENALTY = 601
EAT_REWARD = 60
MOVE_PENALTY = 3
EPS = 0.7
EPS_DECAY = 0.9997
SHOW_WHEN = 2000
STEPS = 220
LEARNING_RATE = 0.8
DISCOUNT = 0.99
FPS = 30
SCALING = SW // SIZE
starting_q_table = None

class Snake:
    def __init__(self):
        self.x = 8
        self.y = 7
        self.size = 4
        self.dir = 1  #directions are 0-up, 1-right, 2-down, 3-left
        self.ate = False
        self.body = []
        for i in range(self.size):
            self.body.append((self.x-i, self.y-i))

    def move(self):
        if self.dir % 2 == 0:
            if self.dir > 0:
                self.y += 1
            else:
                self.y -= 1
        else:
            if self.dir > 1:
                self.x += 1
            else:
                self.x -= 1
        if self.x >= SIZE:  # no walls, snake will go through
            self.x = 0
        elif self.x < 0:
            self.x = SIZE - 1
        if self.y >= SIZE:
            self.y = 0
        elif self.y < 0:
            self.y = SIZE - 1
        if self.ate:
            self.ate = False
            self.body.append(self.body[-1])
        self.body[0] = (self.x, self.y)

        for i in range(len(self.body)):
            if i > 0:
                self.body[-i] = self.body[-i - 1]

    def change_direction(self, new_dir):
        if abs(self.dir - new_dir) != 2:
            self.dir = new_dir

    def act(self, new_dir):
        if new_dir != self.dir:
            self.change_direction(new_dir)
        self.move()

    def draw(self, window):
        for part in self.body:
            #绘制矩形 pygame.draw.rect
            pg.draw.rect(window, (255, 255, 255),
                         (part[0] * SCALING + 1, part[1] * SCALING + 1, SCALING - 2, SCALING - 2))


class Treat:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
    def change_pos(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
    def draw(self, window):
        pg.draw.rect(window, (0, 255, 100), (self.x * SCALING, self.y * SCALING, SCALING, SCALING))

# =========================================================================
# observation space is location of food relative to head and is there a body on the left, right or fowards

if starting_q_table is None:
    q_table = {}
    for xtf in range(-SIZE + 1, SIZE):
        for ytf in range(-SIZE + 1, SIZE):
            for lb in range(2):
                for rb in range(2):
                    for ub in range(2):
                        for db in range(2):
                            for direction in range(4):
                                q_table[(xtf, ytf), lb, rb, ub, db, direction] = np.random.uniform(-8, 0, size=4)     #随机数Q表

epoch_rewards = []
suicides = 0
best_mean = -1000
best_q_table = {}

for epoch in range(EPOCHS + 2):
    python = Snake()
    food = Treat()
    inside = False

    #判断食物是否在🐍的体内
    for part in python.body:
        if part == (food.x, food.y):
            inside = True
            break

        while inside:
            inside = False
            food.change_pos()
            for part in python.body:
                if part == (food.x, food.y):
                    inside = True
                    break

    #每运行五百代打印
    if not epoch % 500:
        # print(f"{epoch}#")
        print(epoch)

    if epoch % SHOW_WHEN == 0:
        render = True
        current_mean = np.mean(epoch_rewards[-SHOW_WHEN:])
        print(epoch, 'mean:', current_mean, 'suicides:', suicides, 'epsilon:',EPS)
        suicides = 0
    else:
        render = False
    epoch_rew = 0
    for i in range(STEPS + render * 1000):
        left_b = 0
        right_b = 0
        up_b = 0
        down_b = 0

        for part in python.body:

            if part == (python.x - 1, python.y):                       #x-1说明向左移动了
                left_b = 1
            elif python.x - 1 < 0 and part == (SIZE - 1, python.y):    #说明穿过最左面，到达了最右端
                left_b = 1
            if part == ((python.x + 1) % SIZE, python.y):
                right_b = 1
            if part == (python.x, python.y - 1):
                up_b = 1
            elif python.y - 1 < 0 and part == (python.x, SIZE - 1):
                up_b = 1
            if part == (python.x, (python.y + 1) % SIZE):
                down_b = 1

        obs = ((python.x - food.x, python.y - food.y), left_b, right_b, up_b, down_b, python.dir)  #当前移动位置的索引
        if np.random.random() > EPS:
            action = np.argmax(q_table[obs])                 #返回最大索引

        else:
            action = np.random.randint(0, 4)

        python.act(action)
        if python.x == food.x and python.y == food.y:
            python.ate = True
            food.change_pos()
            reward = EAT_REWARD
            inside = False
            for part in python.body:
                if part == (food.x, food.y):
                    inside = True
                    break

            while inside:
                inside = False
                food.change_pos()
                for part in python.body:
                    if part == (food.x, food.y):
                        inside = True
                        break

        else:
            reward = 0
            for part in python.body:
                if part == (python.x, python.y) and part is not python.body[0]:
                    reward = -LOSE_PENALTY
                    suicides += 1

                    break

            if reward == 0:
                reward = -MOVE_PENALTY
        new_observation = ((python.x - food.x, python.y - food.y), left_b, right_b, up_b, down_b, python.dir)
        max_future_q = np.max(q_table[new_observation])
        current_q = q_table[obs][action]
        if reward == EAT_REWARD:
            new_q = EAT_REWARD

        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q
        pg.event.get()

        if render:
            clock.tick(FPS)
            win.fill((0, 0, 0))
            python.draw(win)
            food.draw(win)
            pg.display.update()
        epoch_rew += reward
        if reward == -LOSE_PENALTY:
            break

    if render:
        print("snake length ",len(python.body) - 2, 'did suicide: ',suicides)

    if current_mean > best_mean:
        best_q_table = q_table
        best_mean = current_mean

    epoch_rewards.append(epoch_rew)
    EPS *= EPS_DECAY

pg.quit()
