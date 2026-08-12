"""Pygame setup, controls, drawing, and the main application loop."""

import pygame

from assets import load_sprite
from constants import (
    EARTH_RADIUS,
    FPS,
    HEIGHT,
    KM_PER_PIXEL,
    SPACE,
    WHITE,
    WIDTH,
)
from renderer import (
    draw_engineering_hud,
    draw_labels,
    draw_motion_vectors,
    draw_orbit_trail,
    draw_stars,
)
from simulation_state import SimulationState
from stars import STAR_FIELD


class OrbitalSimulator:
    """Connect user input, simulation updates, and rendering."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Operation Aerospace 2026")
        self.clock = pygame.time.Clock()

        self.label_font = pygame.font.SysFont(None, 28)
        self.hud_title_font = pygame.font.SysFont(None, 20)
        self.hud_body_font = pygame.font.SysFont(None, 18)
        self.earth_label = self.label_font.render("Earth", True, WHITE)
        self.satellite_label = self.label_font.render("Satellite", True, WHITE)

        # Images are loaded once during setup, not during every frame.
        self.earth_image = load_sprite(
            "earth.png",
            (EARTH_RADIUS * 2, EARTH_RADIUS * 2),
        )
        self.satellite_image = load_sprite("satellite.png", (56, 40))

        self.earth_screen_x = WIDTH // 2
        self.earth_screen_y = HEIGHT // 2
        self.state = SimulationState()

        self.running = True
        self.paused = False
        self.show_trail = True
        self.show_hud = True

    def run(self):
        """Run the simulator until the window is closed."""
        try:
            while self.running:
                self._handle_events()
                if not self.running:
                    break

                self.state.calculate_measurements()
                self._draw_frame()
                pygame.display.flip()

                dt = self.clock.tick(FPS) / 1000
                if not self.paused:
                    self.state.update(dt)
        finally:
            pygame.quit()

    def _handle_events(self):
        """Respond to window and keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.state.reset()
                    self.paused = False
                elif event.key == pygame.K_t:
                    self.show_trail = not self.show_trail
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud

    def _draw_frame(self):
        """Draw one complete frame using the current simulation state."""
        self.screen.fill(SPACE)
        draw_stars(self.screen, STAR_FIELD)

        if self.show_trail:
            draw_orbit_trail(
                self.screen,
                self.earth_screen_x,
                self.earth_screen_y,
                self.state.orbit_trail,
                KM_PER_PIXEL,
            )

        self._draw_earth_and_satellite()
        self._draw_vectors_and_labels()

        if self.show_hud:
            self._draw_hud()

    def _draw_earth_and_satellite(self):
        """Draw the two image sprites at their current screen positions."""
        earth_rectangle = self.earth_image.get_rect(
            center=(self.earth_screen_x, self.earth_screen_y)
        )
        self.screen.blit(self.earth_image, earth_rectangle)

        satellite_screen_x = (
            self.earth_screen_x + self.state.satellite_x_km / KM_PER_PIXEL
        )
        satellite_screen_y = (
            self.earth_screen_y + self.state.satellite_y_km / KM_PER_PIXEL
        )
        satellite_rectangle = self.satellite_image.get_rect(
            center=(int(satellite_screen_x), int(satellite_screen_y))
        )
        self.screen.blit(self.satellite_image, satellite_rectangle)

    def _draw_vectors_and_labels(self):
        """Draw motion arrows and names for Earth and the satellite."""
        draw_motion_vectors(
            self.screen,
            self.earth_screen_x,
            self.earth_screen_y,
            self.state.satellite_x_km,
            self.state.satellite_y_km,
            KM_PER_PIXEL,
            self.state.satellite_velocity_x_km_s,
            self.state.satellite_velocity_y_km_s,
            self.state.acceleration_x_km_s2,
            self.state.acceleration_y_km_s2,
            self.hud_body_font,
        )
        draw_labels(
            self.screen,
            self.earth_label,
            self.satellite_label,
            self.earth_screen_x,
            self.earth_screen_y,
            EARTH_RADIUS,
            self.state.satellite_x_km,
            self.state.satellite_y_km,
            KM_PER_PIXEL,
            self.satellite_image.get_height() // 2,
        )

    def _draw_hud(self):
        """Draw the current orbital measurements and control status."""
        draw_engineering_hud(
            self.screen,
            self.hud_title_font,
            self.hud_body_font,
            WHITE,
            self.state.altitude,
            self.state.distance,
            self.state.current_speed,
            self.state.orbit_classification,
            self.state.periapsis,
            self.state.apoapsis,
            self.state.semi_major_axis,
            self.state.eccentricity,
            self.state.initial_orbital_period,
            self.state.measured_orbital_period,
            self.state.swept_areas,
            self.state.kepler_ratio_error,
            self.state.simulation_time,
            self.paused,
        )
