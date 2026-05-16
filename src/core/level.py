import pygame

from settings import (
    BLACK,
    TILE_SIZE,
    WIDTH,
    HEIGHT
)

from sprites.player import Player
from sprites.platform_1 import Platform_1
from sprites.platform_2 import Platform_2
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
from sprites.floor import Floor_1
from sprites.candle import Candle


class Level:

    def __init__(self, levels_list, sound_manager):

        self.sound_manager = sound_manager

        self.levels_list = levels_list
        self.current_level_index = 0

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.light_sprites = pygame.sprite.Group()
        self.hazard_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()

        self.level_completed = False

        self.fog = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        self.light_mask = pygame.image.load(
            "../assets/sprites/light_mask.png"
        ).convert_alpha()

        self.candle_light_mask = pygame.transform.scale(
            self.light_mask,
            (140, 140)
        )

        self.player_light_mask = pygame.transform.scale(
            self.light_mask,
            (200, 200)
        )

        level_width = 40 * TILE_SIZE
        level_height = 23 * TILE_SIZE

        self.background = pygame.image.load(
            "../assets/sprites/background.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (level_width, level_height)
        )

        self.load_level_data(
            self.levels_list[self.current_level_index]
        )

    def clear_level(self):

        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.light_sprites.empty()
        self.hazard_sprites.empty()
        self.door_sprites.empty()

    def load_level_data(self, filepath):

        self.clear_level()

        self.level_completed = False

        self.level_map = []

        with open(filepath, "r", encoding="utf-8") as file:

            for line in file:
                self.level_map.append(
                    line.strip("\r\n")
                )

        self.create_map()

    def load_next_level(self):

        self.current_level_index += 1

        if self.current_level_index >= len(self.levels_list):
            return False

        self.load_level_data(
            self.levels_list[self.current_level_index]
        )

        return True

    def create_map(self):

        for row_index, row in enumerate(self.level_map):

            for col_index, cell in enumerate(row):

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == "P":

                    self.player = Player(
                        (x, y),
                        self.sound_manager
                    )

                    self.visible_sprites.add(
                        self.player
                    )

                elif cell == "C":

                    candle = Candle((x, y - 32))

                    self.visible_sprites.add(candle)
                    self.light_sprites.add(candle)

                elif cell == "#":

                    platform = Floor_1((x, y))

                    self.visible_sprites.add(platform)
                    self.obstacle_sprites.add(platform)

                elif cell == "H":

                    shelf = Platform_1((x, y))

                    shelf.is_passable = True

                    self.visible_sprites.add(shelf)
                    self.obstacle_sprites.add(shelf)

                elif cell == "h":

                    shelf = Platform_2((x, y))

                    shelf.is_passable = True

                    self.visible_sprites.add(shelf)
                    self.obstacle_sprites.add(shelf)

                elif cell == "K":

                    button = Button((x, y))

                    self.visible_sprites.add(button)

                elif cell == "N":

                    nightstand = Nightstand((x, y))

                    self.visible_sprites.add(nightstand)
                    self.obstacle_sprites.add(nightstand)

                elif cell == "L":

                    lego = Lego((x, y))

                    self.visible_sprites.add(lego)
                    self.hazard_sprites.add(lego)

                elif cell == "S":

                    glass = Glass((x, y))

                    self.visible_sprites.add(glass)
                    self.hazard_sprites.add(glass)

                elif cell == "/":

                    slope_left = SlopeLeft((x, y))

                    self.visible_sprites.add(slope_left)
                    self.obstacle_sprites.add(slope_left)

                elif cell == "\\":

                    slope_right = SlopeRight((x, y))

                    self.visible_sprites.add(slope_right)
                    self.obstacle_sprites.add(slope_right)

                elif cell == "D":

                    door = Door((x, y - TILE_SIZE))

                    self.visible_sprites.add(door)
                    self.door_sprites.add(door)

                elif cell == "B":

                    bed = Bed((x, y - TILE_SIZE))

                    self.visible_sprites.add(bed)
                    self.obstacle_sprites.add(bed)

                elif cell == "V":

                    sofa = Sofa((x, y - TILE_SIZE))

                    self.visible_sprites.add(sofa)
                    self.obstacle_sprites.add(sofa)

                elif cell == "T":

                    table = Table((x, y))

                    self.visible_sprites.add(table)
                    self.obstacle_sprites.add(table)

                elif cell == "R":

                    fridge = Fridge((x, y - TILE_SIZE))

                    self.visible_sprites.add(fridge)
                    self.obstacle_sprites.add(fridge)

    def check_level_complete(self):

        for door in self.door_sprites:

            if self.player.hitbox.colliderect(door.rect):

                self.sound_manager.play("door")

                self.level_completed = True

                return

    def update(self, dt):

        for sprite in self.visible_sprites:

            if sprite == self.player:
                sprite.update(
                    dt,
                    self.obstacle_sprites
                )

            else:
                sprite.update()

        self.check_level_complete()

    def draw(self, screen):

        screen.fill(BLACK)

        screen.blit(self.background, (0, 0))

        self.visible_sprites.draw(screen)

        self.fog.fill((0, 0, 0, 255))

        for candle in self.light_sprites:

            light_x = (
                candle.rect.centerx
                - self.candle_light_mask.get_width() // 2
            )

            light_y = (
                candle.rect.centery
                - self.candle_light_mask.get_height() // 2
            )

            self.fog.blit(
                self.candle_light_mask,
                (light_x, light_y),
                special_flags=pygame.BLEND_RGBA_SUB
            )

        light_x = (
            self.player.rect.centerx
            - self.player_light_mask.get_width() // 2
        )

        light_y = (
            self.player.rect.centery
            - self.player_light_mask.get_height() // 2
        )

        self.fog.blit(
            self.player_light_mask,
            (light_x, light_y),
            special_flags=pygame.BLEND_RGBA_SUB
        )

        screen.blit(self.fog, (0, 0))