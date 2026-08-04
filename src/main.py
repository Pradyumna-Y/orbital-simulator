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
from renderer import draw_earth, draw_labels, draw_satellite, draw_stars

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
    draw_stars(screen, STAR_COORDINATES, WHITE)

    # -----------------------------
    # Draw Earth
    # -----------------------------
    draw_earth(screen, earth_x, earth_y, EARTH_RADIUS, EARTH_BLUE)

    # -----------------------------
    # Draw Satellite
    # -----------------------------
    draw_satellite(
        screen,
        satellite_x,
        satellite_y,
        SATELLITE_RADIUS,
        SATELLITE_RED,
    )

    # -----------------------------
    # Draw Labels
    # -----------------------------
    draw_labels(
        screen,
        earth_label,
        satellite_label,
        earth_x,
        earth_y,
        EARTH_RADIUS,
        satellite_x,
        satellite_y,
        SATELLITE_RADIUS,
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
