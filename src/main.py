import math

import pygame
from constants import (
    EARTH_BLUE,
    EARTH_RADIUS,
    ESCAPE_TEST_MODE,
    ESCAPE_TEST_SCALE,
    FPS,
    GRAVITY_STRENGTH,
    HEIGHT,
    KEPLER_AREA_INTERVAL,
    MAX_TRAIL_POINTS,
    MAX_SWEPT_AREA_SAMPLES,
    ORBIT_VELOCITY_SCALE,
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
    draw_distance_stability,
    draw_earth,
    draw_escape_telemetry,
    draw_gravity,
    draw_labels,
    draw_orbital_velocity,
    draw_orbital_period,
    draw_orbit_trail,
    draw_orbit_velocity_scale,
    draw_orbit_shape,
    draw_kepler_first_law,
    draw_kepler_second_law,
    draw_kepler_third_law,
    draw_measured_period,
    draw_satellite,
    draw_stars,
    draw_velocity,
)
from simulation import (
    calculate_direction,
    calculate_distance,
    calculate_escape_velocity,
    calculate_gravity,
    calculate_orbital_velocity,
    calculate_orbital_period,
    calculate_semi_major_axis,
    calculate_eccentricity,
    calculate_focus_distance,
    calculate_speed,
    calculate_swept_area,
    calculate_kepler_third_law_ratio,
    calculate_theoretical_kepler_ratio,
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
initial_escape_velocity = calculate_escape_velocity(
    GRAVITY_STRENGTH,
    initial_distance,
)

# Normal mode uses scaled circular speed; escape mode uses the escape speed.
if ESCAPE_TEST_MODE:
    initial_velocity = initial_escape_velocity * ESCAPE_TEST_SCALE
    orbit_mode = "Escape Test"
else:
    initial_velocity = initial_orbital_velocity * ORBIT_VELOCITY_SCALE
    orbit_mode = "Elliptical"

# Orbital period is the time required for one complete revolution.
initial_orbital_period = calculate_orbital_period(
    initial_distance,
    initial_orbital_velocity,
)

# A perfect circular orbit would keep this distance range at zero.
minimum_distance = initial_distance
maximum_distance = initial_distance

# Orbital velocity is perpendicular to the radius, so the satellite starts upward.
# Scaling the circular speed lets gravity create an elliptical orbit naturally.
satellite_velocity_x = 0
satellite_velocity_y = -initial_velocity

# Engineers use trajectory trails to evaluate the shape and stability of an orbit.
orbit_trail = []

# Track the first complete simulated revolution for period comparison.
simulation_time = 0
previous_angle = math.atan2(satellite_y - earth_y, satellite_x - earth_x)
accumulated_angle = 0
measured_orbital_period = None
period_error = None
percent_error = None

# Start each Kepler II interval from the satellite's current position.
kepler_interval_time = 0
previous_sample_x = satellite_x
previous_sample_y = satellite_y
swept_areas = []

# Speed changes naturally as gravity accelerates the satellite around Earth.
initial_speed = calculate_speed(satellite_velocity_x, satellite_velocity_y)
maximum_speed = initial_speed
minimum_speed = initial_speed

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

    # Track radial variation to measure orbit stability and circularity.
    minimum_distance = min(minimum_distance, distance)
    maximum_distance = max(maximum_distance, distance)
    distance_range = maximum_distance - minimum_distance

    # Periapsis is the closest point to Earth; apoapsis is the farthest.
    periapsis = minimum_distance
    apoapsis = maximum_distance

    # These values describe the size and shape of the physics-generated orbit.
    semi_major_axis = calculate_semi_major_axis(periapsis, apoapsis)
    eccentricity = calculate_eccentricity(periapsis, apoapsis)
    focus_distance = calculate_focus_distance(semi_major_axis, eccentricity)

    # Kepler's Third Law compares period squared with semi-major axis cubed.
    theoretical_kepler_ratio = calculate_theoretical_kepler_ratio()
    if measured_orbital_period is None:
        measured_kepler_ratio = None
        kepler_ratio_error = None
    else:
        measured_kepler_ratio = calculate_kepler_third_law_ratio(
            measured_orbital_period,
            semi_major_axis,
        )
        kepler_ratio_error = (
            abs(measured_kepler_ratio - theoretical_kepler_ratio)
            / theoretical_kepler_ratio
            * 100
        )

    # Speed is the magnitude of the current horizontal and vertical velocity.
    current_speed = calculate_speed(satellite_velocity_x, satellite_velocity_y)
    maximum_speed = max(maximum_speed, current_speed)
    minimum_speed = min(minimum_speed, current_speed)

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
    escape_velocity = calculate_escape_velocity(GRAVITY_STRENGTH, distance)

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
    # Draw Orbit Trail
    # -----------------------------
    draw_orbit_trail(screen, orbit_trail)

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
    draw_escape_telemetry(screen, escape_velocity, orbit_mode, font, WHITE)
    draw_distance_stability(
        screen,
        minimum_distance,
        maximum_distance,
        distance_range,
        font,
        WHITE,
    )
    draw_orbital_period(screen, initial_orbital_period, font, WHITE)
    draw_measured_period(screen, measured_orbital_period, percent_error, font, WHITE)
    draw_orbit_velocity_scale(screen, ORBIT_VELOCITY_SCALE, font, WHITE)
    draw_orbit_shape(
        screen,
        periapsis,
        apoapsis,
        semi_major_axis,
        eccentricity,
        focus_distance,
        font,
        WHITE,
    )
    draw_kepler_first_law(screen, font, WHITE)
    draw_kepler_second_law(
        screen,
        KEPLER_AREA_INTERVAL,
        swept_areas,
        current_speed,
        maximum_speed,
        minimum_speed,
        font,
        WHITE,
    )
    draw_kepler_third_law(
        screen,
        measured_kepler_ratio,
        theoretical_kepler_ratio,
        kepler_ratio_error,
        font,
        WHITE,
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

    # Delta time accumulates the elapsed time of the numerical simulation.
    simulation_time += dt

    # Sample the physics-generated path at equal simulation-time intervals.
    kepler_interval_time += dt
    if kepler_interval_time >= KEPLER_AREA_INTERVAL:
        swept_area = calculate_swept_area(
            earth_x,
            earth_y,
            previous_sample_x,
            previous_sample_y,
            satellite_x,
            satellite_y,
        )
        swept_areas.append(swept_area)

        # Keep a recent set of interval areas for comparison in the HUD.
        if len(swept_areas) > MAX_SWEPT_AREA_SAMPLES:
            swept_areas.pop(0)

        previous_sample_x = satellite_x
        previous_sample_y = satellite_y
        kepler_interval_time -= KEPLER_AREA_INTERVAL

    # Measure the satellite's angle around Earth after the physics update.
    current_angle = math.atan2(satellite_y - earth_y, satellite_x - earth_x)
    angle_change = current_angle - previous_angle

    # Correct the jump that occurs when an angle crosses +pi or -pi.
    if angle_change > math.pi:
        angle_change -= 2 * math.pi
    elif angle_change < -math.pi:
        angle_change += 2 * math.pi

    # 2 * pi radians represents one complete revolution around Earth.
    accumulated_angle += abs(angle_change)
    previous_angle = current_angle

    # Record only the first full orbit so later revolutions do not overwrite it.
    if measured_orbital_period is None and accumulated_angle >= 2 * math.pi:
        measured_orbital_period = simulation_time
        period_error = abs(measured_orbital_period - initial_orbital_period)
        percent_error = period_error / initial_orbital_period * 100

    # Store updated positions so engineers can analyze the orbital trajectory.
    orbit_trail.append((satellite_x, satellite_y))

    # Keep the recent trail history bounded as the simulation runs.
    if len(orbit_trail) > MAX_TRAIL_POINTS:
        orbit_trail.pop(0)

# -----------------------------
# Shut Down Pygame
# -----------------------------
pygame.quit()
