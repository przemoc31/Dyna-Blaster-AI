import pygame
import pygame_menu
import sys
import random
import time
import pandas as pd
from player import Player
from explosion import Explosion
from enemy import Enemy
from algorithm import Algorithm

startTimer = 0
endTimer = 0
gameCounter = 0
totalDuration = 0
averageDuration = 0
wonGames = 0
linesToSkip = 1

TILE_WIDTH = 40
TILE_HEIGHT = 40

WINDOW_WIDTH = 13 * TILE_WIDTH
WINDOW_HEIGHT = 13 * TILE_HEIGHT

BACKGROUND = (107, 142, 35) #RGB prawdopodobnie

s = None
show_path = True

clock = None

player = None
player2 = None
enemy_list = []
ene_blocks = []
bombs = []
explosions = []

grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

grass_img = None
block_img = None
box_img = None
bomb1_img = None
bomb2_img = None
bomb3_img = None
explosion1_img = None
explosion2_img = None
explosion3_img = None


terrain_images = []
bomb_images = []
explosion_images = []

pygame.font.init()
font = pygame.font.SysFont('Bebas', 30)
TEXT_LOSE = font.render('GAME OVER', False, (0, 0, 0))
TEXT_WIN = font.render('WIN', False, (0, 0, 0))

COLOR_BACKGROUND = (153, 153, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (102, 102, 153)
MENU_TITLE_COLOR = (51, 51, 255)

pygame.display.init()
TILE_SIZE = 50
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)
surface = pygame.display.set_mode(WINDOW_SIZE)


