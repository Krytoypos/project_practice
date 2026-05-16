import pygame


class Bed(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "../assets/sprites/bed.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (96, 64)
        )

        self.rect = self.image.get_rect(
            topleft=pos
        )

        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.bottom - 64,
            96,
            64
        )