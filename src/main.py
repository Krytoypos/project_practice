import pygame

from src.settings import WIDTH, HEIGHT, FPS, TITLE
from src.core.game import Game


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    game = Game(screen)

    while game.running:

        dt = clock.tick(FPS) / 1000

        game.handle_events()

        game.update(dt)

        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()