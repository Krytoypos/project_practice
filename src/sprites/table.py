import pygame

from settings import TILE_SIZE


class Table(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE))
        self.image.fill((120, 80, 80))

        self.rect = self.image.get_rect(topleft=pos)