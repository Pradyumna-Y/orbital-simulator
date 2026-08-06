import math

from constants import GRAVITY_STRENGTH


def update_satellite(
    satellite_x,
    satellite_y,
    satellite_velocity_x,
    satellite_velocity_y,
    satellite_acceleration_x,
    satellite_acceleration_y,
    dt,
):
    """Update the satellite velocity and position using acceleration and time."""
    # Acceleration changes velocity over time.
    satellite_velocity_x += satellite_acceleration_x * dt
    satellite_velocity_y += satellite_acceleration_y * dt

    # Multiplying velocity by delta time changes position and keeps movement
    # consistent even if the frame rate changes.
    satellite_x += satellite_velocity_x * dt
    satellite_y += satellite_velocity_y * dt

    return satellite_x, satellite_y, satellite_velocity_x, satellite_velocity_y


def calculate_distance(earth_x, earth_y, satellite_x, satellite_y):
    """Calculate the straight-line distance from Earth to the satellite."""
    # dx and dy are the horizontal and vertical distances between the objects.
    dx = satellite_x - earth_x
    dy = satellite_y - earth_y

    # The Pythagorean Theorem finds the straight-line distance.
    distance = math.sqrt(dx ** 2 + dy ** 2)

    return distance


def calculate_direction(earth_x, earth_y, satellite_x, satellite_y):
    """Calculate the unit direction from Earth to the satellite."""
    # dx and dy describe the direction from Earth toward the satellite.
    dx = satellite_x - earth_x
    dy = satellite_y - earth_y

    # Reuse the distance calculation to normalize the direction values.
    distance = calculate_distance(earth_x, earth_y, satellite_x, satellite_y)

    # A zero distance has no direction, and this avoids division by zero.
    if distance == 0:
        return 0.0, 0.0

    # Dividing by distance creates a unit vector with a length of one.
    unit_x = dx / distance
    unit_y = dy / distance

    return unit_x, unit_y


def calculate_gravity(distance):
    """Calculate simplified gravity magnitude using inverse-square distance."""
    # A zero distance avoids division by zero.
    if distance == 0:
        return 0

    # Gravity becomes weaker as the square of distance becomes larger.
    gravity = GRAVITY_STRENGTH / (distance ** 2)

    return gravity
