import math


def update_satellite(
    satellite_x,
    satellite_y,
    satellite_velocity_x,
    satellite_velocity_y,
    dt,
):
    """Update the satellite position using velocity and delta time."""
    # Multiplying velocity by delta time keeps movement
    # consistent even if the frame rate changes.
    satellite_x += satellite_velocity_x * dt
    satellite_y += satellite_velocity_y * dt

    return satellite_x, satellite_y


def calculate_distance(earth_x, earth_y, satellite_x, satellite_y):
    """Calculate the straight-line distance from Earth to the satellite."""
    # dx and dy are the horizontal and vertical distances between the objects.
    dx = satellite_x - earth_x
    dy = satellite_y - earth_y

    # The Pythagorean Theorem finds the straight-line distance.
    distance = math.sqrt(dx ** 2 + dy ** 2)

    return distance
