import pygame


class BackgroundTile(pygame.sprite.Sprite):

    def __init__(self, pos, image_path):
        super().__init__()

        self.image = pygame.image.load(
            image_path
        ).convert()

        self.image = pygame.transform.scale(
            self.image,
            (32, 32)
        )

        self.rect = self.image.get_rect(
            topleft=pos
        )