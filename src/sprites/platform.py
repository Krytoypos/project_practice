import pygame

from settings import TILE_SIZE


class Platform(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        # Временный спрайт платформы
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((70, 70, 70))

        # Позиция
        self.rect = self.image.get_rect(topleft=pos)