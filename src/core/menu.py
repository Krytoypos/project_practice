"""
Nycto — Главное меню
Пиксельный 2D-стиль, атмосферная тьма со светом, туман и частицы пыли.
Экраны: главное меню, выбор уровня, настройки, титры.
"""

import pygame
import math
import random

# ---------- совместимый импорт настроек ----------
try:
    from src.settings import WIDTH, HEIGHT, BLACK, WHITE
except ImportError:
    from settings import WIDTH, HEIGHT, BLACK, WHITE

# ---------- константы меню ----------
MENU_MUSIC_VOL_DEFAULT = 0.20
MENU_SFX_VOL_DEFAULT = 0.60
PIXEL_SCALE = 2          # множитель масштабирования для пиксельного эффекта
PARTICLE_COUNT = 60       # количество пылинок


# ===================================================================
#  Частицы пыли — парят в темноте, создаёт атмосферу
# ===================================================================
class DustParticle:
    __slots__ = ("x", "y", "size", "alpha_base", "vx", "vy", "life", "max_life")

    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.8, 2.5)
        self.alpha_base = random.randint(25, 70)
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-18, -4)
        self.max_life = random.uniform(3, 7)
        self.life = self.max_life

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life <= 0:
            self.respawn()
            return True
        return False

    def draw(self, surface):
        ratio = max(0.0, self.life / self.max_life)
        alpha = int(self.alpha_base * ratio)
        if alpha < 2:
            return
        r = max(1, int(self.size))
        d = r * 2 + 2
        tmp = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (255, 240, 190, alpha), (r + 1, r + 1), r)
        surface.blit(tmp, (int(self.x) - r - 1, int(self.y) - r - 1))


