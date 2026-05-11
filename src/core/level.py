import pygame

from settings import BLACK, TILE_SIZE
from sprites.player import Player
from sprites.platform import Platform


class Level:
    def __init__(self, level_path):

        self.level_path = level_path

        # Группы спрайтов
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Временная карта уровня
        self.level_map = [
            "########################################",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#......................................#",
            "#...................###................#",
            "#......................................#",
            "#..........###.........................#",
            "#......................................#",
            "#......................................#",
            "#.....P................................#",
            "########################################"
        ]

        # Создание объектов уровня
        self.create_map()

    def create_map(self):

        for row_index, row in enumerate(self.level_map):

            for col_index, cell in enumerate(row):

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                # Платформа
                if cell == "#":

                    platform = Platform((x, y))

                    # Добавляем:
                    # - в отрисовку
                    # - в коллизии
                    self.visible_sprites.add(platform)
                    self.obstacle_sprites.add(platform)

                # Игрок
                elif cell == "P":

                    self.player = Player((x, y))

                    # Игрок только в видимые
                    self.visible_sprites.add(self.player)

    def update(self, dt):

        # Обновляем все спрайты
        # Передаем платформы для коллизий
        self.visible_sprites.update(dt, self.obstacle_sprites)

    def draw(self, screen):

        # Фон
        screen.fill(BLACK)

        # Отрисовка всех объектов
        self.visible_sprites.draw(screen)