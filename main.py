from os.path import join, isfile
from os import listdir

import pygame
import random
from platformClass import Platform, PlayerPlatform, Object
from playerClass import Player
from arraySolver import generateMap, randomMatrix

LEVEL_SIZE_X, LEVEL_SIZE_Y = 22,12
PLATFORM_SIZE = 80
HEAD_SIZE = 40
WINDOW_WIDTH, WINDOW_HEIGHT = LEVEL_SIZE_X*PLATFORM_SIZE, LEVEL_SIZE_Y*PLATFORM_SIZE
FPS = 60
PLAYER_SPEED = 8

pygame.display.set_caption("Bonehead")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


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


    # labels tracking player height and number of skulls used
    myfont = pygame.font.SysFont("monospace", 15)
    p_height = WINDOW_HEIGHT - player.rect.y
    height_score = myfont.render("Height: " + str(p_height + (WINDOW_HEIGHT * player.level)), 1, (255, 255, 0))
    skull_score = myfont.render("Skulls: " + str(player.skull_count), 1, (255, 255, 0))
    screen.blit(height_score, (50, 50))
    screen.blit(skull_score, (50, 70))

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
    return PlayerPlatform(player.rect.x+16, player.rect.y+64, size)

def respawn(player):
    # do an animation here
    player.x_vel = 0
    player.y_vel = 0
    player.rect.x = player.initial_x
    player.rect.y = player.initial_y


def level_select(level):

    base =  [[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,]]


    if level == 0:
        return generateMap()

    elif level == 1:
        return base

def build_level(level, platform_size):
    # iterate through array, if indexval = 1, draw platform there
    platforms = []
    matrix = level_select(level)
    for y ,row in enumerate(matrix):
        for x ,value in enumerate(row):
            if value == 1:
                platforms.append(Platform(platform_size * x, platform_size * y, platform_size))
    return platforms

def main(screen):
    pygame.init()
    clock = pygame.time.Clock()
    random.seed()

    current_level = 0
    platforms = build_level(current_level, PLATFORM_SIZE)

    background, bg_image = get_background("backgroundBricks.png")
    player = Player(PLATFORM_SIZE*1,WINDOW_HEIGHT - PLATFORM_SIZE,32,64)

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
                    newPlatform = create_platform(player, HEAD_SIZE)
                    if not is_overlapping(platforms, newPlatform) and player.skull_count > 0:
                        platforms.append(newPlatform)
                        player.skull_count -= 1
                    elif player.skull_count <= 0:
                        print(player.level)
                # reset the world
                if event.key == pygame.K_r:
                    platforms = build_level(current_level, PLATFORM_SIZE)
                    player.skull_count = 100
                    player.level = 0
                    respawn(player)

                #when exit window height, next level
                if (WINDOW_HEIGHT - player.rect.y) > 1000:
                    platforms = build_level(current_level, PLATFORM_SIZE)
                    player.level += 1
                    respawn(player)

        player.loop(FPS)
        move(player, platforms)
        draw(screen, background , bg_image, player, platforms)


if __name__ == "__main__":
    main(screen)