# ===================================================================
#  Класс меню
# ===================================================================
class Menu:
    """Полноэкранное пиксельное меню игры Nycto."""

    # ----- палитра (тёплые тона свечи на фоне тьмы) -----
    C_BG          = (8, 6, 4)
    C_TITLE       = (255, 220, 140)
    C_SUBTITLE    = (160, 135, 95)
    C_ITEM_SEL    = (255, 235, 180)
    C_ITEM_DIM    = (90, 80, 65)
    C_ARROW       = (255, 200, 100)
    C_GLOW        = (255, 200, 100)
    C_BAR_BG      = (35, 30, 25)
    C_BAR_FILL    = (220, 175, 80)
    C_BAR_FILL_A  = (255, 210, 110)
    C_BAR_BORDER  = (100, 85, 60)
    C_CREDIT_NAME = (255, 220, 150)
    C_CREDIT_ROLE = (200, 170, 115)
    C_CREDIT_LIST = (140, 120, 90)
    C_HINT        = (80, 70, 55)

    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager

        # --- состояние ---
        self.state = "main"           # main | level_select | settings | credits
        self.running = True
        self.start_game = False
        self.selected_level = -1      # -1 = с начала

        # главное меню
        self.main_items = ["ИГРАТЬ", "ВЫБОР УРОВНЯ", "НАСТРОЙКИ", "ТИТРЫ", "ВЫХОД"]
        self.main_sel = 0

        # выбор уровня
        self.level_items = ["КОМНАТА 1", "КОМНАТА 2", "КОМНАТА 3"]
        self.level_sel = 0

        # настройки
        self.music_volume = getattr(sound_manager, "music_volume", MENU_MUSIC_VOL_DEFAULT)
        self.sfx_volume   = getattr(sound_manager, "sfx_volume",   MENU_SFX_VOL_DEFAULT)
        self.settings_sel = 0         # 0=музыка 1=SFX 2=назад
        self.adjusting    = False

        # титры
        self.credits_scroll = 0.0
        self.credits_max_scroll = 0.0   # вычислим позже

        # --- шрифты (маленькие -> масштабируем для пиксельного вида) ---
        self.f_sm  = pygame.font.Font(None, 18)
        self.f_md  = pygame.font.Font(None, 26)
        self.f_lg  = pygame.font.Font(None, 44)
        self.f_xl  = pygame.font.Font(None, 72)

        # --- предрендеринг ---
        self._build_title_surface()
        self._build_glow_cache()
        self._build_credits_data()

        # --- частицы ---
        self.particles = [DustParticle() for _ in range(PARTICLE_COUNT)]

        # --- время для анимации ---
        self.time = 0.0

        # --- туман ---
        self.fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # --- попытка загрузить световую маску из игры ---
        self.light_mask = None
        try:
            self.light_mask = pygame.image.load(
                "../assets/sprites/light_mask.png"
            ).convert_alpha()
        except Exception:
            pass

    # =================================================================
    #  Предрендеринг
    # =================================================================
    def _px(self, surf, scale=PIXEL_SCALE):
        """Масштабирование без сглаживания для пиксельного стиля."""
        w, h = surf.get_size()
        return pygame.transform.scale(surf, (w * scale, h * scale))

    def _build_title_surface(self):
        """Предрендер заголовка 'NYCTO'."""
        base = self.f_xl.render("NYCTO", True, self.C_TITLE)
        self.title_surf = self._px(base, 3)
        self.title_rect = self.title_surf.get_rect(
            center=(WIDTH // 2, 120)
        )

        sub = self.f_md.render("Найди свет во тьме", True, self.C_SUBTITLE)
        self.subtitle_surf = self._px(sub, 2)
        self.subtitle_rect = self.subtitle_surf.get_rect(
            center=(WIDTH // 2, 190)
        )

    def _build_glow_cache(self):
        """Кэш свечения разного размера."""
        self._glow_cache = {}
        for radius in (50, 80, 120, 160, 220):
            s = radius * 2
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            for r in range(radius, 0, -2):
                a = int(35 * (1 - r / radius))
                pygame.draw.circle(surf, (*self.C_GLOW, a), (radius, radius), r)
            self._glow_cache[radius] = surf

    def _get_glow(self, radius):
        r = min(self._glow_cache, key=lambda x: abs(x - radius))
        return self._glow_cache[r]

    def _build_credits_data(self):
        """Подготовка данных титров."""
        self.credits_data = [
            {
                "name": "Ефим «Krytoypos» Мар",
                "role": "Lead Developer / Engine",
                "contribs": [
                    "Архитектура проекта (MVC)",
                    "Кастомный физический движок",
                    "Система коллизий по осям X/Y",
                    "Менеджер уровней и тайловая загрузка",
                ],
            },
            {
                "name": "София «Fiep» Панфилова",
                "role": "Level Design / Sound",
                "contribs": [
                    "Проектирование дизайна всех уровней",
                    "Полное звуковое оформление игры",
                    "Подбор и обработка аудио-ассетов",
                    "Создание и наполнение сайта проекта",
                    "Написание отчётной документации по основному проекту",
                ],
            },
            {
                "name": "Елена «ImLuckyCat» Рахчеева",
                "role": "Graphics / Documents",
                "contribs": [
                    "Отрисовка всех игровых спрайтов",
                    "Анимации персонажа",
                    "Полная игровая графика и арт-дирекшн",
                    "Написание отчётной документации по данному проекту",
                ],
            },
        ]
        # оценка высоты для скролла
        total_h = 0
        for person in self.credits_data:
            total_h += 38 + 28 + len(person["contribs"]) * 24 + 40
        self.credits_max_scroll = max(0, total_h - (HEIGHT - 200))

    # =================================================================
    #  Утилиты рисования
    # =================================================================
    def _draw_text(self, text, font, color, center, scale=PIXEL_SCALE):
        surf = font.render(text, True, color)
        surf = self._px(surf, scale)
        rect = surf.get_rect(center=center)
        self.screen.blit(surf, rect)
        return rect

    def _draw_menu_item(self, text, y, selected, font=None):
        """Отрисовка одного пункта меню со свечением и стрелками."""
        if font is None:
            font = self.f_md
        cx = WIDTH // 2

        if selected:
            # свечение
            g = self._get_glow(80)
            self.screen.blit(
                g,
                (cx - g.get_width() // 2, y - g.get_height() // 2),
            )
            # стрелки
            arrow = self._px(font.render(">", True, self.C_ARROW), PIXEL_SCALE)
            self.screen.blit(arrow, (cx - 200, y - arrow.get_height() // 2))
            self.screen.blit(arrow, (cx + 160, y - arrow.get_height() // 2))
            color = self.C_ITEM_SEL
        else:
            color = self.C_ITEM_DIM

        self._draw_text(text, font, color, (cx, y))

    def _draw_slider(self, label, value, y, active):
        """Отрисовка горизонтального слайдера громкости."""
        cx = WIDTH // 2
        bar_w, bar_h = 260, 12
        bar_x = cx - bar_w // 2

        # метка
        lbl_color = self.C_ITEM_SEL if active else self.C_CREDIT_ROLE
        self._draw_text(label, self.f_md, lbl_color, (cx, y))

        # фон полоски
        bar_y = y + 30
        pygame.draw.rect(self.screen, self.C_BAR_BG, (bar_x, bar_y, bar_w, bar_h))

        # заполнение
        fill_w = max(0, int(bar_w * value))
        fill_col = self.C_BAR_FILL_A if active else self.C_BAR_FILL
        if fill_w > 0:
            pygame.draw.rect(self.screen, fill_col, (bar_x, bar_y, fill_w, bar_h))

        # рамка
        pygame.draw.rect(self.screen, self.C_BAR_BORDER, (bar_x, bar_y, bar_w, bar_h), 2)

        # процент
        self._draw_text(
            f"{int(value * 100)}%",
            self.f_sm,
            self.C_CREDIT_ROLE,
            (cx, bar_y + 28),
        )

    # =================================================================
    #  Туман / свет
    # =================================================================
    def _apply_fog(self, light_center=None):
        """Накладывает туман тьмы с источником света."""
        self.fog.fill((0, 0, 0, 190))
        if light_center is None:
            light_center = (WIDTH // 2, HEIGHT // 2 - 60)

        lx, ly = light_center
        if self.light_mask:
            mask = pygame.transform.scale(self.light_mask, (350, 350))
        else:
            mask = self._get_glow(160)

        self.fog.blit(
            mask,
            (lx - mask.get_width() // 2, ly - mask.get_height() // 2),
            special_flags=pygame.BLEND_RGBA_SUB,
        )
        self.screen.blit(self.fog, (0, 0))

    # =================================================================
    #  Обработка ввода
    # =================================================================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            key = event.key

            # --- главное меню ---
            if self.state == "main":
                if key in (pygame.K_UP, pygame.K_w):
                    self.main_sel = (self.main_sel - 1) % len(self.main_items)
                    self._play_nav()
                elif key in (pygame.K_DOWN, pygame.K_s):
                    self.main_sel = (self.main_sel + 1) % len(self.main_items)
                    self._play_nav()
                elif key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._play_confirm()
                    self._main_action(self.main_sel)

            # --- выбор уровня ---
            elif self.state == "level_select":
                total = len(self.level_items) + 1  # + "Назад"
                if key in (pygame.K_UP, pygame.K_w):
                    self.level_sel = (self.level_sel - 1) % total
                    self._play_nav()
                elif key in (pygame.K_DOWN, pygame.K_s):
                    self.level_sel = (self.level_sel + 1) % total
                    self._play_nav()
                elif key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._play_confirm()
                    if self.level_sel < len(self.level_items):
                        self.start_game = True
                        self.selected_level = self.level_sel
                    else:
                        self.state = "main"
                elif key == pygame.K_ESCAPE:
                    self.state = "main"

            # --- настройки ---
            elif self.state == "settings":
                if not self.adjusting:
                    if key in (pygame.K_UP, pygame.K_w):
                        self.settings_sel = (self.settings_sel - 1) % 3
                        self._play_nav()
                    elif key in (pygame.K_DOWN, pygame.K_s):
                        self.settings_sel = (self.settings_sel + 1) % 3
                        self._play_nav()
                    elif key in (pygame.K_RETURN, pygame.K_SPACE,
                                 pygame.K_LEFT, pygame.K_RIGHT):
                        if self.settings_sel == 2:
                            self._play_confirm()
                            self.state = "main"
                        else:
                            self.adjusting = True
                    elif key == pygame.K_ESCAPE:
                        self.state = "main"
                else:
                    if key == pygame.K_LEFT:
                        self._adjust_vol(self.settings_sel, -0.05)
                    elif key == pygame.K_RIGHT:
                        self._adjust_vol(self.settings_sel, 0.05)
                    elif key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        self.adjusting = False

            # --- титры ---
            elif self.state == "credits":
                if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "main"
                elif key == pygame.K_UP:
                    self.credits_scroll = max(0, self.credits_scroll - 40)
                elif key == pygame.K_DOWN:
                    self.credits_scroll = min(
                        self.credits_max_scroll,
                        self.credits_scroll + 40,
                    )

    def _play_nav(self):
        try:
            self.sound_manager.play("button")
        except Exception:
            pass

    def _play_confirm(self):
        try:
            self.sound_manager.play("lamp_on")
        except Exception:
            pass

    def _main_action(self, idx):
        if idx == 0:          # Играть
            self.start_game = True
            self.selected_level = -1
        elif idx == 1:        # Выбор уровня
            self.state = "level_select"
            self.level_sel = 0
        elif idx == 2:        # Настройки
            self.state = "settings"
            self.settings_sel = 0
            self.adjusting = False
        elif idx == 3:        # Титры
            self.state = "credits"
            self.credits_scroll = 0.0
        elif idx == 4:        # Выход
            self.running = False

    def _adjust_vol(self, setting, delta):
        if setting == 0:
            self.music_volume = max(0.0, min(1.0, self.music_volume + delta))
            pygame.mixer.music.set_volume(self.music_volume)
            self.sound_manager.music_volume = self.music_volume
        elif setting == 1:
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + delta))
            self.sound_manager.sfx_volume = self.sfx_volume
            for snd in self.sound_manager.sounds.values():
                snd.set_volume(self.sfx_volume)
            for snd in self.sound_manager.footsteps:
                snd.set_volume(self.sfx_volume)

    # =================================================================
    #  Обновление
    # =================================================================
    def update(self, dt):
        self.time += dt
        for p in self.particles:
            p.update(dt)

    # =================================================================
    #  Отрисовка экранов
    # =================================================================
    def draw(self):
        self.screen.fill(self.C_BG)

        if self.state == "main":
            self._draw_main()
        elif self.state == "level_select":
            self._draw_level_select()
        elif self.state == "settings":
            self._draw_settings()
        elif self.state == "credits":
            self._draw_credits()

        # частицы поверх всего
        for p in self.particles:
            p.draw(self.screen)

        # туман + свет
        self._apply_fog()

    # ----- Главное меню -----
    def _draw_main(self):
        # свечение за заголовком (мерцание)
        flicker = math.sin(self.time * 2.5) * 0.15 + 0.85
        g = self._get_glow(160)
        g_copy = g.copy()
        g_copy.set_alpha(int(40 * flicker))
        self.screen.blit(g_copy, (WIDTH // 2 - g.get_width() // 2, 60))

        # заголовок (мерцание яркости)
        title_alpha = int(200 + 55 * flicker)
        ts = self.title_surf.copy()
        ts.set_alpha(title_alpha)
        self.screen.blit(ts, self.title_rect)

        # подзаголовок
        self.screen.blit(self.subtitle_surf, self.subtitle_rect)

        # пункты меню
        start_y = 310
        spacing = 58
        for i, item in enumerate(self.main_items):
            y = start_y + i * spacing
            self._draw_menu_item(item, y, i == self.main_sel)

        # подсказка внизу
        self._draw_text(
            "W/S или Стрелки — выбор  |  Enter — подтвердить",
            self.f_sm,
            self.C_HINT,
            (WIDTH // 2, HEIGHT - 30),
        )

    # ----- Выбор уровня -----
    def _draw_level_select(self):
        self._draw_text(
            "ВЫБОР УРОВНЯ",
            self.f_lg,
            self.C_TITLE,
            (WIDTH // 2, 90),
        )

        start_y = 240
        spacing = 72
        all_items = self.level_items + ["НАЗАД"]
        for i, item in enumerate(all_items):
            y = start_y + i * spacing
            self._draw_menu_item(item, y, i == self.level_sel)

        self._draw_text(
            "ESC — назад",
            self.f_sm,
            self.C_HINT,
            (WIDTH // 2, HEIGHT - 30),
        )

    # ----- Настройки -----
    def _draw_settings(self):
        self._draw_text(
            "НАСТРОЙКИ",
            self.f_lg,
            self.C_TITLE,
            (WIDTH // 2, 90),
        )

        # слайдер музыки
        self._draw_slider(
            "Громкость музыки",
            self.music_volume,
            250,
            self.settings_sel == 0 and self.adjusting,
        )
        # слайдер эффектов
        self._draw_slider(
            "Громкость эффектов",
            self.sfx_volume,
            380,
            self.settings_sel == 1 and self.adjusting,
        )

        # кнопка "Назад"
        self._draw_menu_item(
            "НАЗАД",
            530,
            self.settings_sel == 2,
        )

        # подсказка
        if self.adjusting:
            self._draw_text(
                "Стрелки влево/вправо — изменить  |  Enter — подтвердить",
                self.f_sm,
                self.C_HINT,
                (WIDTH // 2, HEIGHT - 30),
            )
        else:
            self._draw_text(
                "Enter — выбрать  |  ESC — назад",
                self.f_sm,
                self.C_HINT,
                (WIDTH // 2, HEIGHT - 30),
            )

    # ----- Титры -----
    def _draw_credits(self):
        self._draw_text(
            "ТИТРЫ",
            self.f_lg,
            self.C_TITLE,
            (WIDTH // 2, 50),
        )

        # Область клиппинга для титров
        clip_top = 100
        clip_bot = HEIGHT - 60
        cx = WIDTH // 2

        y = clip_top + 20 - self.credits_scroll
        for person in self.credits_data:
            # Имя
            if clip_top < y < clip_bot:
                self._draw_text(
                    person["name"],
                    self.f_md,
                    self.C_CREDIT_NAME,
                    (cx, y),
                )
            y += 38

            # Роль
            if clip_top < y < clip_bot:
                self._draw_text(
                    person["role"],
                    self.f_sm,
                    self.C_CREDIT_ROLE,
                    (cx, y),
                )
            y += 28

            # Список вкладов
            for line in person["contribs"]:
                if clip_top < y < clip_bot:
                    self._draw_text(
                        line,
                        self.f_sm,
                        self.C_CREDIT_LIST,
                        (cx, y),
                    )
                y += 24

            y += 40   # отступ между блоками

        self._draw_text(
            "Стрелки вверх/вниз — прокрутка  |  ESC — назад",
            self.f_sm,
            self.C_HINT,
            (cx, HEIGHT - 28),
        )
