import pygame
from settings import (
    BLACK,
    WHITE,
    WIDTH,
    HEIGHT
)
from core.level import Level
from core.sound_manager import SoundManager
from core.menu import Menu


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # --- звук ---
        self.sound_manager = SoundManager()
        self.sound_manager.play_music()

        # --- пути к уровням ---
        self.level_paths = [
            "../levels/level_01.txt",
            "../levels/level_01.txt",
            "../levels/level_02.txt",
            "../levels/level_03.txt"
        ]

        # --- машина состояний ---
        self.state = "menu"        # menu | playing
        self.menu = Menu(screen, self.sound_manager)
        self.level = None

        # --- загрузка уровня ---
        self.is_loading = False
        self.loading_timer = 0
        self.loading_duration = 1.8
        self.font = pygame.font.Font(None, 72)

        # --- флаг: все уровни пройдены ---
        self.all_levels_done = False

    # =================================================================
    #  События
    # =================================================================
    def handle_events(self):
        if self.state == "menu":
            self.menu.handle_events()
            if not self.menu.running:
                self.running = False
            elif self.menu.start_game:
                self.menu.start_game = False
                self._start_game(self.menu.selected_level)

        elif self.state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._return_to_menu()

    # =================================================================
    #  Управление состояниями
    # =================================================================
    def _start_game(self, level_index):
        """Запуск игры с указанного уровня (-1 = с начала)."""
        if level_index >= 0 and level_index < len(self.level_paths):
            # Начинаем с конкретного уровня: загружаем только его и последующие
            paths = self.level_paths[level_index:]
            self.level = Level(paths, self.sound_manager)
        else:
            # Начинаем с первого уровня
            self.level = Level(self.level_paths, self.sound_manager)

        self.state = "playing"
        self.is_loading = True
        self.loading_timer = 0
        self.all_levels_done = False

    def _return_to_menu(self):
        """Возврат в главное меню."""
        self.level = None
        self.state = "menu"
        self.menu.start_game = False
        self.is_loading = False
        self.all_levels_done = False

    # =================================================================
    #  Загрузочный экран
    # =================================================================
    def start_loading(self):
        self.is_loading = True
        self.loading_timer = 0

    def update_loading(self, dt):
        self.loading_timer += dt
        if self.loading_timer >= self.loading_duration:
            self.is_loading = False
            success = self.level.load_next_level()
            if not success:
                # Все уровни пройдены — возвращаемся в меню
                self.all_levels_done = True
                self._return_to_menu()

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

    # =================================================================
    #  Главный цикл
    # =================================================================
    def update(self, dt):
        if self.state == "menu":
            self.menu.update(dt)

        elif self.state == "playing":
            if self.is_loading:
                self.update_loading(dt)
                return
            if self.level is None:
                return
            self.level.update(dt)
            if self.level.level_completed:
                self.start_loading()

    def draw(self):
        if self.state == "menu":
            self.menu.draw()

        elif self.state == "playing":
            if self.is_loading:
                self.draw_loading()
            elif self.level is not None:
                self.level.draw(self.screen)
