import pygame
from constants import (
    EARTH_BLUE,
    EARTH_RADIUS,
    FPS,
    HEIGHT,
    SATELLITE_DISTANCE,
    SATELLITE_RADIUS,
    SATELLITE_RED,
    SPACE,
    WHITE,
    WIDTH,
)
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
earth_label = font.render("Earth", True, WHITE)
satellite_label = font.render("Satellite", True, WHITE)

# -----------------------------
# Window Settings
# -----------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Operation Aerospace 2026")

# -----------------------------
# Simulation Timing
# -----------------------------
clock = pygame.time.Clock()

# -----------------------------
# Earth Properties
# -----------------------------
earth_x = WIDTH // 2
earth_y = HEIGHT // 2

# -----------------------------
# Satellite Properties
# -----------------------------
# Velocity is measured in pixels per second.
satellite_velocity_x = 120
satellite_velocity_y = 0

satellite_x = earth_x + SATELLITE_DISTANCE
satellite_y = earth_y

# -----------------------------
# Main Game Loop
# -----------------------------
running = True

while running:

    # -----------------------------
    # Handle Events
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # Clear Screen
    # -----------------------------
    screen.fill(SPACE)

    # -----------------------------
    # Draw Star Field
    # -----------------------------
    for star in STAR_COORDINATES:
        pygame.draw.circle(
            screen,
            WHITE,
            star,
            2
        )

    # -----------------------------
    # Draw Earth
    # -----------------------------
    pygame.draw.circle(
        screen,
        EARTH_BLUE,
        (earth_x, earth_y),
        EARTH_RADIUS
    )

    # -----------------------------
    # Draw Satellite
    # -----------------------------
    pygame.draw.circle(
        screen,
        SATELLITE_RED,
        (satellite_x, satellite_y),
        SATELLITE_RADIUS
    )

    # -----------------------------
    # Draw Labels
    # -----------------------------
    screen.blit(
        earth_label,
        (
            earth_x - earth_label.get_width() // 2,
            earth_y + EARTH_RADIUS + 10
        )
    )

    screen.blit(
        satellite_label,
        (
            satellite_x - satellite_label.get_width() // 2,
            satellite_y + SATELLITE_RADIUS + 10
        )
    )

    # -----------------------------
    # Update Display
    # -----------------------------
    pygame.display.flip()

    # -----------------------------
    # Calculate Delta Time
    # -----------------------------
    # clock.tick() returns the time since the previous frame in milliseconds.
    # Dividing by 1000 converts milliseconds to seconds.
    dt = clock.tick(FPS) / 1000

    # -----------------------------
    # Update Satellite Position
    # -----------------------------
    # Multiplying velocity by delta time keeps movement
    # consistent even if the frame rate changes.
    satellite_x += satellite_velocity_x * dt
    satellite_y += satellite_velocity_y * dt

# -----------------------------
# Shut Down Pygame
# -----------------------------
pygame.quit()
