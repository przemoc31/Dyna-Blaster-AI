import pygame
import math
import random
from bomb import Bomb
from node import Node
from nodeA import NodeA
from algorithm import Algorithm


class Player:
    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    def __init__(self, x, y, alg):
        self.life = True
        self.path = []
        self.directions_path = []
        self.posX = x * 4
        self.posY = y * 4
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.range = 3
        self.bomb_limit = 1
        self.plant = False
        self.algorithm = alg
        self.avoidExplosion = False

    def move(self, map, bombs, explosions, enemy):

        if self.direction == 0:
            self.posY += 1
        elif self.direction == 1:
            self.posX += 1
        elif self.direction == 2:
            self.posY -= 1
        elif self.direction == 3:
            self.posX -= 1

        if self.posX % 4 == 0 and self.posY % 4 == 0:
            self.directions_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                grid = self.create_grid(map, bombs, explosions, enemy)
                next = self.path[1]
                if grid[next[0]][next[1]] > 1:
                    self.directions_path.clear()
                    self.path.clear()

        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def make_move(self, map, bombs, explosions, enemys):
        if not self.life:
            return
        if len(self.directions_path) == 0:
            if self.plant:
                bombs.append(self.plant_bomb(map))
                self.plant = False
                map[int(self.posX / 4)][int(self.posY / 4)] = 3

            if self.algorithm is Algorithm.BFS:
                self.BFS(self.create_grid_Algorithm(map, bombs, explosions, enemys), enemys)
            elif self.algorithm is Algorithm.ASTAR:
                self.Astar(self.create_grid_Algorithm(map, bombs, explosions, enemys), enemys)
            elif self.algorithm is Algorithm.DFS:
                self.DFS(self.create_grid_Algorithm(map, bombs, explosions, enemys), enemys)
        else:
            self.direction = self.directions_path[0]
            self.move(map, bombs, explosions, enemys)

    def Astar(self, grid, enemys, targetNode = None, destinationNode = None):
        openList = []
        closed = []
        startNode = grid[int(self.posX / 4)][int(self.posY / 4)]
        openList.append(startNode)
        if destinationNode is None or targetNode is None:
            targetNode, destinationNode = self.determineTarget(grid, enemys)
        #print("newTarget: ", targetNode.x, targetNode.y, "newDestination: ", destinationNode.x, destinationNode.y)
        found = False
        while True:
            if len(openList) == 0:
                return False
            current = self.findSmallestFx(openList)
            openList.remove(current)
            closed.append(current)

            if current == destinationNode:
                found = True
                break

            neighbours = self.getNeighbours(grid, current)

            for neighbour in neighbours:
                if neighbour in closed:
                    continue

                if neighbour.parent is None:
                    neighbour.parent = current
                newGx = self.findGx(neighbour, startNode)

                if newGx < neighbour.gx or neighbour not in openList:
                    neighbour.gx = newGx
                    neighbour.hx = self.findHx(neighbour, targetNode)
                    neighbour.fx = neighbour.gx + neighbour.hx
                    neighbour.parent = current
                    if neighbour not in openList:
                        openList.append(neighbour)

        if found:
            self.path.clear()
            tmp = destinationNode
            self.path.append([tmp.x, tmp.y])

            #Path
            while tmp.parent is not None:
                self.path.append([tmp.parent.x, tmp.parent.y])
                tmp = tmp.parent
            self.path.reverse()

            #Directions Path
            self.directions_path.clear()
            if len(self.path) > 1:
                if self.path[1][1] - int(self.posY / 4) == 1:
                    self.directions_path.append(0)
                elif self.path[1][0] - int(self.posX /4) == 1:
                    self.directions_path.append(1)
                elif self.path[1][1] - int(self.posY / 4) == -1:
                    self.directions_path.append(2)
                elif self.path[1][0] - int(self.posX / 4) == -1:
                    self.directions_path.append(3)
                else:
                    self.directions_path.append(random.randint(0, 3))
            else:
                if self.bomb_limit > 0:
                    self.plant = True
                    grid[targetNode.x][targetNode.y].prio = 0
            return True

    def create_grid_Algorithm(self, map, bombs, explosions, enemys):
        grid = [[None] * len(map) for r in range(len(map))]
        # 0 - safe
        # 1 - destroyable
        # 2 - unreachable
        # 3 - unsafe
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    grid[i][j] = NodeA(i, j, True, 0)
                elif map[i][j] == 1:
                    grid[i][j] = NodeA(i, j, False, -1)
                elif map[i][j] == 2:
                    grid[i][j] = NodeA(i, j, False, 2)
                elif map[i][j] == 3:
                    grid[i][j] = NodeA(i, j, False, -1)

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]].reach = False

        for x in enemys:
            if not x.life:
                continue
            else:
                grid[int(x.posX / 4)][int(x.posY / 4)].reach = False
                grid[int(x.posX / 4)][int(x.posY / 4)].prio = 3
                grid[int(x.posX / 4) + 1][int(x.posY / 4)].reach = False
                grid[int(x.posX / 4) - 1][int(x.posY / 4)].reach = False
                grid[int(x.posX / 4)][int(x.posY / 4) + 1].reach = False
                grid[int(x.posX / 4)][int(x.posY / 4) - 1].reach = False

        for b in bombs:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]].prio = -1
            grid[b.posX][b.posY].reach = False

        if len(bombs) > 0:
            if grid[int(self.posX / 4)][int(self.posY / 4)].prio != -1:
                self.avoidExplosion = True
            else:
                self.avoidExplosion = False

            for b in bombs:
                if self.avoidExplosion is True and b.time < 700:
                    for x in b.sectors:
                        grid[x[0]][x[1]].reach = False

        return grid

    def findHx(self, node, targetNode):
        hx = abs(node.x - targetNode.x) + abs(node.y - targetNode.y)
        return hx

    def findGx(self, node, startNode):
            return node.parent.gx + 1

    def getNeighbours(self, grid, current):
        neighbours = []
        if grid[current.x][current.y + 1].reach is True:
            neighbours.append(grid[current.x][current.y + 1])
        if grid[current.x + 1][current.y].reach is True:
            neighbours.append(grid[current.x + 1][current.y])
        if grid[current.x][current.y - 1].reach is True:
            neighbours.append(grid[current.x][current.y - 1])
        if grid[current.x - 1][current.y].reach is True:
            neighbours.append(grid[current.x - 1][current.y])
        return neighbours

    def determineTarget(self, grid, enemys):
        currentTarget = None
        currentDestination = None
        detectorRange = 2
        while True:
            currentTarget, currentDestination = self.findEnemy(grid, detectorRange, enemys)
            if currentTarget is None or currentDestination is None:
                currentTarget, currentDestination = self.findBlock(grid, detectorRange, enemys)

            if currentTarget is not None and currentDestination is not None:
                break
            else:
                if detectorRange < len(grid):
                    detectorRange += 1
                else:
                    while True:
                        x = random.randint(1, 12)
                        y = random.randint(1, 12)
                        if abs(x - self.posX) > 3 and abs(y - self.posY) > 3:
                            currentDestination = grid[x][y]
                            currentTarget = currentDestination
                            break
                    break

        return currentTarget, currentDestination

    def findBlock(self, grid, detectorRange, enemys):
        gridPosX = int(self.posX / 4)
        gridPosY = int(self.posY / 4)
        currentTarget = None
        currentDestination = None
        smallestRange = 999
        for i in range(-detectorRange, detectorRange + 1):
            for j in range(-detectorRange, detectorRange + 1):
                if gridPosX + i >= 1 and gridPosX + i < len(grid) - 1 and gridPosY + j >= 1 and gridPosY + j < len(grid) - 1:
                    if grid[gridPosX + i][gridPosY + j].prio == 2:
                        tempRange = self.findHx(grid[gridPosX][gridPosY], grid[gridPosX + i][gridPosY + j])
                        if tempRange < smallestRange:
                            tempDestination, isAccess = self.isAccessible(grid, grid[gridPosX + i][gridPosY + j])
                            if isAccess is True:
                                if self.algorithm == Algorithm.ASTAR:
                                    fieldNotBlocked = self.Astar(grid, enemys, grid[gridPosX + i][gridPosY + j], tempDestination)
                                elif self.algorithm == Algorithm.BFS:
                                    fieldNotBlocked = self.BFS(grid, enemys, grid[gridPosX + i][gridPosY + j], tempDestination)
                                elif self.algorithm == Algorithm.DFS:
                                    fieldNotBlocked = self.DFS(grid, enemys, grid[gridPosX + i][gridPosY + j], tempDestination)
                                if fieldNotBlocked is True:
                                    smallestRange = tempRange
                                    currentTarget = grid[gridPosX + i][gridPosY + j]
                                    currentDestination = tempDestination
                                else:
                                    continue
                            else:
                                continue
        return currentTarget, currentDestination

    def findEnemy(self, grid, detectorRange, enemys):
        gridPosX = int(self.posX / 4)
        gridPosY = int(self.posY / 4)
        currentTarget = None
        currentDestination = None
        smallestRange = 999
        for i in range(-detectorRange, detectorRange + 1):
            for j in range(-detectorRange, detectorRange + 1):
                if gridPosX + i >= 1 and gridPosX + i < len(grid) - 1 and gridPosY + j >= 1 and gridPosY + j < len(grid) - 1:
                     if grid[gridPosX + i][gridPosY + j].prio == 3:
                        enemyDir = -1
                        for enemy in enemys:
                            if (int(enemy.posX / 4) == gridPosX + i) and (int(enemy.posY / 4) == gridPosY + j):
                                enemyDir = enemy.direction
                                targetCandidate = grid[gridPosX + i][gridPosY + j]
                                if (enemyDir == 0) and ((gridPosY + j + 2) < len(grid) - 1):
                                    destinationCandidate = grid[gridPosX + i][gridPosY + j + 2]
                                elif (enemyDir == 1) and ((gridPosX + i + 2) < len(grid) - 1):
                                    destinationCandidate = grid[gridPosX + i + 2][gridPosY + j]
                                elif (enemyDir == 2) and ((gridPosY + j - 2) >= 1):
                                    destinationCandidate = grid[gridPosX + i][gridPosY + j - 2]
                                elif (enemyDir == 3) and ((gridPosX + i - 2) >= 1):
                                    destinationCandidate = grid[gridPosX + i - 2][gridPosY + j]
                                else:
                                    enemyDir = -1
                                break
                        if enemyDir != -1:
                            tempRange = self.findHx(grid[gridPosX][gridPosY], destinationCandidate)
                            if tempRange < smallestRange:
                                if destinationCandidate.prio == 0:
                                    if self.algorithm == Algorithm.ASTAR:
                                        fieldNotBlocked = self.Astar(grid, enemys, grid[gridPosX + i][gridPosY + j], destinationCandidate)
                                    elif self.algorithm == Algorithm.BFS:
                                        fieldNotBlocked = self.BFS(grid, enemys, grid[gridPosX + i][gridPosY + j], destinationCandidate)
                                    elif self.algorithm == Algorithm.DFS:
                                        fieldNotBlocked = self.DFS(grid, enemys, grid[gridPosX + i][gridPosY + j], destinationCandidate)
                                    if fieldNotBlocked is True:
                                        smallestRange = tempRange
                                        currentTarget = targetCandidate
                                        currentDestination = destinationCandidate
                                    else:
                                        continue
                                else:
                                    continue

        return currentTarget, currentDestination

    def isAccessible(self, grid, currentTarget):
        gridPosX = int(self.posX / 4)
        gridPosY = int(self.posY / 4)
        currentDestination = None
        currentNode = grid[gridPosX][gridPosY]
        neighbour1 = grid[currentTarget.x + 1][currentTarget.y]
        neighbour2 = grid[currentTarget.x - 1][currentTarget.y]
        neighbour3 = grid[currentTarget.x][currentTarget.y + 1]
        neighbour4 = grid[currentTarget.x][currentTarget.y - 1]
        smallestRange = 999
        if neighbour1.prio == 0:
            tempRange = self.findHx(currentNode, neighbour1)
            if tempRange < smallestRange:
                currentDestination = neighbour1
                smallestRange = tempRange
        if neighbour2.prio == 0:
            tempRange = self.findHx(currentNode, neighbour2)
            if tempRange < smallestRange:
                currentDestination = neighbour2
                smallestRange = tempRange
        if neighbour3.prio == 0:
            tempRange = self.findHx(currentNode, neighbour3)
            if tempRange < smallestRange:
                currentDestination = neighbour3
                smallestRange = tempRange
        if neighbour4.prio == 0:
            tempRange = self.findHx(currentNode, neighbour4)
            if tempRange < smallestRange:
                currentDestination = neighbour4
                smallestRange = tempRange
        if currentDestination is not None:
            isAccess = True
        else:
            isAccess = False
        return currentDestination, isAccess

    def findSmallestFx(self, openList):
        smallest = openList[0]
        for node in openList:
            if node.fx < smallest.fx:
                smallest = node
            elif node.fx == smallest.fx:
                if node.hx < smallest.hx:
                    smallest = node
        return smallest

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

    def DFS(self, grid, enemys, targetNode = None, destinationNode = None):
        found = False
        open = list()
        visited = list()
        rootNode = grid[int(self.posX / 4)][int(self.posY / 4)]
        open.append(rootNode)
        if destinationNode is None or targetNode is None:
            targetNode, destinationNode = self.determineTarget(grid, enemys)
        while len(open) > 0:
            currentNode = open.pop()
            visited.append(currentNode)
            if currentNode == destinationNode:
                found = True
                break

            for neighbour in self.getNeighbours(grid, currentNode):
                if neighbour not in visited and neighbour not in open:
                    open.append(neighbour)
                    neighbour.parent = currentNode

        if found is True:
            self.path.clear()
            tmp = destinationNode
            self.path.append([tmp.x, tmp.y])

            # Path
            while tmp.parent is not None:
                self.path.append([tmp.parent.x, tmp.parent.y])
                tmp = tmp.parent
            self.path.reverse()

            # Directions Path
            self.directions_path.clear()
            if len(self.path) > 1:
                if self.path[1][1] - int(self.posY / 4) == 1:
                    self.directions_path.append(0)
                elif self.path[1][0] - int(self.posX / 4) == 1:
                    self.directions_path.append(1)
                elif self.path[1][1] - int(self.posY / 4) == -1:
                    self.directions_path.append(2)
                elif self.path[1][0] - int(self.posX / 4) == -1:
                    self.directions_path.append(3)
                else:
                    self.directions_path.append(random.randint(0, 3))
            else:
                if self.bomb_limit > 0:
                    self.plant = True
                    grid[targetNode.x][targetNode.y].prio = 0
            return True
        else:
            return False

    def BFS(self, grid, enemys, targetNode = None, destinationNode = None):
        found = False
        open = list()
        visited = list()
        rootNode = grid[int(self.posX / 4)][int(self.posY / 4)]
        open.append(rootNode)
        if destinationNode is None or targetNode is None:
           targetNode, destinationNode = self.determineTarget(grid, enemys)
        while len(open) > 0:
            currentNode = open.pop(0)
            visited.append(currentNode)
            if currentNode == destinationNode:
                found = True
                break
            for neighbour in self.getNeighbours(grid, currentNode):
                if neighbour not in visited and neighbour not in open:
                    open.append(neighbour)
                    neighbour.parent = currentNode

        if found is True:
            self.path.clear()
            tmp = destinationNode
            self.path.append([tmp.x, tmp.y])

            # Path
            while tmp.parent is not None:
                self.path.append([tmp.parent.x, tmp.parent.y])
                tmp = tmp.parent
            self.path.reverse()

            # Directions Path
            self.directions_path.clear()
            if len(self.path) > 1:
                if self.path[1][1] - int(self.posY / 4) == 1:
                    self.directions_path.append(0)
                elif self.path[1][0] - int(self.posX / 4) == 1:
                    self.directions_path.append(1)
                elif self.path[1][1] - int(self.posY / 4) == -1:
                    self.directions_path.append(2)
                elif self.path[1][0] - int(self.posX / 4) == -1:
                    self.directions_path.append(3)
                else:
                    self.directions_path.append(random.randint(0, 3))
            else:
                if self.bomb_limit > 0:
                    self.plant = True
                    grid[targetNode.x][targetNode.y].prio = 0
            return True
        else:
            return False

    def playerMove(self, dx, dy, grid, enemys):
        tempx = int(self.posX/4)
        tempy = int(self.posY/4)

        map = []

        for i in range(len(grid)):
            map.append([])
            for j in range(len(grid[i])):
                map[i].append(grid[i][j])

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                map[int(x.posX/4)][int(x.posY/4)] = 2

        if self.posX % 4 != 0 and dx == 0:
            if self.posX % 4 == 1:
                self.posX -= 1
            elif self.posX % 4 == 3:
                self.posX += 1
            return
        if self.posY % 4 != 0 and dy == 0:
            if self.posY % 4 == 1:
                self.posY -= 1
            elif self.posY % 4 == 3:
                self.posY += 1
            return

        # right
        if dx == 1:
            if map[tempx+1][tempy] == 0:
                self.posX += 1
        # left
        elif dx == -1:
            tempx = math.ceil(self.posX / 4)
            if map[tempx-1][tempy] == 0:
                self.posX -= 1

        # bottom
        if dy == 1:
            if map[tempx][tempy+1] == 0:
                self.posY += 1
        # top
        elif dy == -1:
            tempy = math.ceil(self.posY / 4)
            if map[tempx][tempy-1] == 0:
                self.posY -= 1

    def plant_bomb(self, map):
        b = Bomb(self.range, round(self.posX/4), round(self.posY/4), map, self)
        self.bomb_limit -= 1
        return b

    def check_death(self, exp, enemy_list):
        for e in exp:
            for s in e.sectors:
                if int(self.posX/4) == s[0] and int(self.posY/4) == s[1]:
                    self.life = False
        for en in enemy_list:
            if en.life is True:
                if abs(self.posX - en.posX) <= 2 and abs(self.posY - en.posY) <= 2:
                    self.life = False
                    return

    def load_animations(self, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        f1 = pygame.image.load('images/hero/pf0.png')
        f2 = pygame.image.load('images/hero/pf1.png')
        f3 = pygame.image.load('images/hero/pf2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load('images/hero/pr0.png')
        r2 = pygame.image.load('images/hero/pr1.png')
        r3 = pygame.image.load('images/hero/pr2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load('images/hero/pb0.png')
        b2 = pygame.image.load('images/hero/pb1.png')
        b3 = pygame.image.load('images/hero/pb2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load('images/hero/pl0.png')
        l2 = pygame.image.load('images/hero/pl1.png')
        l3 = pygame.image.load('images/hero/pl2.png')

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
