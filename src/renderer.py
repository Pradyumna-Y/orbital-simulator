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
