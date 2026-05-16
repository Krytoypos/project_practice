import pygame

import settings
from settings import (
    PLAYER_SPEED,
    GRAVITY,
    JUMP_POWER
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, sound_manager):
        super().__init__()

        self.animations = {
            "idle": [],
            "run": [],
            "jump": []
        }

        self.sound_manager = sound_manager

        self.load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 6
        self.facing_right = True

        # Текущий спрайт
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + 4,
            settings.PLAYER_WIDTH,
            settings.PLAYER_HEIGHT
        )

        # позиция
        self.pos = pygame.Vector2(self.hitbox.topleft)

        # ФИЗИКА
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

        self.step_timer = 0

    def load_animations(self):
        idle_1 = pygame.image.load(
            "../assets/sprites/player/idle1.png"
        ).convert_alpha()

        idle_2 = pygame.image.load(
            "../assets/sprites/player/idle2.png"
        ).convert_alpha()
        self.animations["idle"] = [
            idle_1,
            idle_2
        ]

        run_1 = pygame.image.load(
            "../assets/sprites/player/run1.png"
        ).convert_alpha()

        run_2 = pygame.image.load(
            "../assets/sprites/player/run2.png"
        ).convert_alpha()

        run_3 = pygame.image.load(
            "../assets/sprites/player/run3.png"
        ).convert_alpha()
        self.animations["run"] = [
            run_2,
            run_1,
            run_2,
            run_3
        ]

        jump_1 = pygame.image.load(
            "../assets/sprites/player/jump1.png"
        ).convert_alpha()

        jump_2 = pygame.image.load(
            "../assets/sprites/player/jump2.png"
        ).convert_alpha()
        self.animations["jump"] = [
            jump_1,
            jump_2
        ]

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        ) and self.on_ground:
            self.jump()

    def jump(self):
        self.sound_manager.play("jump")
        self.velocity.y = JUMP_POWER
        self.on_ground = False

    def apply_gravity(self, dt):

        self.velocity.y += GRAVITY * dt

        if self.velocity.y > 1200:
            self.velocity.y = 1200

    def animate(self, dt):
        if self.velocity.y < -50:
            self.state = "jump"
        elif self.velocity.x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        self.frame_index += self.animation_speed * dt
        animation = self.animations[self.state]

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

        # ОТРАЖЕНИЕ
        if not self.facing_right:
            self.image = pygame.transform.flip(
                self.image,
                True,
                False
            )

    def horizontal_movement_collision(self, platforms, dt):
        self.pos.x += self.velocity.x * dt
        self.hitbox.x = round(self.pos.x)
        for sprite in platforms:
            if sprite.rect.colliderect(self.hitbox):
                if self.velocity.x > 0:
                    self.hitbox.right = sprite.rect.left
                elif self.velocity.x < 0:
                    self.hitbox.left = sprite.rect.right
                self.pos.x = self.hitbox.x
                self.velocity.x = 0

    def vertical_movement_collision(self, platforms, dt):

        self.apply_gravity(dt)
        self.on_ground = False
        self.pos.y += self.velocity.y * dt
        self.hitbox.y = round(self.pos.y)

        for sprite in platforms:
            if sprite.rect.colliderect(self.hitbox):
                if self.velocity.y > 0:
                    self.hitbox.bottom = sprite.rect.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.hitbox.top = sprite.rect.bottom
                self.pos.y = self.hitbox.y
                self.velocity.y = 0

    def update(self, dt, platforms=None):

        self.get_input()

        if platforms:
            self.horizontal_movement_collision(
                platforms,
                dt
            )

            self.vertical_movement_collision(
                platforms,
                dt
            )

        if abs(self.velocity.x) > 20 and self.on_ground:

            self.step_timer += dt

            if self.step_timer >= 0.12:
                self.step_timer = 0

                self.sound_manager.play_footstep()

        else:

            self.step_timer = 0

        self.animate(dt)

        self.rect.center = self.hitbox.center