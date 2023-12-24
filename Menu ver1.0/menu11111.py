import pygame
import pygame_menu


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (100, 0, 153, 0)

MENU_TITLE_COLOR = (255, 255, 0, 0)
WINDOW_SCALE = 0.4

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.045)
WINDOW_SIZE = (30 * TILE_SIZE, 20 * TILE_SIZE)

surface = pygame.display.set_mode(WINDOW_SIZE)


def run_game():
    game.game_init()


def main_background():
    global surface
    # Загрузка изображения для фона
    background_image = pygame.image.load('fire_background.jpg')
    # Масштабирование изображения до размера окна
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
    # Отображение изображения на поверхности
    surface.blit(background_image, (0, 0))


def menu_loop():
    pygame.init()

    pygame.display.set_caption('Water and fire')

    menu_theme = pygame_menu.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame.font.Font('BetaDance.ttf', 40),
        title_font_size=TILE_SIZE,
        title_font_color=(255, 255, 255),
        title_font=pygame.font.Font('BetaDance.ttf',100),
        widget_font_color=(255, 255, 0),
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Play menu'
    )

    play_menu.add.button('Start',
                         run_game)

    play_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame.font.Font('BetaDance.ttf',20),
        title_font_size=TILE_SIZE,
        title_font_color=(255,255,255),
        title_font=pygame.font.Font('BetaDance.ttf',100),
        widget_font_color=(255,255,0),
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR
    )

    about_menu = pygame_menu.Menu(
        theme=about_menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        overflow=False,
        title='   About'
    )
    about_menu.add.label("Authors: Shumakova Yana")
    about_menu.add.vertical_margin(10)
    about_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='   Menu'
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    running = True
    while running:


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
