import pygame

from settings import (
    BLACK,
    TILE_SIZE,
    WIDTH,
    HEIGHT
)

from sprites.player import Player
from sprites.platform import Platform
from sprites.button import Button
from sprites.nightstand import Nightstand
from sprites.lego import Lego
from sprites.glass import Glass
from sprites.slope_left import SlopeLeft
from sprites.slope_right import SlopeRight
from sprites.door import Door
from sprites.bed import Bed
from sprites.sofa import Sofa
from sprites.table import Table
from sprites.fridge import Fridge

class Level:

    def __init__(self, level_path):

        self.level_path = level_path

        # Группы спрайтов
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # =========================
        # ОСВЕЩЕНИЕ
        # =========================

        # Поверхность темноты
        self.fog = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        # Маска света
        self.light_mask = pygame.image.load("../assets/sprites/light_mask.jpg").convert_alpha()

        # =========================
        # КАРТА УРОВНЯ
        # =========================

        self.level_map = [
            "########################################",
            "#...................#..................#",
            "#..............K....D................E.#",
            "#...................D..................#",
            "#.....\#################################",
            "#HH....#################################",
            "#......#################################",
            "#....HH#################################",
            "#......................#################",
            "#HH....................#################",
            "#......................\################",
            "#################......................#",
            "#################......................#",
            "#################VVV...................#",
            "#################VVV...................#",
            "###################################\...#",
            "##############################/........#",
            "##########################/............#",
            "#.................................../###",
            "#.BBB...............................####",
            "#.BBB.P.............................####",
            "########################################",
            "######################################"
        ]

        self.hazard_sprites = pygame.sprite.Group()
        # Создание карты
        self.create_map()

    def create_map(self):

        for row_index, row in enumerate(self.level_map):

            for col_index, cell in enumerate(row):

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                # =====================================
                # ИГРОК
                # =====================================

                if cell == "P":

                    self.player = Player((x, y))

                    self.visible_sprites.add(self.player)

                # =====================================
                # ПЛАТФОРМЫ
                # =====================================

                elif cell == "#":

                    platform = Platform((x, y))

                    self.visible_sprites.add(platform)
                    self.obstacle_sprites.add(platform)

                # =====================================
                # СКВОЗНАЯ ПОЛКА
                # =====================================

                elif cell == "H":

                    shelf = Platform((x, y))

                    # Сквозная платформа
                    shelf.is_passable = True

                    self.visible_sprites.add(shelf)
                    self.obstacle_sprites.add(shelf)

                # =====================================
                # КНОПКА
                # =====================================

                elif cell == "K":

                    button = Button((x, y))

                    self.visible_sprites.add(button)

                # =====================================
                # ТУМБОЧКА
                # =====================================

                elif cell == "N":

                    nightstand = Nightstand((x, y))

                    self.visible_sprites.add(nightstand)
                    self.obstacle_sprites.add(nightstand)

                # =====================================
                # LEGO (ОПАСНОСТЬ)
                # =====================================

                elif cell == "L":

                    lego = Lego((x, y))

                    self.visible_sprites.add(lego)
                    self.hazard_sprites.add(lego)

                # =====================================
                # СТЕКЛО (ОПАСНОСТЬ)
                # =====================================

                elif cell == "S":

                    glass = Glass((x, y))

                    self.visible_sprites.add(glass)
                    self.hazard_sprites.add(glass)

                # =====================================
                # НАКЛОН ВЛЕВО
                # =====================================

                elif cell == "/":

                    slope_left = SlopeLeft((x, y))

                    self.visible_sprites.add(slope_left)
                    self.obstacle_sprites.add(slope_left)

                # =====================================
                # НАКЛОН ВПРАВО
                # =====================================

                elif cell == "\\":

                    slope_right = SlopeRight((x, y))

                    self.visible_sprites.add(slope_right)
                    self.obstacle_sprites.add(slope_right)

                # =====================================
                # ДВЕРЬ (1x2)
                # =====================================

                elif cell == "D":

                    door = Door((x, y - TILE_SIZE))

                    self.visible_sprites.add(door)

                # =====================================
                # КРОВАТЬ (3x2)
                # =====================================

                elif cell == "B":

                    bed = Bed((x, y - TILE_SIZE))

                    self.visible_sprites.add(bed)
                    self.obstacle_sprites.add(bed)

                # =====================================
                # ДИВАН (3x2)
                # =====================================

                elif cell == "V":

                    sofa = Sofa((x, y - TILE_SIZE))

                    self.visible_sprites.add(sofa)
                    self.obstacle_sprites.add(sofa)

                # =====================================
                # СТОЛ (2x1)
                # =====================================

                elif cell == "T":

                    table = Table((x, y))

                    self.visible_sprites.add(table)
                    self.obstacle_sprites.add(table)

                # =====================================
                # ХОЛОДИЛЬНИК (1x2)
                # =====================================

                elif cell == "R":

                    fridge = Fridge((x, y - TILE_SIZE))

                    self.visible_sprites.add(fridge)
                    self.obstacle_sprites.add(fridge)

    def update(self, dt):

        # Обновление всех спрайтов
        self.visible_sprites.update(
            dt,
            self.obstacle_sprites
        )

    def draw(self, screen):

        # =========================
        # ФОН
        # =========================

        screen.fill(BLACK)

        # =========================
        # СПРАЙТЫ
        # =========================

        self.visible_sprites.draw(screen)

        # =========================
        # ОСВЕЩЕНИЕ
        # =========================

        # Полная темнота
        self.fog.fill((0, 0, 0, 235))

        # Позиция света
        light_x = (
            self.player.rect.centerx
            - self.light_mask.get_width() // 2
        )

        light_y = (
            self.player.rect.centery
            - self.light_mask.get_height() // 2
        )

        # Вырезаем свет
        self.fog.blit(
            self.light_mask,
            (light_x, light_y),
            special_flags=pygame.BLEND_RGBA_SUB
        )

        # Накладываем темноту
        screen.blit(self.fog, (0, 0))