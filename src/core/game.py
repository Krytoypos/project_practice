import pygame

from settings import (
    BLACK,
    WHITE,
    WIDTH,
    HEIGHT
)

from core.level import Level
from core.sound_manager import SoundManager


class Game:

    def __init__(self, screen):

        self.screen = screen
        self.running = True

        self.sound_manager = SoundManager()
        self.sound_manager.play_music()

        self.level_paths = [
            "../levels/level_01.txt",
            "../levels/level_02.txt",
            "../levels/level_03.txt"
        ]

        self.level = Level(
            self.level_paths,
            self.sound_manager
        )

        self.is_loading = False
        self.loading_timer = 0
        self.loading_duration = 1.8

        self.font = pygame.font.Font(
            None,
            72
        )

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def start_loading(self):

        self.is_loading = True
        self.loading_timer = 0

    def update_loading(self, dt):

        self.loading_timer += dt

        if self.loading_timer >= self.loading_duration:

            self.is_loading = False

            success = self.level.load_next_level()

            if not success:
                self.running = False

    def draw_loading(self):

        self.screen.fill(BLACK)

        alpha = abs(
            int(
                255 * (
                    pygame.time.get_ticks() % 1000
                ) / 1000 - 128
            )
        ) * 2

        text = f"КОМНАТА {self.level.current_level_index + 1}"

        text_surface = self.font.render(
            text,
            True,
            WHITE
        )

        text_surface.set_alpha(alpha)

        rect = text_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        self.screen.blit(text_surface, rect)

    def update(self, dt):

        if self.is_loading:

            self.update_loading(dt)
            return

        self.level.update(dt)

        if self.level.level_completed:
            self.start_loading()

    def draw(self):

        if self.is_loading:
            self.draw_loading()
        else:
            self.level.draw(self.screen)