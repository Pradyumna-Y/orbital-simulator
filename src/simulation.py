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


def calculate_orbital_velocity(distance):
    """Calculate the theoretical circular orbital velocity at a distance."""
    # A zero distance avoids division by zero.
    if distance == 0:
        return 0

    # This equation comes from balancing gravity with centripetal acceleration.
    orbital_velocity = math.sqrt(GRAVITY_STRENGTH / distance)

    return orbital_velocity


def calculate_escape_velocity(gravity_strength, distance):
    """Calculate the minimum speed needed to escape the gravity model."""
    # A non-positive distance avoids division by zero or an invalid result.
    if distance <= 0:
        return 0

    escape_velocity = math.sqrt((2 * gravity_strength) / distance)

    return escape_velocity


def calculate_orbital_period(distance, orbital_velocity):
    """Calculate the time required for one complete circular revolution."""
    # A zero velocity cannot complete an orbit and would cause division by zero.
    if orbital_velocity == 0:
        return 0

    # One complete orbit travels the circumference of a circle.
    circumference = 2 * math.pi * distance
    orbital_period = circumference / orbital_velocity

    return orbital_period


def calculate_semi_major_axis(periapsis, apoapsis):
    """Calculate the semi-major axis from the nearest and farthest distances."""
    # The semi-major axis is the average of periapsis and apoapsis.
    semi_major_axis = (periapsis + apoapsis) / 2

    return semi_major_axis


def calculate_eccentricity(periapsis, apoapsis):
    """Calculate how much the generated orbit differs from a circle."""
    # Eccentricity compares the difference between apoapsis and periapsis
    # with their total distance. A circle has an eccentricity of zero.
    denominator = apoapsis + periapsis

    if denominator == 0:
        return 0

    eccentricity = (apoapsis - periapsis) / denominator

    return eccentricity


def calculate_focus_distance(semi_major_axis, eccentricity):
    """Calculate the distance from the center of an ellipse to a focus."""
    # In an ellipse, focus distance equals semi-major axis times eccentricity.
    focus_distance = semi_major_axis * eccentricity

    return focus_distance


def calculate_swept_area(
    earth_x,
    earth_y,
    previous_x,
    previous_y,
    current_x,
    current_y,
):
    """Calculate the triangle area swept from Earth between two positions."""
    # The cross product gives twice the signed triangle area.
    area = abs(
        (previous_x - earth_x) * (current_y - earth_y)
        - (previous_y - earth_y) * (current_x - earth_x)
    ) / 2

    return area


def calculate_speed(velocity_x, velocity_y):
    """Calculate satellite speed from its horizontal and vertical velocities."""
    speed = math.sqrt(velocity_x ** 2 + velocity_y ** 2)

    return speed


def calculate_kepler_third_law_ratio(period, semi_major_axis):
    """Calculate the T squared over a cubed value for an orbit."""
    # A zero semi-major axis would cause division by zero.
    if semi_major_axis == 0:
        return 0

    ratio = (period ** 2) / (semi_major_axis ** 3)

    return ratio


def calculate_theoretical_kepler_ratio():
    """Calculate Kepler's Third Law ratio for the simulation gravity model."""
    theoretical_ratio = (4 * math.pi ** 2) / GRAVITY_STRENGTH

    return theoretical_ratio
