import pygame


class Platform(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "../assets/sprites/floor1.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)