from os.path import join, isfile
from os import listdir

import pygame


"""Flips the sprites on x axis"""
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

"""Loads the sprite sheets into separate sprites for animation"""
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)

            sprites.append(pygame.transform.scale_by(surface,4))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites


"""Constructor for the player character"""
class Player(pygame.sprite.Sprite):
    GRAVITY = 4
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__()
        self.SPRITES = load_sprite_sheets("characters","bonehead",16, 16, True)
        self.initial_x = x
        self.initial_y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.fall_count = 0
        self.direction = "left"
        self.animation_count = 0
        self.jump_count = 0
        self.skull_count = 100


    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))

    def jump(self):
         if self.fall_count <= 10:
             self.y_vel = -self.GRAVITY * 2.1
             self.animation_count = 0
             self.jump_count += 1
             if self.jump_count == 1:
                 self.fall_count = 0

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def move_left(self, velocity):
        self.x_vel = -velocity
        # for animation
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, velocity):
        self.x_vel = velocity
        # for animation
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
        # gravity
        self.y_vel += min(3, (self.fall_count / fps) * self.GRAVITY)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -0.9

    """Animates sprite"""
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

