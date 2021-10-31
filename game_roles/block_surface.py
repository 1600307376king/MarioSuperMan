import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, init_x, init_y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y


class BlockSurface(pygame.sprite.Sprite):
    def __init__(self, color, width, height, init_x, init_y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
