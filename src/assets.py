"""Helpers for loading the simulator's image files."""

from pathlib import Path

import pygame


ASSETS_FOLDER = Path(__file__).resolve().parent.parent / "assets"


def load_sprite(file_name, maximum_size):
    """Load a transparent image, trim its padding, and resize it proportionally."""
    image = pygame.image.load(ASSETS_FOLDER / file_name).convert_alpha()

    # The PNG files have transparent padding around the visible object.
    visible_area = image.get_bounding_rect(min_alpha=1)
    image = image.subsurface(visible_area).copy()

    max_width, max_height = maximum_size
    scale = min(max_width / image.get_width(), max_height / image.get_height())
    new_size = (
        max(1, round(image.get_width() * scale)),
        max(1, round(image.get_height() * scale)),
    )

    return pygame.transform.smoothscale(image, new_size)
