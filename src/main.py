import random
import pygame

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Window Settings
# -----------------------------
WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Operation Aerospace 2026")

# -----------------------------
# Colors
# -----------------------------
SPACE = (15, 15, 30)
EARTH_BLUE = (50, 120, 255)
SATELLITE_RED = (255, 0, 0)

# -----------------------------
# Earth Properties
# -----------------------------
EARTH_RADIUS = 60

earth_x = WIDTH // 2
earth_y = HEIGHT // 2

# -----------------------------
# Satellite Properties
# -----------------------------
SATELLITE_RADIUS = 30
SATELLITE_DISTANCE = 150

satellite_x = earth_x + SATELLITE_DISTANCE
satellite_y = earth_y

print(satellite_x)
print(satellite_y)
# -----------------------------
# Main Game Loop
# -----------------------------
running = True

while running:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with space color
    screen.fill(SPACE)

    # Draw random stars
    for i in range(200):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (star_x, star_y),
            2
        )

    # Draw Earth
    pygame.draw.circle(
        screen,
        EARTH_BLUE,
        (earth_x, earth_y),
        EARTH_RADIUS
    )

    # Draw Satellite
    pygame.draw.circle(
        screen,
        SATELLITE_RED,
        (satellite_x, satellite_y),
        SATELLITE_RADIUS
    )

    # Update the display
    pygame.display.flip()

pygame.quit()