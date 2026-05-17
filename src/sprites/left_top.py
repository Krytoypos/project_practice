import pygame


class Left_Top(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "../assets/sprites/floor11.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(
            topleft=pos
        )

        self.hitbox = self.rect.copy()