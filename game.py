import pygame
import sys
import random
import pygame.mixer

# from enums.power_up_type import PowerUpType
from player import Player
from put_out_fires import Put_out_fires
from Friend import Friend
from enums.algorithm import Algorithm

# from power_up import PowerUp

BACKGROUND_COLOR = (255, 255, 0)  # фон поля ОКНА
game_over_image = pygame.image.load("game_over_image.jpg")
font = None

pygame.mixer.init()
music1 = pygame.mixer.Sound('Rovio.mp3')
music2 = pygame.mixer.Sound('game_over.mp3')

player = None
friend_list = []
ene_blocks = []
barrels = []
Put_out_firess = []
power_ups = []
# создаем поле
GRID_BASE = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def game_init(surface, path, player_alg, en1_alg, en2_alg, en3_alg, scale):
    global font
    font = pygame.font.SysFont('Bebas', 50)
    music1.play()

    global friend_list
    global ene_blocks
    global player

    friend_list = []
    ene_blocks = []
    global Put_out_firess
    global barrels
    global power_ups
    barrels.clear()
    Put_out_firess.clear()
    power_ups.clear()

    player = Player()

    if en1_alg is not Algorithm.NONE:
        en1 = Friend(11, 11, en1_alg)
        en1.load_animations('1', scale)
        friend_list.append(en1)
        ene_blocks.append(en1)

    if en2_alg is not Algorithm.NONE:
        en2 = Friend(1, 11, en2_alg)
        en2.load_animations('2', scale)
        friend_list.append(en2)
        ene_blocks.append(en2)

    if en3_alg is not Algorithm.NONE:
        en3 = Friend(11, 1, en3_alg)
        en3.load_animations('3', scale)
        friend_list.append(en3)
        ene_blocks.append(en3)

    if player_alg is Algorithm.PLAYER:
        player.load_animations(scale)
        ene_blocks.append(player)
    elif player_alg is not Algorithm.NONE:
        en0 = Friend(1, 1, player_alg)
        en0.load_animations('', scale)
        friend_list.append(en0)
        ene_blocks.append(en0)
        player.life = False
    else:
        player.life = False

    grass_img = pygame.image.load('images/terrain/grass.png')
    grass_img = pygame.transform.scale(grass_img, (scale, scale))

    block_img = pygame.image.load('images/terrain/block.png')
    block_img = pygame.transform.scale(block_img, (scale, scale))

    box_img = pygame.image.load('images/terrain/box.png')
    box_img = pygame.transform.scale(box_img, (scale, scale))

    water1_img = pygame.image.load('images/water/1.png')
    water1_img = pygame.transform.scale(water1_img, (scale, scale))

    water2_img = pygame.image.load('images/water/2.png')
    water2_img = pygame.transform.scale(water2_img, (scale, scale))

    water3_img = pygame.image.load('images/water/3.png')
    water3_img = pygame.transform.scale(water3_img, (scale, scale))

    Put_out_fires1_img = pygame.image.load('images/Put_out_fires/1.png')
    Put_out_fires1_img = pygame.transform.scale(Put_out_fires1_img, (scale, scale))

    Put_out_fires2_img = pygame.image.load('images/Put_out_fires/2.png')
    Put_out_fires2_img = pygame.transform.scale(Put_out_fires2_img, (scale, scale))

    Put_out_fires3_img = pygame.image.load('images/Put_out_fires/3.png')
    Put_out_fires3_img = pygame.transform.scale(Put_out_fires3_img, (scale, scale))

    terrain_images = [grass_img, block_img, box_img, grass_img]
    water_images = [water1_img, water2_img, water3_img]
    Put_out_fires_images = [Put_out_fires1_img, Put_out_fires2_img, Put_out_fires3_img]

    power_up_water_img = pygame.image.load('images/power_up/water.png')
    power_up_water_img = pygame.transform.scale(power_up_water_img, (scale, scale))

    power_up_fire_img = pygame.image.load('images/power_up/fire.png')
    power_up_fire_img = pygame.transform.scale(power_up_fire_img, (scale, scale))

    power_ups_images = [power_up_water_img, power_up_fire_img]

    main(surface, scale, path, terrain_images, water_images, Put_out_fires_images, power_ups_images)


