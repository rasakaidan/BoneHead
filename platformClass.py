from os.path import join, isfile
from os import listdir

import pygame

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


"""Constructor for the default platform"""
def get_platform(size, image):
    path = join("assets", "world", image)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0,0,size,size)
    surface.blit(image,(0,0), rect)
    return pygame.transform.scale_by(surface,5)