def game_init(path, player_alg, scale):
    global startTimer
    startTimer = time.time()

    global TILE_WIDTH
    global TILE_HEIGHT
    TILE_WIDTH = scale
    TILE_HEIGHT = scale

    global font
    font = pygame.font.SysFont('Bebas', scale)

    global show_path
    show_path = path

    global s
    s = pygame.display.set_mode((13 * TILE_WIDTH, 13 * TILE_HEIGHT))
    pygame.display.set_caption('Bomberman')

    global clock
    clock = pygame.time.Clock()

    global enemy_list
    global ene_blocks
    global player
    global player2

    enemy_list = []
    ene_blocks = []
    global explosions
    global bombs
    bombs.clear()
    explosions.clear()

    player = Player(1, 1, player_alg)
    player.load_animations(scale)
    '''player2 = Player(11, 11, Algorithm.BFS)
    player2.load_animations(scale)'''

    en1 = Enemy(11, 11)
    en1.load_animations('1', scale)
    enemy_list.append(en1)
    ene_blocks.append(en1)

    en2 = Enemy(1, 11)
    en2.load_animations('1', scale)
    enemy_list.append(en2)
    ene_blocks.append(en2)

    en3 = Enemy(11, 1)
    en3.load_animations('1', scale)
    enemy_list.append(en3)
    ene_blocks.append(en3)

    global grass_img
    grass_img = pygame.image.load('images/terrain/grass.png')
    grass_img = pygame.transform.scale(grass_img, (TILE_WIDTH, TILE_HEIGHT))
    global block_img
    block_img = pygame.image.load('images/terrain/block.png')
    block_img = pygame.transform.scale(block_img, (TILE_WIDTH, TILE_HEIGHT))
    global box_img
    box_img = pygame.image.load('images/terrain/box.png')
    box_img = pygame.transform.scale(box_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb1_img
    bomb1_img = pygame.image.load('images/bomb/1.png')
    bomb1_img = pygame.transform.scale(bomb1_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb2_img
    bomb2_img = pygame.image.load('images/bomb/2.png')
    bomb2_img = pygame.transform.scale(bomb2_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb3_img
    bomb3_img = pygame.image.load('images/bomb/3.png')
    bomb3_img = pygame.transform.scale(bomb3_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion1_img
    explosion1_img = pygame.image.load('images/explosion/1.png')
    explosion1_img = pygame.transform.scale(explosion1_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion2_img
    explosion2_img = pygame.image.load('images/explosion/2.png')
    explosion2_img = pygame.transform.scale(explosion2_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion3_img
    explosion3_img = pygame.image.load('images/explosion/3.png')
    explosion3_img = pygame.transform.scale(explosion3_img, (TILE_WIDTH, TILE_HEIGHT))
    global terrain_images
    terrain_images = [grass_img, block_img, box_img, grass_img]
    global bomb_images
    bomb_images = [bomb1_img, bomb2_img, bomb3_img]
    global explosion_images
    explosion_images = [explosion1_img, explosion2_img, explosion3_img]

    main()


def draw():
    s.fill(BACKGROUND)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            s.blit(terrain_images[grid[i][j]], (i * TILE_WIDTH, j * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for x in bombs:
        s.blit(bomb_images[x.frame], (x.posX * TILE_WIDTH, x.posY * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for y in explosions:
        for x in y.sectors:
            s.blit(explosion_images[y.frame], (x[0] * TILE_WIDTH, x[1] * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))
    if player.life:
        s.blit(player.animation[player.direction][player.frame],
               (player.posX * (TILE_WIDTH / 4), player.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
    if player2 is not None:
        if player2.life:
            s.blit(player2.animation[player2.direction][player2.frame],
                   (player2.posX * (TILE_WIDTH / 4), player2.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
    if show_path:
        for sek in player.path:
            pygame.draw.rect(s, (218, 112, 214, 240),
                             [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 5)
        if player2 is not None:
            for sek in player2.path:
                pygame.draw.rect(s, (204, 204, 0, 240),
                                 [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 5)
    for en in enemy_list:
        if en.life:
            s.blit(en.animation[en.direction][en.frame],
                   (en.posX * (TILE_WIDTH / 4), en.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
    pygame.display.update()


def generate_map():
    global grid
    global linesToSkip
    grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 2:
                grid[i][j] = 2

    '''grid = []
    grid2 = []
    with open("grid.txt", "r") as f:
        for _ in range(linesToSkip):
            f.readline()
        for i in range(13):
            grid.append(list(f.readline()))
    f.close()

    for i in range(13):
        for j in range(26):
            if grid[i][j] == ' ':
                continue
            else:
                grid2.append(int(grid[i][j]))
    grid = [[0] * 13 for i in range(13)]
    for i in range(13):
        for j in range(13):
            grid[i][j] = grid2.pop(0)'''

    '''with open('grid.txt', 'w') as f:
        f.write(str(13) + " " + str(13) + '\n')
        for raw in grid:
            for field in raw:
                f.write(str(field))

    linesToSkip += 14'''
    return


def check_win():
    for en in enemy_list:
        if en.life:
            return
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 2:
                return
    game_won()


def main():
    generate_map()
    if player2 is None:
        while player.life:
            dt = clock.tick(15)
            for en in enemy_list:
                en.move(grid, bombs, explosions, ene_blocks)
                en.frame += 1
                if en.frame == 3:
                    en.frame = 0
            if player.algorithm == Algorithm.PLAYER:
                keys = pygame.key.get_pressed()
                temp = player.direction
                movement = False
                if keys[pygame.K_DOWN]:
                    temp = 0
                    player.playerMove(0, 1, grid, ene_blocks)
                    movement = True
                elif keys[pygame.K_RIGHT]:
                    temp = 1
                    player.playerMove(1, 0, grid, ene_blocks)
                    movement = True
                elif keys[pygame.K_UP]:
                    temp = 2
                    player.playerMove(0, -1, grid, ene_blocks)
                    movement = True
                elif keys[pygame.K_LEFT]:
                    temp = 3
                    player.playerMove(-1, 0, grid, ene_blocks)
                    movement = True
                if temp != player.direction:
                    player.frame = 0
                    player.direction = temp

                if movement:
                    if player.frame == 2:
                        player.frame = 0
                    else:
                        player.frame += 1
            else:
                player.make_move(grid, bombs, explosions, enemy_list)
                if player.frame == 2:
                    player.frame = 0
                else:
                    player.frame += 1

            draw()
            check_win()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        if player.bomb_limit == 0:
                            continue
                        temp_bomb = player.plant_bomb(grid)
                        bombs.append(temp_bomb)
                        grid[temp_bomb.posX][temp_bomb.posY] = 3

            update_bombs(dt)
    else:
        while player.life or player2.life:
            dt = clock.tick(15)
            for en in enemy_list:
                en.move(grid, bombs, explosions, ene_blocks)
                en.frame += 1
                if en.frame == 3:
                    en.frame = 0
            if player.life:
                if player.algorithm == Algorithm.PLAYER:
                    keys = pygame.key.get_pressed()
                    temp = player.direction
                    movement = False
                    if keys[pygame.K_DOWN]:
                        temp = 0
                        player.playerMove(0, 1, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_RIGHT]:
                        temp = 1
                        player.playerMove(1, 0, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_UP]:
                        temp = 2
                        player.playerMove(0, -1, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_LEFT]:
                        temp = 3
                        player.playerMove(-1, 0, grid, ene_blocks)
                        movement = True
                    if temp != player.direction:
                        player.frame = 0
                        player.direction = temp

                    if movement:
                        if player.frame == 2:
                            player.frame = 0
                        else:
                            player.frame += 1
                else:
                    player.make_move(grid, bombs, explosions, enemy_list)
                    if player.frame == 2:
                        player.frame = 0
                    else:
                        player.frame += 1
            if player2.life:
                if player2.algorithm == Algorithm.PLAYER:
                    keys = pygame.key.get_pressed()
                    temp = player2.direction
                    movement = False
                    if keys[pygame.K_DOWN]:
                        temp = 0
                        player2.playerMove(0, 1, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_RIGHT]:
                        temp = 1
                        player2.playerMove(1, 0, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_UP]:
                        temp = 2
                        player2.playerMove(0, -1, grid, ene_blocks)
                        movement = True
                    elif keys[pygame.K_LEFT]:
                        temp = 3
                        player2.playerMove(-1, 0, grid, ene_blocks)
                        movement = True
                    if temp != player2.direction:
                        player2.frame = 0
                        player2.direction = temp

                    if movement:
                        if player2.frame == 2:
                            player2.frame = 0
                        else:
                            player2.frame += 1
                else:
                    player2.make_move(grid, bombs, explosions, enemy_list)
                    if player2.frame == 2:
                        player2.frame = 0
                    else:
                        player2.frame += 1

            draw()
            check_win()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        if player2 is None:
                            if player.bomb_limit == 0:
                                continue
                            temp_bomb = player.plant_bomb(grid)
                            bombs.append(temp_bomb)
                            grid[temp_bomb.posX][temp_bomb.posY] = 3
                        else:
                            if player.algorithm == Algorithm.PLAYER:
                                if player.bomb_limit == 0:
                                    continue
                                temp_bomb = player.plant_bomb(grid)
                                bombs.append(temp_bomb)
                                grid[temp_bomb.posX][temp_bomb.posY] = 3
                            elif player2.algorithm == Algorithm.PLAYER:
                                if player2.bomb_limit == 0:
                                    continue
                                temp_bomb = player2.plant_bomb(grid)
                                bombs.append(temp_bomb)
                                grid[temp_bomb.posX][temp_bomb.posY] = 3

            update_bombs(dt)
    game_over()


def update_bombs(dt):
    for b in bombs:
        b.update(dt)
        if b.time < 1:
            b.bomber.bomb_limit += 1
            grid[b.posX][b.posY] = 0
            exp_temp = Explosion(b.posX, b.posY, b.range)
            exp_temp.explode(grid, bombs, b)
            exp_temp.clear_sectors(grid)
            explosions.append(exp_temp)

    if player not in enemy_list:
        player.check_death(explosions, enemy_list)
    if player2 is not None:
        if player2 not in enemy_list:
            player2.check_death(explosions, enemy_list)
    for en in enemy_list:
        en.check_death(explosions)
    for e in explosions:
        e.update(dt)
        if e.time < 1:
            explosions.remove(e)


def run_game():
    game_init(show_path, player.algorithm, TILE_SIZE)


def game_over():
    global startTimer
    global endTimer
    global gameCounter
    global totalDuration
    global averageDuration
    global wonGames
    endTimer = time.time()
    gameCounter += 1
    averageDuration = totalDuration / wonGames
    if player.algorithm == Algorithm.ASTAR:
        print("Algorithm A*: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration,
              "averageDuration =", averageDuration)
    elif player.algorithm == Algorithm.BFS:
        print("Algorithm BFS: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration,
              "averageDuration =", averageDuration)
    elif player.algorithm == Algorithm.PLAYER:
        print("PLAYER: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration,
              "averageDuration =", averageDuration)
    dt = clock.tick(15)
    update_bombs(dt)

    draw()

    menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=int(TILE_SIZE * 0.8),
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        # widget_shadow=False
    )

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.4),
        width=int(WINDOW_SIZE[0] * 0.6),
        onclose=pygame_menu.events.NONE,
        title='YOU   LOST   BOOMER'
    )

    explosions.clear()
    enemy_list.clear()
    ene_blocks.clear()

    main_menu.add_button('Quit', pygame_menu.events.EXIT)
    main_menu.add_button('Play Again', run_game)

    while True:
        clock.tick(0.05*FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        main_menu.mainloop(surface, draw, disable_loop=True, fps_limit=0)
        main_menu.update(events)
        pygame.display.flip()
        time.sleep(3)
        run_game()


def game_won():
    global startTimer
    global endTimer
    global gameCounter
    global totalDuration
    global averageDuration
    global wonGames
    endTimer = time.time()
    tempTime = endTimer - startTimer
    totalDuration += tempTime
    gameCounter += 1
    wonGames += 1
    averageDuration = totalDuration / wonGames
    if player.algorithm == Algorithm.ASTAR:
        print("Algorithm A*: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration, "averageDuration =", averageDuration)
    elif player.algorithm == Algorithm.BFS:
        print("Algorithm BFS: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration, "averageDuration =", averageDuration)
    elif player.algorithm == Algorithm.PLAYER:
        print("PLAYER: game", gameCounter, "won games =", wonGames, "totalDuration =", totalDuration, "averageDuration =", averageDuration)
    dt = clock.tick(15)
    update_bombs(dt)
    draw()

    menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=int(TILE_SIZE * 0.8),
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        # widget_shadow=False
    )
    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1]*0.8),
        width=int(WINDOW_SIZE[0]*0.7),
        onclose=pygame_menu.events.NONE,
        title=''
    )
    main_menu.add.image('images/end_screen1.png',angle=0, scale=(0.7, 0.7))
    explosions.clear()
    enemy_list.clear()
    ene_blocks.clear()

    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    main_menu.add.button('Play Again', run_game)
    while True:
        clock.tick(0.05*FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        main_menu.mainloop(surface, draw, disable_loop=True, fps_limit=0)
        main_menu.update(events)
        pygame.display.flip()
        time.sleep(3)
        run_game()