"""The changing position, velocity, and measurements of the orbit."""

import math

from constants import (
    EARTH_MU,
    EARTH_RADIUS_KM,
    ESCAPE_TEST_MODE,
    ESCAPE_TEST_SCALE,
    INITIAL_ORBIT_RADIUS_KM,
    KEPLER_AREA_INTERVAL,
    MAX_SWEPT_AREA_SAMPLES,
    MAX_TRAIL_POINTS,
    ORBIT_VELOCITY_SCALE,
)
from simulation import (
    calculate_direction,
    calculate_distance,
    calculate_eccentricity,
    calculate_escape_velocity,
    calculate_gravity,
    calculate_kepler_third_law_ratio,
    calculate_orbital_period,
    calculate_orbital_velocity,
    calculate_semi_major_axis,
    calculate_specific_orbital_energy,
    calculate_speed,
    calculate_swept_area,
    calculate_theoretical_kepler_ratio,
    classify_orbit,
    update_satellite,
)


class SimulationState:
    """Own the simulation values and update them one frame at a time."""

    def __init__(self):
        # Earth is the physics origin. Satellite positions are relative to it.
        self.earth_x_km = 0.0
        self.earth_y_km = 0.0
        self.reset()

    def reset(self):
        """Restore the orbit and all measurements to their starting values."""
        self.satellite_x_km = INITIAL_ORBIT_RADIUS_KM
        self.satellite_y_km = 0.0

        self.initial_distance = calculate_distance(
            self.earth_x_km,
            self.earth_y_km,
            self.satellite_x_km,
            self.satellite_y_km,
        )
        circular_speed = calculate_orbital_velocity(self.initial_distance)

        if ESCAPE_TEST_MODE:
            escape_speed = calculate_escape_velocity(EARTH_MU, self.initial_distance)
            initial_speed = escape_speed * ESCAPE_TEST_SCALE
        else:
            initial_speed = circular_speed * ORBIT_VELOCITY_SCALE

        self.initial_orbital_period = calculate_orbital_period(
            self.initial_distance,
            circular_speed,
        )

        # The starting velocity is perpendicular to the Earth-satellite radius.
        self.satellite_velocity_x_km_s = 0.0
        self.satellite_velocity_y_km_s = -initial_speed

        self.minimum_distance = self.initial_distance
        self.maximum_distance = self.initial_distance
        self.orbit_trail = []
        self.swept_areas = []
        self.simulation_time = 0.0
        self.measured_orbital_period = None

        self.previous_angle = math.atan2(
            self.satellite_y_km - self.earth_y_km,
            self.satellite_x_km - self.earth_x_km,
        )
        self.accumulated_angle = 0.0
        self.kepler_interval_time = 0.0
        self.previous_sample_x_km = self.satellite_x_km
        self.previous_sample_y_km = self.satellite_y_km

        # Populate the values that the first rendered frame needs.
        self.calculate_measurements()

    def calculate_measurements(self):
        """Calculate the current orbital values shown in the HUD and vectors."""
        self.distance = calculate_distance(
            self.earth_x_km,
            self.earth_y_km,
            self.satellite_x_km,
            self.satellite_y_km,
        )
        self.altitude = self.distance - EARTH_RADIUS_KM

        self.minimum_distance = min(self.minimum_distance, self.distance)
        self.maximum_distance = max(self.maximum_distance, self.distance)
        self.periapsis = self.minimum_distance
        self.apoapsis = self.maximum_distance
        self.semi_major_axis = calculate_semi_major_axis(
            self.periapsis,
            self.apoapsis,
        )
        self.eccentricity = calculate_eccentricity(
            self.periapsis,
            self.apoapsis,
        )

        self.current_speed = calculate_speed(
            self.satellite_velocity_x_km_s,
            self.satellite_velocity_y_km_s,
        )
        specific_energy = calculate_specific_orbital_energy(
            self.current_speed,
            EARTH_MU,
            self.distance,
        )
        self.orbit_classification = classify_orbit(specific_energy)

        direction_x, direction_y = calculate_direction(
            self.earth_x_km,
            self.earth_y_km,
            self.satellite_x_km,
            self.satellite_y_km,
        )
        gravity = calculate_gravity(self.distance)
        self.acceleration_x_km_s2 = -gravity * direction_x
        self.acceleration_y_km_s2 = -gravity * direction_y

        if self.measured_orbital_period is None:
            self.kepler_ratio_error = None
        else:
            measured_ratio = calculate_kepler_third_law_ratio(
                self.measured_orbital_period,
                self.semi_major_axis,
            )
            theoretical_ratio = calculate_theoretical_kepler_ratio()
            self.kepler_ratio_error = (
                abs(measured_ratio - theoretical_ratio)
                / theoretical_ratio
                * 100
            )

    def update(self, dt):
        """Advance the satellite and orbital measurements by one time step."""
        (
            self.satellite_x_km,
            self.satellite_y_km,
            self.satellite_velocity_x_km_s,
            self.satellite_velocity_y_km_s,
        ) = update_satellite(
            self.satellite_x_km,
            self.satellite_y_km,
            self.satellite_velocity_x_km_s,
            self.satellite_velocity_y_km_s,
            self.acceleration_x_km_s2,
            self.acceleration_y_km_s2,
            dt,
        )

        self.simulation_time += dt
        self._measure_swept_area(dt)
        self._measure_orbital_period()

        self.orbit_trail.append((self.satellite_x_km, self.satellite_y_km))
        if len(self.orbit_trail) > MAX_TRAIL_POINTS:
            self.orbit_trail.pop(0)

    def _measure_swept_area(self, dt):
        """Record areas swept during equal simulation-time intervals."""
        self.kepler_interval_time += dt
        if self.kepler_interval_time < KEPLER_AREA_INTERVAL:
            return

        swept_area = calculate_swept_area(
            self.earth_x_km,
            self.earth_y_km,
            self.previous_sample_x_km,
            self.previous_sample_y_km,
            self.satellite_x_km,
            self.satellite_y_km,
        )
        self.swept_areas.append(swept_area)
        if len(self.swept_areas) > MAX_SWEPT_AREA_SAMPLES:
            self.swept_areas.pop(0)

        self.previous_sample_x_km = self.satellite_x_km
        self.previous_sample_y_km = self.satellite_y_km
        self.kepler_interval_time -= KEPLER_AREA_INTERVAL

    def _measure_orbital_period(self):
        """Record the simulation time after the first complete revolution."""
        current_angle = math.atan2(
            self.satellite_y_km - self.earth_y_km,
            self.satellite_x_km - self.earth_x_km,
        )
        angle_change = current_angle - self.previous_angle

        # Correct the angle jump when crossing from +pi to -pi or vice versa.
        if angle_change > math.pi:
            angle_change -= 2 * math.pi
        elif angle_change < -math.pi:
            angle_change += 2 * math.pi

        self.accumulated_angle += abs(angle_change)
        self.previous_angle = current_angle

        if (
            self.measured_orbital_period is None
            and self.accumulated_angle >= 2 * math.pi
        ):
            self.measured_orbital_period = self.simulation_time
