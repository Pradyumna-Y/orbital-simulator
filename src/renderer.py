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
