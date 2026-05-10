import pygame

from src.settings import BLACK


class Level:

    def __init__(self, level_path):

        self.level_path = level_path

    def update(self, dt):

        pass

    def draw(self, screen):

        screen.fill(BLACK)