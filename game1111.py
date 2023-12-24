import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fire and Water')

beta_dance_font = pygame.font.Font('BetaDance.ttf', 40)

fire_background = pygame.image.load('fire_background.jpg')
water_background = pygame.image.load('water_background.jpg')

fire_background = pygame.transform.scale(fire_background, (WIDTH, HEIGHT))
water_background = pygame.transform.scale(water_background, (WIDTH, HEIGHT))

fire_sprite = pygame.image.load('fire_sprite.gif')
fire_sprite = pygame.transform.scale(fire_sprite, (50, 50))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def main_menu():
    while True:
        screen.blit(fire_background, (0, 0))

        text_rects = []
        text_highlighted = [False, False, False]

        menu_options = ['START', 'MENU', 'EXIT']
        mx, my = pygame.mouse.get_pos()

        for idx, option in enumerate(menu_options):
            text_rect = draw_text(option, beta_dance_font, WHITE if not text_highlighted[idx] else RED, screen, 300, 200 + idx * 100)
            text_rects.append(text_rect)

        for idx, text_rect in enumerate(text_rects):
            if text_rect.collidepoint((mx, my)):
                text_highlighted = [False, False, False]
                text_highlighted[idx] = True
                screen.blit(fire_sprite, (text_rect.x - 60, text_rect.y))

                if idx == 0:  # При наведении на "Старт"
                    if click:
                        game()  # Запуск игры

                elif idx == 2:  # При наведении на "Выход"
                    if click:
                        pygame.quit()
                        sys.exit()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game():
    running = True
    while running:
        screen.blit(water_background, (0, 0))
        draw_text("Let's get started !!!", beta_dance_font, WHITE, screen, 300, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main_menu()