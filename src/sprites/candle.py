import pygame


class Candle(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "../assets/sprites/light1.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (32, 64)
        )

        self.rect = self.image.get_rect(
            topleft=pos
        )

        self.hitbox = self.rect.copy()