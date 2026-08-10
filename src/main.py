import math

import pygame
from constants import (
    EARTH_BLUE,
    EARTH_RADIUS,
    EARTH_RADIUS_KM,
    EARTH_MU,
    ESCAPE_TEST_MODE,
    ESCAPE_TEST_SCALE,
    FPS,
    HEIGHT,
    INITIAL_ORBIT_RADIUS_KM,
    KEPLER_AREA_INTERVAL,
    MAX_TRAIL_POINTS,
    MAX_SWEPT_AREA_SAMPLES,
    KM_PER_PIXEL,
    ORBIT_VELOCITY_SCALE,
    SATELLITE_RADIUS,
    SATELLITE_RED,
    SPACE,
    WHITE,
    WIDTH,
)
from stars import STAR_COORDINATES
from renderer import (
    draw_acceleration,
    draw_controls_hint,
    draw_engineering_hud,
    draw_direction,
    draw_distance,
    draw_distance_stability,
    draw_earth,
    draw_motion_vectors,
    draw_escape_telemetry,
    draw_orbital_energy,
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
    calculate_specific_orbital_energy,
    classify_orbit,
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
hud_title_font = pygame.font.SysFont(None, 20)
hud_body_font = pygame.font.SysFont(None, 18)

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
# Earth Screen Position
# -----------------------------
earth_screen_x = WIDTH // 2
earth_screen_y = HEIGHT // 2

# -----------------------------
# Kilometer-Based Physics State
# -----------------------------
# Earth is the physics origin; satellite position is relative to Earth in km.
earth_x_km = 0.0
earth_y_km = 0.0


def reset_simulation():
    """Restore the satellite and all analysis measurements to their initial state."""
    global satellite_x_km, satellite_y_km
    global satellite_velocity_x_km_s, satellite_velocity_y_km_s
    global initial_distance, initial_orbital_velocity, initial_escape_velocity
    global initial_velocity, initial_orbital_period, orbit_mode
    global minimum_distance, maximum_distance, orbit_trail
    global simulation_time, previous_angle, accumulated_angle
    global measured_orbital_period, period_error, percent_error
    global kepler_interval_time, previous_sample_x_km, previous_sample_y_km
    global swept_areas, initial_speed, maximum_speed, minimum_speed

    satellite_x_km = INITIAL_ORBIT_RADIUS_KM
    satellite_y_km = 0.0

    initial_distance = calculate_distance(
        earth_x_km,
        earth_y_km,
        satellite_x_km,
        satellite_y_km,
    )
    initial_orbital_velocity = calculate_orbital_velocity(initial_distance)
    initial_escape_velocity = calculate_escape_velocity(EARTH_MU, initial_distance)

    # Normal mode uses scaled circular speed; escape mode uses the escape speed.
    if ESCAPE_TEST_MODE:
        initial_velocity = initial_escape_velocity * ESCAPE_TEST_SCALE
        orbit_mode = "Escape Test"
    else:
        initial_velocity = initial_orbital_velocity * ORBIT_VELOCITY_SCALE
        orbit_mode = "Elliptical"

    initial_orbital_period = calculate_orbital_period(
        initial_distance,
        initial_orbital_velocity,
    )
    minimum_distance = initial_distance
    maximum_distance = initial_distance

    # Orbital velocity is perpendicular to the radius at the starting position.
    satellite_velocity_x_km_s = 0.0
    satellite_velocity_y_km_s = -initial_velocity

    orbit_trail = []
    simulation_time = 0.0
    previous_angle = math.atan2(
        satellite_y_km - earth_y_km,
        satellite_x_km - earth_x_km,
    )
    accumulated_angle = 0.0
    measured_orbital_period = None
    period_error = None
    percent_error = None

    kepler_interval_time = 0.0
    previous_sample_x_km = satellite_x_km
    previous_sample_y_km = satellite_y_km
    swept_areas = []

    initial_speed = calculate_speed(
        satellite_velocity_x_km_s,
        satellite_velocity_y_km_s,
    )
    maximum_speed = initial_speed
    minimum_speed = initial_speed


reset_simulation()

# User interface state does not alter the physics model.
paused = False
show_trail = True
show_hud = True

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                reset_simulation()
                paused = False
            elif event.key == pygame.K_t:
                show_trail = not show_trail
            elif event.key == pygame.K_h:
                show_hud = not show_hud

    # -----------------------------
    # Calculate Earth-Satellite Distance
    # -----------------------------
    distance = calculate_distance(
        earth_x_km,
        earth_y_km,
        satellite_x_km,
        satellite_y_km,
    )
    altitude = distance - EARTH_RADIUS_KM

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
    current_speed = calculate_speed(
        satellite_velocity_x_km_s,
        satellite_velocity_y_km_s,
    )
    maximum_speed = max(maximum_speed, current_speed)
    minimum_speed = min(minimum_speed, current_speed)

    # Specific orbital energy determines whether gravity can keep the orbit bound.
    specific_energy = calculate_specific_orbital_energy(
        current_speed,
        EARTH_MU,
        distance,
    )
    orbit_classification = classify_orbit(specific_energy)

    # -----------------------------
    # Calculate Earth-Satellite Direction
    # -----------------------------
    direction_x, direction_y = calculate_direction(
        earth_x_km,
        earth_y_km,
        satellite_x_km,
        satellite_y_km,
    )

    # -----------------------------
    # Calculate Simplified Gravity
    # -----------------------------
    gravity = calculate_gravity(distance)

    # Calculate the circular-orbit speed for HUD telemetry only.
    orbital_velocity = calculate_orbital_velocity(distance)
    escape_velocity = calculate_escape_velocity(EARTH_MU, distance)

    # -----------------------------
    # Calculate Gravitational Acceleration
    # -----------------------------
    # Gravity magnitude and direction combine to create acceleration.
    # The negative sign points the acceleration back toward Earth.
    satellite_acceleration_x_km_s2 = -gravity * direction_x
    satellite_acceleration_y_km_s2 = -gravity * direction_y

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
    if show_trail:
        draw_orbit_trail(
            screen,
            earth_screen_x,
            earth_screen_y,
            orbit_trail,
            KM_PER_PIXEL,
        )

    # -----------------------------
    # Draw Earth
    # -----------------------------
    draw_earth(screen, earth_screen_x, earth_screen_y, EARTH_RADIUS, EARTH_BLUE)

    # -----------------------------
    # Draw Satellite
    # -----------------------------
    draw_satellite(
        screen,
        earth_screen_x,
        earth_screen_y,
        satellite_x_km,
        satellite_y_km,
        KM_PER_PIXEL,
        SATELLITE_RADIUS,
        SATELLITE_RED,
    )

    draw_motion_vectors(
        screen,
        earth_screen_x,
        earth_screen_y,
        satellite_x_km,
        satellite_y_km,
        KM_PER_PIXEL,
        satellite_velocity_x_km_s,
        satellite_velocity_y_km_s,
        satellite_acceleration_x_km_s2,
        satellite_acceleration_y_km_s2,
        hud_body_font,
    )

    # -----------------------------
    # Draw Labels
    # -----------------------------
    draw_labels(
        screen,
        earth_label,
        satellite_label,
        earth_screen_x,
        earth_screen_y,
        EARTH_RADIUS,
        satellite_x_km,
        satellite_y_km,
        KM_PER_PIXEL,
        SATELLITE_RADIUS,
    )

    # -----------------------------
    # Draw Distance Telemetry
    # -----------------------------
    if show_hud:
        draw_engineering_hud(
            screen,
            hud_title_font,
            hud_body_font,
            WHITE,
            altitude,
            distance,
            current_speed,
            orbit_classification,
            periapsis,
            apoapsis,
            semi_major_axis,
            eccentricity,
            initial_orbital_period,
            measured_orbital_period,
            swept_areas,
            kepler_ratio_error,
            simulation_time,
            paused,
        )

    # -----------------------------
    # Update Display
    # -----------------------------
    pygame.display.flip()

    # -----------------------------
    # Calculate Delta Time
    # -----------------------------
    # clock.tick() returns the time since the previous frame in milliseconds.
    # Paused frames are rendered but do not advance simulation state.
    frame_time_ms = clock.tick(FPS)
    if paused:
        continue

    # Dividing by 1000 converts milliseconds to seconds.
    dt = frame_time_ms / 1000

    # -----------------------------
    # Update Satellite Position
    # -----------------------------
    (
        satellite_x_km,
        satellite_y_km,
        satellite_velocity_x_km_s,
        satellite_velocity_y_km_s,
    ) = update_satellite(
        satellite_x_km,
        satellite_y_km,
        satellite_velocity_x_km_s,
        satellite_velocity_y_km_s,
        satellite_acceleration_x_km_s2,
        satellite_acceleration_y_km_s2,
        dt,
    )

    # Delta time accumulates the elapsed time of the numerical simulation.
    simulation_time += dt

    # Sample the physics-generated path at equal simulation-time intervals.
    kepler_interval_time += dt
    if kepler_interval_time >= KEPLER_AREA_INTERVAL:
        swept_area = calculate_swept_area(
            earth_x_km,
            earth_y_km,
            previous_sample_x_km,
            previous_sample_y_km,
            satellite_x_km,
            satellite_y_km,
        )
        swept_areas.append(swept_area)

        # Keep a recent set of interval areas for comparison in the HUD.
        if len(swept_areas) > MAX_SWEPT_AREA_SAMPLES:
            swept_areas.pop(0)

        previous_sample_x_km = satellite_x_km
        previous_sample_y_km = satellite_y_km
        kepler_interval_time -= KEPLER_AREA_INTERVAL

    # Measure the satellite's angle around Earth after the physics update.
    current_angle = math.atan2(
        satellite_y_km - earth_y_km,
        satellite_x_km - earth_x_km,
    )
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
    orbit_trail.append((satellite_x_km, satellite_y_km))

    # Keep the recent trail history bounded as the simulation runs.
    if len(orbit_trail) > MAX_TRAIL_POINTS:
        orbit_trail.pop(0)

# -----------------------------
# Shut Down Pygame
# -----------------------------
pygame.quit()
