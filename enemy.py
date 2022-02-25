import pygame
import random
from bomb import Bomb
from node import Node
from algorithm import Algorithm
import math


class Enemy:

    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    def __init__(self, x, y):
        self.life = True
        #self.path = []
        #self.movement_path = []
        self.posX = x * 4
        self.posY = y * 4
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.hitWall = True
        #self.range = 3
        #self.bomb_limit = 1
        #self.plant = False
        #self.algorithm = alg

    def move(self, map, bombs, explosions, enemy):
        if self.hitWall:
            self.direction = random.randint(0, 3)
            self.hitWall = False

        tempx = int(self.posX / 4)
        tempy = int(self.posY / 4)

        if not self.hitWall:
            if (self.direction == 0 or self.direction == 2) and int(self.posY) % 4 == 0:
                if map[tempx+1][tempy] == 0:
                    chance = random.random()
                    if chance < 0.1:
                        self.direction = 1
                if map[tempx-1][tempy] == 0:
                    chance = random.random()
                    if chance < 0.1:
                        self.direction = 3

            elif (self.direction == 1 or self.direction == 3) and int(self.posX) % 4 == 0:
                if map[tempx][tempy+1] == 0:
                    chance = random.random()
                    if chance < 0.1:
                        self.direction = 0
                if map[tempx][tempy-1] == 0:
                    chance = random.random()
                    if chance < 0.1:
                        self.direction = 2

        if int(self.posX) % 4 != 0 and (self.direction == 0 or self.direction == 2):
            if int(self.posX) % 4 == 1:
                self.posX -= 0.2
            elif int(self.posX) % 4 == 3:
                self.posX += 0.2
            return

        if int(self.posY) % 4 != 0 and (self.direction == 1 or self.direction == 3):
            if int(self.posY) % 4 == 1:
                self.posY -= 0.2
            elif int(self.posY) % 4 == 3:
                self.posY += 0.2
            return



        # right
        if self.direction == 1:
            if map[tempx + 1][tempy] == 0:
                self.posX += 0.2
            else:
                self.hitWall = True
        # left
        elif self.direction == 3:
            tempx = math.ceil(self.posX / 4)
            if map[tempx - 1][tempy] == 0:
                self.posX -= 0.2
            else:
                self.hitWall = True

        # bottom
        if self.direction == 0:
            if map[tempx][tempy + 1] == 0:
                self.posY += 0.2
            else:
                self.hitWall = True
        # top
        elif self.direction == 2:
            tempy = math.ceil(self.posY / 4)
            if map[tempx][tempy - 1] == 0:
                self.posY -= 0.2
            else:
                self.hitWall = True

    def check_death(self, exp):
        for e in exp:
            for s in e.sectors:
                if int(self.posX / 4) == s[0] and int(self.posY / 4) == s[1]:
                    self.life = False
                    return

    def create_grid(self, map, bombs, explosions, enemys):
        grid = [[0] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destryable
        # 3 - unreachable

        for b in bombs:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]] = 1    #pole rażenia - unsafe
            grid[b.posX][b.posY] = 3    #współrzędne bomby - unreacheable

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]] = 3    #współrzędne wybuchu - unreachable

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    grid[i][j] = 3      #ściana - unreacheable
                elif map[i][j] == 2:
                    grid[i][j] = 2      #karton - destroyable

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.posX / 4)][int(x.posY / 4)] = 2      #współrzędne innego gracza - destroyable

        return grid

    def load_animations(self, en, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        image_path = 'images/enemy/e'
        if en == '':
            image_path = 'images/hero/p'

        f1 = pygame.image.load(image_path + en + 'f0.png')
        f2 = pygame.image.load(image_path + en + 'f1.png')
        f3 = pygame.image.load(image_path + en + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load(image_path + en + 'r0.png')
        r2 = pygame.image.load(image_path + en + 'r1.png')
        r3 = pygame.image.load(image_path + en + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load(image_path + en + 'b0.png')
        b2 = pygame.image.load(image_path + en + 'b1.png')
        b3 = pygame.image.load(image_path + en + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load(image_path + en + 'l0.png')
        l2 = pygame.image.load(image_path + en + 'l1.png')
        l3 = pygame.image.load(image_path + en + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)

