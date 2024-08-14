import pygame

# resolution
WIDTH = 1920
HEIGHT = 1040
# rgb of background
BACKGROUND = (1, 1, 6)


# sprite renderer
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# player builder
class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("assets/characters/bonehead.png", startx, starty)

        # player movement speed
        self.speed = 4.5

    def move(self, x, y):
        self.rect.move_ip([x, y])

    def update(self):
        # basic controls
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.move(-self.speed, 0)
        elif key[pygame.K_d]:
            self.move(self.speed, 0)


# platform builder
class Platform(Sprite):
    def __init__(self, startx, starty):
        super().__init__("assets/world/block.png", startx, starty)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # where player spawns
    player = Player(100, 528)
    platforms = pygame.sprite.Group()

    # weird platform placing loop from tutorial
    for platform in range(0, 1280, 248):
        platforms.add(Platform(platform, 656))

    while True:
        pygame.event.pump()
        player.update()

        screen.fill(BACKGROUND)
        player.draw(screen)
        platforms.draw(screen)
        pygame.display.flip()

        # 60fps gamespeed
        clock.tick(60)


# idk, runs it
if __name__ == "__main__":
    main()
