from os.path import join, isfile
from os import listdir

import pygame
from platformClass import Platform, PlayerPlatform, Object
from playerClass import Player

WINDOW_WIDTH, WINDOW_HEIGHT = 1728, 960
FPS = 60
PLAYER_SPEED = 8

pygame.display.set_caption("Bonehead")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

"""Flips the sprites on x axis"""
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


"""Creates a tiled background from name in assets/world/"""
def get_background(name):
    image = pygame.image.load(join("assets", "world", name))
    image = pygame.transform.scale_by(image, 4)
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WINDOW_WIDTH // width + 1):
        for j in range(WINDOW_HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

"""Renderer"""
def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)

    for object in objects:
        object.draw(window)

    player.draw(window)
    pygame.display.update()


def vertical_collision(player, objects, y_velocity):
    collided_objects = []
    for object in objects:
        if pygame.sprite.collide_mask(player,object):
            if y_velocity > 0:
                player.rect.bottom = object.rect.top
                player.landed()
            elif y_velocity < 0:
                player.rect.top = object.rect.bottom
                player.hit_head()
        collided_objects.append(object)

    return collided_objects


def collide(player, objects, x):
    player.move(x,0)
    player.update()
    collided_object = None
    for object in objects:
        if pygame.sprite.collide_mask(player, object):
            collided_object = object

    player.move(-x,0)
    player.update()
    return collided_object


def move(player, objects):
    keys = pygame.key.get_pressed()
    collide_left = collide(player, objects, -PLAYER_SPEED * 1.2)
    collide_right = collide(player, objects, PLAYER_SPEED * 1.2)

    player.x_vel = 0
    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_SPEED)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_SPEED)

    vertical_collision(player, objects, player.y_vel)


def is_overlapping(platforms, new_platform):
    for platform in platforms:
        if platform.rect.colliderect(new_platform):
            return True
    return False

def create_platform(player, size):
    return PlayerPlatform(player.rect.x+24, player.rect.y+80, size)

def respawn(player):
    # do an animation here
    player.x_vel = 0
    player.y_vel = 0
    player.rect.x = player.initial_x
    player.rect.y = player.initial_y

def build_level1(platforms, platform_size):
    platforms.clear()

    for i in range(0, WINDOW_WIDTH //platform_size):
        platforms.append(Platform(i * platform_size, WINDOW_HEIGHT - platform_size, platform_size))
    for i in range(0, WINDOW_HEIGHT // platform_size):
        platforms.append(Platform(WINDOW_WIDTH - platform_size, i * platform_size, platform_size))
        platforms.append(Platform(0, i * platform_size, platform_size))
    for i in range (3, (WINDOW_WIDTH// platform_size) - 1):
        platforms.append(Platform(i * platform_size, 0, platform_size))
    # draws from the top left corner, (0,0) = top left, (18,9) = bottom right
    # its so uglyyy
    #first part
    for i in range(4,9):
        platforms.append(Platform(platform_size * 4, platform_size * i, platform_size))
    for i in range(1,7):
        platforms.append(Platform(platform_size * i, platform_size * 2, platform_size))
    platforms.append(Platform(platform_size * 3, platform_size * 5, platform_size))
    platforms.append(Platform(platform_size * 3, platform_size * 7, platform_size))
    platforms.append(Platform(platform_size * 5, platform_size * 5, platform_size))
    platforms.append(Platform(platform_size * 8, platform_size * 8, platform_size))
    platforms.append(Platform(platform_size * 9, platform_size * 8, platform_size))
    #second part
    platforms.append(Platform(platform_size * 6, platform_size * 3, platform_size))
    platforms.append(Platform(platform_size * 7, platform_size * 4, platform_size))
    platforms.append(Platform(platform_size * 8, platform_size * 4, platform_size))
    for i in range (9,12):
        platforms.append(Platform(platform_size * i, platform_size * 3, platform_size))
    for i in range(5,9):
        platforms.append(Platform(platform_size * 10, platform_size * i, platform_size))
    #third part
    for i in range(2,6):
        platforms.append(Platform(platform_size * 12, platform_size * i, platform_size))
    platforms.append(Platform(platform_size * 15, platform_size * 6, platform_size))
    platforms.append(Platform(platform_size * 16, platform_size * 8, platform_size))
    platforms.append(Platform(platform_size * 16, platform_size * 3, platform_size))
    for i in range(14,17):
        platforms.append(Platform(platform_size * i, platform_size * 4, platform_size))

    return

def level_select(number):

    base =  [[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


    if number == 1:
        return base

def build_level(array, platform_size):
    # iterate through array, if indexval = 1, draw platform there
    return


def main(screen):
    pygame.init()
    clock = pygame.time.Clock()

    platform_size = 96
    head_size = 48
    platforms = []
    build_level1(platforms, platform_size)

    background, bg_image = get_background("backgroundBricks.png")
    # player spawn location
    player = Player(platform_size*1,WINDOW_HEIGHT- platform_size,40,80)


    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # jump handler, can do multi jump if want, glitchy
                if event.key == pygame.K_w and player.jump_count < 1:
                    player.jump()
                # place a skull
                if event.key == pygame.K_SPACE:
                    newPlatform = create_platform(player, head_size)
                    if not is_overlapping(platforms, newPlatform):
                        platforms.append(newPlatform)
                        player.skull_count += 1
                        #respawn(player)
                # reset the world
                if event.key == pygame.K_r:
                    build_level1(platforms, platform_size)
                    player.skull_count = 0
                    respawn(player)

        player.loop(FPS)
        move(player, platforms)
        draw(screen, background , bg_image, player, platforms)


if __name__ == "__main__":
    main(screen)
