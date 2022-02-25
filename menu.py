import pygame
import pygame_menu
import game
from algorithm import Algorithm

COLOR_BACKGROUND = (153, 153, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (102, 102, 153)
MENU_TITLE_COLOR = (51, 51, 255)

pygame.display.init()
TILE_SIZE = 50
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)

clock = None
player_alg = Algorithm.ASTAR
show_path = True
surface = pygame.display.set_mode(WINDOW_SIZE)


def change_path(value, c):
    global show_path
    show_path = c


def change_player(value, c):
    global player_alg
    player_alg = c


def run_game():
    game.game_init(show_path, player_alg, TILE_SIZE)


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def menu_loop():
    pygame.init()

    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()

    menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=int(TILE_SIZE*0.8),
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE*0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        #widget_shadow=False
    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        onclose=pygame_menu.events.NONE,
        title='Play menu'
    )

    play_options = pygame_menu.Menu(theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        title='Options'
    )
    play_options.add.selector("AI   Player", [("ASTAR", Algorithm.ASTAR), ("BFS", Algorithm.BFS), ("DFS", Algorithm.DFS),  ("Player", Algorithm.PLAYER),
                                              ("None", Algorithm.NONE)], onchange=change_player)
    play_options.add.selector("Show path", [("Yes", True), ("No", False)], onchange=change_path)

    play_options.add.button('Back', pygame_menu.events.BACK)
    play_menu.add.button('Start',
                         run_game)

    play_menu.add.button('Options', play_options)
    play_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE*0.4),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        #widget_shadow=False
    )

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.6),
        width=int(WINDOW_SIZE[0] * 0.6),
        onclose=pygame_menu.events.NONE,
        title='Main menu'
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    while True:

        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        main_menu.mainloop(surface, main_background, le_loop=False, fps_limit=0)
        main_menu.update(events)
        main_menu.draw(surface)

        pygame.display.flip()


menu_loop()
