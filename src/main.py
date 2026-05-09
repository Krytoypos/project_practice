import pygame
pygame.init()

WIDTH, HEIGHT = 1280, 720 # РАЗМЕР ОКНА
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Visual Novel")  # НАЗВАНИЕ ИГРЫ

font = pygame.font.SysFont("Arial", 36)  # ШРИФТ


running = True # ИНДИКАТОР
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50,50,50)) # ФОН

    text_surface = font.render("Привет, это начало новой новеллы!", True, (255,255,255))
    screen.blit(text_surface, (50,50))

    pygame.display.flip()

pygame.quit() # ЗАКРЫТИЕ ОКНА