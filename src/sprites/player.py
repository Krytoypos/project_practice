import pygame

from settings import (
    PLAYER_SPEED,
    GRAVITY,
    JUMP_POWER
)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        # Временный спрайт
        self.image = pygame.Surface((32, 64))
        self.image.fill((200, 200, 220))

        self.rect = self.image.get_rect(topleft=pos)

        # Хитбокс
        self.hitbox = pygame.Rect(
            self.rect.x + 4,
            self.rect.y + 2,
            24,
            60
        )

        # Float-позиция
        self.pos = pygame.Vector2(self.hitbox.topleft)

        # Скорость
        self.velocity = pygame.Vector2(0, 0)

        # На земле?
        self.on_ground = False

    def get_input(self):

        keys = pygame.key.get_pressed()

        # Движение по X
        self.velocity.x = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED

        # Прыжок
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        ) and self.on_ground:

            self.jump()

    def jump(self):

        self.velocity.y = JUMP_POWER
        self.on_ground = False

    def apply_gravity(self, dt):

        self.velocity.y += GRAVITY * dt

        # Ограничение скорости падения
        if self.velocity.y > 1200:
            self.velocity.y = 1200

    def horizontal_movement_collision(self, platforms, dt):

        # Движение по X
        self.pos.x += self.velocity.x * dt
        self.hitbox.x = round(self.pos.x)

        # Коллизии
        for sprite in platforms:

            if sprite.rect.colliderect(self.hitbox):

                # Движение вправо
                if self.velocity.x > 0:
                    self.hitbox.right = sprite.rect.left

                # Движение влево
                elif self.velocity.x < 0:
                    self.hitbox.left = sprite.rect.right

                # Синхронизация позиции
                self.pos.x = self.hitbox.x

                # Остановка
                self.velocity.x = 0

    def vertical_movement_collision(self, platforms, dt):

        # Гравитация
        self.apply_gravity(dt)

        # Сбрасываем состояние пола
        self.on_ground = False

        # Движение по Y
        self.pos.y += self.velocity.y * dt
        self.hitbox.y = round(self.pos.y)

        # Коллизии
        for sprite in platforms:

            if sprite.rect.colliderect(self.hitbox):

                # Падение вниз
                if self.velocity.y > 0:

                    self.hitbox.bottom = sprite.rect.top
                    self.on_ground = True

                # Удар головой
                elif self.velocity.y < 0:

                    self.hitbox.top = sprite.rect.bottom

                # Синхронизация позиции
                self.pos.y = self.hitbox.y

                # Остановка
                self.velocity.y = 0

    def update(self, dt, platforms):

        # Ввод
        self.get_input()

        # Коллизии по X
        self.horizontal_movement_collision(platforms, dt)

        # Коллизии по Y
        self.vertical_movement_collision(platforms, dt)

        # Синхронизация визуального rect
        self.rect.center = self.hitbox.center