def draw(s, grid, tile_size, show_path, game_ended, terrain_images, water_images, Put_out_fires_images,
         power_ups_images):
    s.fill(BACKGROUND_COLOR)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            s.blit(terrain_images[grid[i][j]], (i * tile_size, j * tile_size, tile_size, tile_size))

    for pu in power_ups:
        s.blit(power_ups_images[pu.type.value], (pu.pos_x * tile_size, pu.pos_y * tile_size, tile_size, tile_size))

    for x in barrels:
        s.blit(water_images[x.frame], (x.pos_x * tile_size, x.pos_y * tile_size, tile_size, tile_size))

    for y in Put_out_firess:
        for x in y.sectors:
            s.blit(Put_out_fires_images[y.frame], (x[0] * tile_size, x[1] * tile_size, tile_size, tile_size))
    if player.life:
        s.blit(player.animation[player.direction][player.frame],
               (player.pos_x * (tile_size / 4), player.pos_y * (tile_size / 4), tile_size, tile_size))
    for en in friend_list:
        if en.life:
            s.blit(en.animation[en.direction][en.frame],
                   (en.pos_x * (tile_size / 4), en.pos_y * (tile_size / 4), tile_size, tile_size))
            if show_path:
                if en.algorithm == Algorithm.friend_2:
                    for sek in en.path:
                        pygame.draw.rect(s, (255, 0, 0, 240),
                                         [sek[0] * tile_size, sek[1] * tile_size, tile_size, tile_size], 1)
                else:
                    for sek in en.path:
                        pygame.draw.rect(s, (255, 0, 255, 240),
                                         [sek[0] * tile_size, sek[1] * tile_size, tile_size, tile_size], 1)

    if game_ended:
        music1.stop()
        music2.play()
        tf = font.render("GAME OVER !!!", False, (255, 255, 0))
        tf1 = font.render("Press ESC to go back to menu", False, (255, 255, 255))
        scaled_image = pygame.transform.scale(game_over_image, (1000, 700))
        s.blit(scaled_image, (0, 0))
        s.blit(tf, (350, 200))
        s.blit(tf1, (200, 300))
    pygame.display.update()


# заполнение карты урнами с огнем
def generate_map(grid):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 3:  # регулирует заполненность поля ящиками
                grid[i][j] = 2

    return


# основной цикл игры
def main(s, tile_size, show_path, terrain_images, water_images, Put_out_fires_images, power_ups_images):
    grid = [row[:] for row in GRID_BASE]
    generate_map(grid)

    clock = pygame.time.Clock()

    running = True
    game_ended = False
    while running:
        dt = clock.tick(10)  # время в миллисекундах, прошедшее с предыдущего кадра
        for en in friend_list:
            en.make_move(grid, barrels, Put_out_firess, ene_blocks)
        if player.life:
            keys = pygame.key.get_pressed()
            temp = player.direction
            movement = False
            if keys[pygame.K_DOWN]:
                temp = 0
                player.move(0, 1, grid, ene_blocks, power_ups)
                movement = True
            elif keys[pygame.K_RIGHT]:
                temp = 1
                player.move(1, 0, grid, ene_blocks, power_ups)
                movement = True
            elif keys[pygame.K_UP]:
                temp = 2
                player.move(0, -1, grid, ene_blocks, power_ups)
                movement = True
            elif keys[pygame.K_LEFT]:
                temp = 3
                player.move(-1, 0, grid, ene_blocks, power_ups)
                movement = True
            if temp != player.direction:
                player.frame = 0
                player.direction = temp
            if movement:
                if player.frame == 2:
                    player.frame = 0
                else:
                    player.frame += 1

        draw(s, grid, tile_size, show_path, game_ended, terrain_images, water_images, Put_out_fires_images,
             power_ups_images)

        if not game_ended:
            game_ended = check_end_game()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if player.barrel_limit == 0 or not player.life:
                        continue
                    temp_water = player.plant_water(grid)
                    barrels.append(temp_water)
                    grid[temp_water.pos_x][temp_water.pos_y] = 3
                    player.barrel_limit -= 1
                elif e.key == pygame.K_ESCAPE:
                    running = False

        update_barrels(grid, dt)

    Put_out_firess.clear()
    friend_list.clear()
    ene_blocks.clear()
    power_ups.clear()


def update_barrels(grid, dt):
    for b in barrels:
        b.update(dt)
        if b.time < 1:
            b.fireman.barrel_limit += 1
            grid[b.pos_x][b.pos_y] = 0
            exp_temp = Put_out_fires(b.pos_x, b.pos_y, b.range)
            exp_temp.explode(grid, barrels, b, power_ups)
            exp_temp.clear_sectors(grid, random, power_ups)
            Put_out_firess.append(exp_temp)
    if player not in friend_list:
        player.check_death(Put_out_firess)
    for en in friend_list:
        en.check_death(Put_out_firess)
    for e in Put_out_firess:
        e.update(dt)
        if e.time < 1:
            Put_out_firess.remove(e)


def check_end_game():
    if not player.life:
        return True

    for en in friend_list:
        if en.life:
            return False

    return True
