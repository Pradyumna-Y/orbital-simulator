import math

import pygame

from constants import TRAIL_COLOR


def draw_stars(screen, star_field):
    """Draw stars with mostly dim points and a few softly glowing ones."""
    for x, y, radius, color, has_glow in star_field:
        if has_glow:
            # Dark, colored outer rings give only the brightest stars a glow.
            glow_color = tuple(max(1, channel // 8) for channel in color)
            pygame.draw.circle(screen, glow_color, (x, y), radius + 3)

            middle_color = tuple(max(1, channel // 4) for channel in color)
            pygame.draw.circle(screen, middle_color, (x, y), radius + 1)

        pygame.draw.circle(screen, color, (x, y), radius)


def draw_earth(screen, earth_x, earth_y, radius, color):
    """Draw Earth at its current position."""
    pygame.draw.circle(screen, color, (earth_x, earth_y), radius)


def draw_satellite(
    screen,
    earth_screen_x,
    earth_screen_y,
    satellite_x_km,
    satellite_y_km,
    km_per_pixel,
    radius,
    color,
):
    """Convert kilometer coordinates to pixels and draw the satellite."""
    screen_x = earth_screen_x + satellite_x_km / km_per_pixel
    screen_y = earth_screen_y + satellite_y_km / km_per_pixel
    pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), radius)


def draw_motion_vectors(
    screen,
    earth_screen_x,
    earth_screen_y,
    satellite_x_km,
    satellite_y_km,
    km_per_pixel,
    velocity_x,
    velocity_y,
    acceleration_x,
    acceleration_y,
    label_font,
):
    """Draw visual-only velocity and gravitational acceleration arrows."""
    start_x = earth_screen_x + satellite_x_km / km_per_pixel
    start_y = earth_screen_y + satellite_y_km / km_per_pixel

    def draw_arrow(vector_x, vector_y, length, color, label):
        magnitude = math.sqrt(vector_x ** 2 + vector_y ** 2)
        if magnitude == 0:
            return

        unit_x = vector_x / magnitude
        unit_y = vector_y / magnitude
        end_x = start_x + unit_x * length
        end_y = start_y + unit_y * length
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)

        arrow_angle = math.atan2(unit_y, unit_x)
        left_point = (
            end_x - 10 * math.cos(arrow_angle - math.pi / 6),
            end_y - 10 * math.sin(arrow_angle - math.pi / 6),
        )
        right_point = (
            end_x - 10 * math.cos(arrow_angle + math.pi / 6),
            end_y - 10 * math.sin(arrow_angle + math.pi / 6),
        )
        pygame.draw.polygon(screen, color, [(end_x, end_y), left_point, right_point])
        screen.blit(label_font.render(label, True, color), (end_x + 5, end_y + 5))

    velocity_magnitude = math.sqrt(velocity_x ** 2 + velocity_y ** 2)
    acceleration_magnitude = math.sqrt(acceleration_x ** 2 + acceleration_y ** 2)

    # These lengths are visual scaling only and do not change physics values.
    velocity_length = min(80, max(30, velocity_magnitude * 6))
    acceleration_length = min(80, max(30, acceleration_magnitude * 6000))

    draw_arrow(velocity_x, velocity_y, velocity_length, (80, 255, 130), "v")
    draw_arrow(acceleration_x, acceleration_y, acceleration_length, (255, 170, 70), "a")


def draw_orbit_trail(
    screen,
    earth_screen_x,
    earth_screen_y,
    orbit_trail,
    km_per_pixel,
):
    """Convert stored kilometer positions to pixels for the trajectory trail."""
    for position in orbit_trail:
        screen_position = (
            int(earth_screen_x + position[0] / km_per_pixel),
            int(earth_screen_y + position[1] / km_per_pixel),
        )
        pygame.draw.circle(screen, TRAIL_COLOR, screen_position, 2)


def draw_labels(
    screen,
    earth_label,
    satellite_label,
    earth_screen_x,
    earth_screen_y,
    earth_radius,
    satellite_x_km,
    satellite_y_km,
    km_per_pixel,
    satellite_radius,
):
    """Draw labels below Earth and the satellite."""
    satellite_screen_x = earth_screen_x + satellite_x_km / km_per_pixel
    satellite_screen_y = earth_screen_y + satellite_y_km / km_per_pixel
    screen.blit(
        earth_label,
        (
            earth_screen_x - earth_label.get_width() // 2,
            earth_screen_y + earth_radius + 10,
        ),
    )
    screen.blit(
        satellite_label,
        (
            int(satellite_screen_x - satellite_label.get_width() // 2),
            int(satellite_screen_y + satellite_radius + 10),
        ),
    )


def draw_distance(screen, distance_km, altitude_km, font, color):
    """Draw real-world Earth-center distance and altitude telemetry."""
    altitude_text = font.render(f"Altitude: {altitude_km:.2f} km", True, color)
    distance_text = font.render(
        f"Distance from Earth center: {distance_km:.2f} km", True, color
    )
    screen.blit(altitude_text, (20, 20))
    screen.blit(distance_text, (20, 55))


def draw_direction(screen, direction_x, direction_y, font, color):
    """Draw the Earth-to-satellite direction values below the distance."""
    direction_x_text = font.render(f"Direction X: {direction_x:.3f}", True, color)
    direction_y_text = font.render(f"Direction Y: {direction_y:.3f}", True, color)
    screen.blit(direction_x_text, (20, 90))
    screen.blit(direction_y_text, (20, 125))


def draw_velocity(screen, velocity_x, velocity_y, font, color):
    """Draw the satellite velocity values below the direction telemetry."""
    velocity_x_text = font.render(f"Velocity X: {velocity_x:.3f} km/s", True, color)
    velocity_y_text = font.render(f"Velocity Y: {velocity_y:.3f} km/s", True, color)
    screen.blit(velocity_x_text, (20, 160))
    screen.blit(velocity_y_text, (20, 195))


def draw_acceleration(screen, acceleration_x, acceleration_y, font, color):
    """Draw the satellite acceleration values below the velocity telemetry."""
    acceleration_x_text = font.render(
        f"Acceleration X: {acceleration_x:.5f} km/s^2", True, color
    )
    acceleration_y_text = font.render(
        f"Acceleration Y: {acceleration_y:.5f} km/s^2", True, color
    )
    screen.blit(acceleration_x_text, (20, 230))
    screen.blit(acceleration_y_text, (20, 265))


def draw_gravity(screen, gravity, font, color):
    """Draw the simplified gravity value below the acceleration telemetry."""
    gravity_label = font.render("Gravity:", True, color)
    gravity_value = font.render(f"{gravity:.6f} km/s^2", True, color)
    screen.blit(gravity_label, (20, 300))
    screen.blit(gravity_value, (20, 335))


def draw_orbital_velocity(screen, orbital_velocity, font, color):
    """Draw the theoretical circular orbital velocity below gravity."""
    orbital_velocity_text = font.render(
        f"Circular Velocity: {orbital_velocity:.3f} km/s", True, color
    )
    screen.blit(orbital_velocity_text, (20, 370))


def draw_escape_telemetry(screen, escape_velocity, orbit_mode, font, color):
    """Draw escape velocity and the active initial-velocity mode."""
    escape_velocity_text = font.render(
        f"Escape Velocity: {escape_velocity:.3f} km/s", True, color
    )
    orbit_mode_text = font.render(f"Orbit Mode: {orbit_mode}", True, color)
    screen.blit(escape_velocity_text, (650, 580))
    screen.blit(orbit_mode_text, (650, 615))


def draw_orbital_energy(screen, specific_energy, orbit_classification, font, color):
    """Draw the energy-based gravitational orbit classification."""
    energy_text = font.render(
        f"Specific Energy: {specific_energy:.4f} km^2/s^2", True, color
    )
    classification_text = font.render(
        f"Orbit Classification: {orbit_classification}", True, color
    )
    screen.blit(energy_text, (650, 650))
    screen.blit(classification_text, (20, 660))


def draw_distance_stability(
    screen,
    minimum_distance,
    maximum_distance,
    distance_range,
    font,
    color,
):
    """Draw distance measurements used to evaluate orbit circularity."""
    minimum_text = font.render(
        f"Minimum Distance: {minimum_distance:.2f} km", True, color
    )
    maximum_text = font.render(
        f"Maximum Distance: {maximum_distance:.2f} km", True, color
    )
    range_text = font.render(
        f"Distance Range: {distance_range:.2f} km", True, color
    )
    screen.blit(minimum_text, (20, 370))
    screen.blit(maximum_text, (20, 405))
    screen.blit(range_text, (20, 440))


def draw_orbital_period(screen, orbital_period, font, color):
    """Draw the theoretical time required for one complete revolution."""
    orbital_period_text = font.render(
        f"Theoretical Period: {orbital_period:.2f} s", True, color
    )
    screen.blit(orbital_period_text, (20, 475))


def draw_measured_period(screen, measured_period, percent_error, font, color):
    """Draw the measured period and its difference from the theory."""
    if measured_period is None:
        measured_text = font.render("Measured Period: Measuring...", True, color)
        error_text = font.render("Period Error: Measuring...", True, color)
    else:
        measured_text = font.render(
            f"Measured Period: {measured_period:.2f} s", True, color
        )
        error_text = font.render(f"Period Error: {percent_error:.2f} %", True, color)

    screen.blit(measured_text, (20, 510))
    screen.blit(error_text, (20, 545))


def draw_orbit_velocity_scale(screen, velocity_scale, font, color):
    """Draw the scale applied to the initial circular orbital velocity."""
    scale_text = font.render(f"Orbit Velocity Scale: {velocity_scale:.2f}", True, color)
    screen.blit(scale_text, (20, 580))


def draw_orbit_shape(
    screen,
    periapsis,
    apoapsis,
    semi_major_axis,
    eccentricity,
    focus_distance,
    font,
    color,
):
    """Draw calculated measurements that describe the elliptical orbit."""
    periapsis_text = font.render(f"Periapsis: {periapsis:.2f} km", True, color)
    apoapsis_text = font.render(f"Apoapsis: {apoapsis:.2f} km", True, color)
    semi_major_axis_text = font.render(
        f"Semi-major Axis: {semi_major_axis:.2f} km", True, color
    )
    eccentricity_text = font.render(f"Eccentricity: {eccentricity:.3f}", True, color)
    focus_distance_text = font.render(
        f"Focus Distance: {focus_distance:.2f} km", True, color
    )
    screen.blit(periapsis_text, (650, 20))
    screen.blit(apoapsis_text, (650, 55))
    screen.blit(semi_major_axis_text, (650, 90))
    screen.blit(eccentricity_text, (650, 125))
    screen.blit(focus_distance_text, (650, 160))


def draw_kepler_first_law(screen, font, color):
    """Draw the Kepler's First Law interpretation of the measured orbit."""
    kepler_text = font.render(
        "Kepler I: Elliptical orbit, Earth at one focus", True, color
    )
    screen.blit(kepler_text, (20, 625))


def draw_kepler_second_law(
    screen,
    area_interval,
    swept_areas,
    current_speed,
    maximum_speed,
    minimum_speed,
    font,
    color,
):
    """Draw area and speed measurements for Kepler's Second Law."""
    interval_text = font.render(
        f"Kepler II Interval: {area_interval:.2f} s", True, color
    )

    if swept_areas:
        latest_area_text = font.render(
            f"Latest Swept Area: {swept_areas[-1]:.2f} km^2", True, color
        )
        minimum_area_text = font.render(
            f"Min Swept Area: {min(swept_areas):.2f} km^2", True, color
        )
        maximum_area_text = font.render(
            f"Max Swept Area: {max(swept_areas):.2f} km^2", True, color
        )
    else:
        latest_area_text = font.render("Latest Swept Area: Measuring...", True, color)
        minimum_area_text = font.render("Min Swept Area: Measuring...", True, color)
        maximum_area_text = font.render("Max Swept Area: Measuring...", True, color)

    current_speed_text = font.render(
        f"Current Speed: {current_speed:.3f} km/s", True, color
    )
    maximum_speed_text = font.render(
        f"Maximum Speed: {maximum_speed:.3f} km/s", True, color
    )
    minimum_speed_text = font.render(
        f"Minimum Speed: {minimum_speed:.3f} km/s", True, color
    )

    screen.blit(interval_text, (650, 195))
    screen.blit(latest_area_text, (650, 230))
    screen.blit(minimum_area_text, (650, 265))
    screen.blit(maximum_area_text, (650, 300))
    screen.blit(current_speed_text, (650, 335))
    screen.blit(maximum_speed_text, (650, 370))
    screen.blit(minimum_speed_text, (650, 405))


def draw_kepler_third_law(
    screen,
    measured_ratio,
    theoretical_ratio,
    ratio_error,
    font,
    color,
):
    """Draw Kepler's Third Law measurements from the simulated orbit."""
    heading_text = font.render("Kepler III:", True, color)
    theoretical_text = font.render(
        f"Theoretical Ratio: {theoretical_ratio:.6f}", True, color
    )

    if measured_ratio is None:
        measured_text = font.render("T^2 / a^3: Measuring...", True, color)
        error_text = font.render("Ratio Error: Measuring...", True, color)
    else:
        measured_text = font.render(
            f"T^2 / a^3: {measured_ratio:.6f}", True, color
        )
        error_text = font.render(f"Ratio Error: {ratio_error:.2f} %", True, color)

    screen.blit(heading_text, (650, 440))
    screen.blit(measured_text, (650, 475))
    screen.blit(theoretical_text, (650, 510))
    screen.blit(error_text, (650, 545))


def draw_controls_hint(screen, font, color):
    """Draw a compact reminder of the simulator keyboard controls."""
    controls_text = font.render(
        "SPACE: Pause | R: Reset | T: Trail | H: HUD", True, color
    )
    screen.blit(controls_text, (320, 5))


def draw_engineering_hud(
    screen,
    title_font,
    body_font,
    color,
    altitude,
    distance,
    speed,
    orbit_classification,
    periapsis,
    apoapsis,
    semi_major_axis,
    eccentricity,
    theoretical_period,
    measured_period,
    swept_areas,
    kepler_ratio_error,
    simulation_time,
    paused,
):
    """Draw a compact engineering summary of the current simulation state."""
    panel_color = (8, 14, 28)
    border_color = (70, 110, 160)
    heading_color = (130, 200, 255)

    def draw_panel(x, y, width, height, title, lines):
        pygame.draw.rect(screen, panel_color, (x, y, width, height))
        pygame.draw.rect(screen, border_color, (x, y, width, height), 1)
        screen.blit(title_font.render(title, True, heading_color), (x + 12, y + 8))
        for index, line in enumerate(lines):
            text = body_font.render(line, True, color)
            screen.blit(text, (x + 12, y + 38 + index * 24))

    if measured_period is None:
        period_text = f"Period: Theory {theoretical_period:.2f} s"
    else:
        period_text = f"Period: {measured_period:.2f} s"

    if swept_areas:
        swept_area_variation = max(swept_areas) - min(swept_areas)
        kepler_two_lines = [
            "Kepler II: Swept area variation",
            f"  {swept_area_variation:.2f} km^2",
        ]
    else:
        kepler_two_lines = ["Kepler II: Measuring swept areas..."]

    if kepler_ratio_error is None:
        kepler_three_text = "Kepler III: Measuring ratio error..."
    else:
        kepler_three_text = f"Kepler III: Ratio error {kepler_ratio_error:.2f} %"

    draw_panel(
        18,
        18,
        320,
        145,
        "ORBIT",
        [
            f"Altitude: {altitude:.2f} km",
            f"Distance: {distance:.2f} km",
            f"Speed: {speed:.3f} km/s",
            f"Classification: {orbit_classification}",
        ],
    )
    draw_panel(
        18,
        178,
        320,
        170,
        "ORBITAL MECHANICS",
        [
            f"Periapsis: {periapsis:.2f} km",
            f"Apoapsis: {apoapsis:.2f} km",
            f"Semi-major Axis: {semi_major_axis:.2f} km",
            f"Eccentricity: {eccentricity:.3f}",
            period_text,
        ],
    )
    draw_panel(
        18,
        363,
        320,
        145,
        "VALIDATION",
        [
            "Kepler I: Earth at one focus",
            *kepler_two_lines,
            kepler_three_text,
        ],
    )

    status_color = (255, 120, 120) if paused else heading_color
    status_text = "PAUSED" if paused else "RUNNING"
    screen.blit(
        title_font.render(status_text, True, status_color),
        (830, 18),
    )
    simulation_text = body_font.render(
        f"Simulation Time: {simulation_time:.2f} s", True, color
    )
    controls_text = body_font.render(
        "SPACE: Pause | R: Reset | T: Trail | H: HUD", True, color
    )
    screen.blit(simulation_text, (18, 650))
    screen.blit(controls_text, (420, 650))
