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
from renderer import (
    draw_acceleration,
    draw_direction,
    draw_distance,
    draw_earth,
    draw_gravity,
    draw_labels,
    draw_orbital_velocity,
    draw_satellite,
    draw_stars,
    draw_velocity,
)
from simulation import (
    calculate_direction,
    calculate_distance,
    calculate_gravity,
    calculate_orbital_velocity,
    update_satellite,
)

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
satellite_x = earth_x + SATELLITE_DISTANCE
satellite_y = earth_y

# Calculate the orbital speed from the satellite's initial distance from Earth.
initial_distance = calculate_distance(earth_x, earth_y, satellite_x, satellite_y)
initial_orbital_velocity = calculate_orbital_velocity(initial_distance)

# Orbital velocity is perpendicular to the radius, so the satellite starts upward.
# This creates a counterclockwise orbit from a starting point right of Earth.
satellite_velocity_x = 0
satellite_velocity_y = -initial_orbital_velocity

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
    # Calculate Earth-Satellite Distance
    # -----------------------------
    distance = calculate_distance(earth_x, earth_y, satellite_x, satellite_y)

    # -----------------------------
    # Calculate Earth-Satellite Direction
    # -----------------------------
    direction_x, direction_y = calculate_direction(
        earth_x,
        earth_y,
        satellite_x,
        satellite_y,
    )

    # -----------------------------
    # Calculate Simplified Gravity
    # -----------------------------
    gravity = calculate_gravity(distance)

    # Calculate the circular-orbit speed for HUD telemetry only.
    orbital_velocity = calculate_orbital_velocity(distance)

    # -----------------------------
    # Calculate Gravitational Acceleration
    # -----------------------------
    # Gravity magnitude and direction combine to create acceleration.
    # The negative sign points the acceleration back toward Earth.
    satellite_acceleration_x = -gravity * direction_x
    satellite_acceleration_y = -gravity * direction_y

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
    # Draw Distance Telemetry
    # -----------------------------
    draw_distance(screen, distance, font, WHITE)
    draw_direction(screen, direction_x, direction_y, font, WHITE)
    draw_velocity(screen, satellite_velocity_x, satellite_velocity_y, font, WHITE)
    draw_acceleration(
        screen,
        satellite_acceleration_x,
        satellite_acceleration_y,
        font,
        WHITE,
    )
    draw_gravity(screen, gravity, font, WHITE)
    draw_orbital_velocity(screen, orbital_velocity, font, WHITE)

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
    (
        satellite_x,
        satellite_y,
        satellite_velocity_x,
        satellite_velocity_y,
    ) = update_satellite(
        satellite_x,
        satellite_y,
        satellite_velocity_x,
        satellite_velocity_y,
        satellite_acceleration_x,
        satellite_acceleration_y,
        dt,
    )

# -----------------------------
# Shut Down Pygame
# -----------------------------
pygame.quit()
