import pygame

from src.settings import BLACK
from src.core.level import Level
from core.sound_manager import SoundManager

class Game:
    def __init__(self, screen):
        self.sound_manager = SoundManager()

        self.sound_manager.play_music()

        self.screen = screen

        self.running = True

        self.level = Level(
            "src/levels/room_01.json",
            self.sound_manager
        )

    def handle_events(self):

        for event in pygame.event.get():

            # Закрытие окна
            if event.type == pygame.QUIT:
                self.running = False

        return self.running

    def update(self, dt):

        self.level.update(dt)

    def draw(self):

        self.level.draw(self.screen)