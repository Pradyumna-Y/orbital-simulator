import pygame
from stars import STAR_COORDINATES

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Font Setup
# -----------------------------
font = pygame.font.SysFont(None, 28)

# -----------------------------
# Text Rendering
# -----------------------------
earth_label = font.render("Earth", True, (255, 255, 255))
satellite_label = font.render("Satellite", True, (255, 255, 255))

# -----------------------------
# Window Settings
# -----------------------------
WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# A Clock object helps control how often the simulation updates.
clock = pygame.time.Clock()

# FPS means frames per second. Limiting FPS keeps simulation speed consistent.
FPS = 60

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

# Velocity changes the satellite position every frame.
satellite_velocity_x = 120
satellite_velocity_y = 0

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
    for star in STAR_COORDINATES:

        pygame.draw.circle(
            screen,
            (255,255,255),
            star,
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

    # Draw labels below Earth and the satellite
    screen.blit(
        earth_label,
        (earth_x - earth_label.get_width() // 2, earth_y + EARTH_RADIUS + 10)
    )
    screen.blit(
        satellite_label,
        (satellite_x - satellite_label.get_width() // 2, satellite_y + SATELLITE_RADIUS + 10)
    )

    # Update the display
    pygame.display.flip()

    # Delta time is the time that passed since the previous frame.
    # clock.tick returns milliseconds, so dividing by 1000 converts it to seconds.
    dt = clock.tick(FPS) / 1000

    # Multiplying velocity by dt makes movement independent of the frame rate.
    satellite_x += satellite_velocity_x * dt
    satellite_y += satellite_velocity_y * dt

pygame.quit()
