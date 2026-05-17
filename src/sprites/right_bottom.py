import pygame

from settings import TILE_SIZE


class Right_Bottom(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        self.image = pygame.image.load(
            "../assets/sprites/block6.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()