import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 700

SPACE = (15, 15, 30)
EARTH_BLUE = (50, 120, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Operation Aerospace 2026")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SPACE)

    pygame.draw.circle(
        screen,
        EARTH_BLUE,
        (WIDTH // 2, HEIGHT // 2),
        60
    )

    pygame.display.flip()

pygame.quit()