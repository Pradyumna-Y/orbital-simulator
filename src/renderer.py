import pygame


def draw_stars(screen, star_coordinates, color):
    """Draw the fixed star field."""
    for star in star_coordinates:
        pygame.draw.circle(screen, color, star, 2)


def draw_earth(screen, earth_x, earth_y, radius, color):
    """Draw Earth at its current position."""
    pygame.draw.circle(screen, color, (earth_x, earth_y), radius)


def draw_satellite(screen, satellite_x, satellite_y, radius, color):
    """Draw the satellite at its current position."""
    pygame.draw.circle(screen, color, (satellite_x, satellite_y), radius)


def draw_labels(
    screen,
    earth_label,
    satellite_label,
    earth_x,
    earth_y,
    earth_radius,
    satellite_x,
    satellite_y,
    satellite_radius,
):
    """Draw labels below Earth and the satellite."""
    screen.blit(
        earth_label,
        (
            earth_x - earth_label.get_width() // 2,
            earth_y + earth_radius + 10,
        ),
    )
    screen.blit(
        satellite_label,
        (
            satellite_x - satellite_label.get_width() // 2,
            satellite_y + satellite_radius + 10,
        ),
    )


def draw_distance(screen, distance, font, color):
    """Draw the Earth-to-satellite distance in the upper-left corner."""
    distance_text = font.render(f"Distance: {distance:.2f} px", True, color)
    screen.blit(distance_text, (20, 20))


def draw_direction(screen, direction_x, direction_y, font, color):
    """Draw the Earth-to-satellite direction values below the distance."""
    direction_x_text = font.render(f"Direction X: {direction_x:.3f}", True, color)
    direction_y_text = font.render(f"Direction Y: {direction_y:.3f}", True, color)
    screen.blit(direction_x_text, (20, 55))
    screen.blit(direction_y_text, (20, 90))


def draw_velocity(screen, velocity_x, velocity_y, font, color):
    """Draw the satellite velocity values below the direction telemetry."""
    velocity_x_text = font.render(f"Velocity X: {velocity_x:.2f}", True, color)
    velocity_y_text = font.render(f"Velocity Y: {velocity_y:.2f}", True, color)
    screen.blit(velocity_x_text, (20, 125))
    screen.blit(velocity_y_text, (20, 160))


def draw_acceleration(screen, acceleration_x, acceleration_y, font, color):
    """Draw the satellite acceleration values below the velocity telemetry."""
    acceleration_x_text = font.render(
        f"Acceleration X: {acceleration_x:.2f}", True, color
    )
    acceleration_y_text = font.render(
        f"Acceleration Y: {acceleration_y:.2f}", True, color
    )
    screen.blit(acceleration_x_text, (20, 195))
    screen.blit(acceleration_y_text, (20, 230))


def draw_gravity(screen, gravity, font, color):
    """Draw the simplified gravity value below the acceleration telemetry."""
    gravity_label = font.render("Gravity:", True, color)
    gravity_value = font.render(f"{gravity:.4f}", True, color)
    screen.blit(gravity_label, (20, 265))
    screen.blit(gravity_value, (20, 300))


def draw_orbital_velocity(screen, orbital_velocity, font, color):
    """Draw the theoretical circular orbital velocity below gravity."""
    orbital_velocity_text = font.render(
        f"Orbital Velocity: {orbital_velocity:.2f} px/s", True, color
    )
    screen.blit(orbital_velocity_text, (20, 335))
