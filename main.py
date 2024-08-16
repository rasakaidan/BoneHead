from os.path import join, isfile
from os import listdir

import pygame
from pygame.examples.moveit import WIDTH

WINDOW_WIDTH, WINDOW_HEIGHT = 1792, 896
FPS = 60
PLAYER_SPEED = 8

pygame.display.set_caption("Bonehead")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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

            sprites.append(pygame.transform.scale_by(surface,5))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

"""Constructor for the default platform"""
def get_platform(size, image):
    path = join("assets", "world", image)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0,0,size,size)
    surface.blit(image,(0,0), rect)
    return pygame.transform.scale_by(surface,6)

"""Constructor for the player character"""
class Player(pygame.sprite.Sprite):
    GRAVITY = 3
    SPRITES = load_sprite_sheets("characters","bonehead",16, 16, True)
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.fall_count = 0
        self.direction = "left"
        self.animation_count = 0
        self.jump_count = 0


    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))

    def jump(self):
        self.y_vel = -self.GRAVITY * 7
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

        self.fall_count += 3
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1.8

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


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# platformBricks.png is 16x16 but scaled by get_platform (6), 96x96
class Platform(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        platform = get_platform(size, "platformBricks.png")
        self.image.blit(platform, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

# platformBonehead.png is 8x8 but scaled by get_platform (6), 48x48
class PlayerPlatform(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        platform = get_platform(size, "platformBonehead.png")
        self.image.blit(platform, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


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
    collide_left = collide(player, objects, -PLAYER_SPEED * 2)
    collide_right = collide(player, objects, PLAYER_SPEED * 2)

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



def build_level1(platforms, platform_size):
    platforms.clear()
    for i in range(-WIDTH // platform_size, WIDTH * 3 // platform_size):
        platforms.append(Platform(i * platform_size, WINDOW_HEIGHT - platform_size, platform_size))

    platforms.append(Platform(platform_size * 2, platform_size * 6, platform_size))
    platforms.append(Platform(platform_size * 5, platform_size * 4, platform_size))
    platforms.append(Platform(platform_size * 7, platform_size * 4, platform_size))

    return

def main(screen):
    pygame.init()
    clock = pygame.time.Clock()

    platform_size = 96
    platforms = []
    build_level1(platforms, platform_size)

    background, bg_image = get_background("backgroundBricks.png")
    # player spawn location
    player = Player(100,750,40,80)


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
                    newPlatform = create_platform(player, platform_size)
                    if not is_overlapping(platforms, newPlatform):
                        platforms.append(newPlatform)

                # reset the world
                if event.key == pygame.K_r:
                    build_level1(platforms, platform_size)

        player.loop(FPS)
        move(player, platforms)
        draw(screen, background , bg_image, player, platforms)


if __name__ == "__main__":
    main(screen)
