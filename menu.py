import pygame
import pygame_menu
import pygame.mixer

import game
from enums.algorithm import Algorithm

black = (0, 0, 0)
white = (255, 255, 255)
FPS = 70.0  # Количество кадров в секунду (60 норма для плавного и отзывчивого игрового процесса во многих играх)

MENU_TITLE_COLOR = (255, 255, 0, 100)  # фон верхней части меню и прозрачность
MENU_BACKGROUND_COLOR = (100, 0, 153, 100)  # фон нижней части меню и прозрачность
WINDOW_SCALE = 0.8  # масштаб окна меню относительно ОКНА

pygame.mixer.init()
mus_main = pygame.mixer.Sound('mus_main.mp3')

mus_main.play()
pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.04865)  # задает масштаб игрового поля внутри размера ОКНА
WINDOW_SIZE = (1000, 700)  # задает размер ОКНА

clock = None
player_alg = Algorithm.PLAYER
en1_alg = Algorithm.friend_1
en2_alg = Algorithm.friend_2
en3_alg = Algorithm.friend_1
show_path = True
surface = pygame.display.set_mode(WINDOW_SIZE)


def change_path(value, c):
    global show_path
    show_path = c


def change_player(value, c):
    global player_alg
    player_alg = c


def change_frie1(value, c):
    global en1_alg
    en1_alg = c


def change_frie2(value, c):
    global en2_alg
    en2_alg = c


def change_frie3(value, c):
    global en3_alg
    en3_alg = c


def run_game():
    mus_main.stop()
    game.game_init(surface, show_path, player_alg, en1_alg, en2_alg, en3_alg, TILE_SIZE)

# Загрузка изображения для фона
def main_background():
    global surface
    background_image = pygame.image.load('fire_background.jpg')  # Масштабирование изображения до размера окна
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)  # Отображение изображения на поверхности
    surface.blit(background_image, (0, 0))  # рисует наш рисунок поверх фона ОКНА

# создание меню
def menu_loop():
    pygame.init()

    pygame.display.set_caption('Огонь и вода')
    clock = pygame.time.Clock()

    menu_theme = pygame_menu.Theme(
        selection_color=white,  # цвет выделенного пункта меню
        widget_font=pygame.font.Font('BetaDance.ttf', 45),  # шрифт и размер шрифта основных пунктов меню
        title_font_size=TILE_SIZE,
        title_font_color=(255, 255, 255),  # цвет слов в шапке меню
        title_font=pygame.font.Font('BetaDance.ttf', 80),  # шрифт и размер шрифта в шапке меню
        widget_font_color=(255, 255, 0),  # цвет слов в меню
        widget_font_size=int(TILE_SIZE * 0.6),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,

    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Play'
    )

    play_options = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Options'
    )
    play_options.add.selector("Player 1   ",
                              [("User", Algorithm.PLAYER), ("Friend", Algorithm.friend_2), ("None", Algorithm.NONE)],
                              onchange=change_player)
    play_options.add.selector("Player 2   ", [("Friend", Algorithm.friend_1), ("None", Algorithm.NONE)],
                              onchange=change_frie1)
    play_options.add.selector("Player 3   ", [("Friend", Algorithm.friend_2), ("None", Algorithm.NONE)],
                              onchange=change_frie2)
    play_options.add.selector("Player 4   ", [("Friend", Algorithm.friend_1), ("None", Algorithm.NONE)],
                              onchange=change_frie3)
    play_options.add.selector("Show path   ", [("Yes", False), ("No", True )], onchange=change_path)

    play_options.add.button('Back', pygame_menu.events.BACK)
    play_menu.add.button('Start', run_game)

    play_menu.add.button('Options', play_options)
    play_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=white,
        widget_font=pygame.font.Font('BetaDance.ttf', 35),
        title_font_size=TILE_SIZE,
        title_font_color=(255, 255, 255),
        title_font=pygame.font.Font('BetaDance.ttf', 90),
        widget_font_color=(255, 255, 0),
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR
    )

    about_menu = pygame_menu.Menu(
        theme=about_menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        overflow=False,
        title='About'
    )
    about_menu.add.label("Player controls : ")
    about_menu.add.label("Movement : Arrows")
    about_menu.add.label("Plant barrel : Space")
    about_menu.add.label("Authors : Shumakova Yana")
    about_menu.add.vertical_margin(12)
    about_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Menu'
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    running = True
    while running:

        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background)

        pygame.display.flip()

    exit()


if __name__ == "__main__":
    menu_loop()
