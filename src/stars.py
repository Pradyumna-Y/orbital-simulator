import random
from constants import HEIGHT, NUMBER_OF_STARS, WIDTH


def create_star_field():
    """Create stars with varied brightness, color, and apparent size."""
    random_generator = random.Random(2026)
    stars = []

    for _ in range(NUMBER_OF_STARS):
        x = random_generator.randrange(WIDTH)
        y = random_generator.randrange(HEIGHT)

        # Squaring the random value makes dim stars much more common than
        # bright ones, which looks closer to a real night sky.
        brightness = int(90 + 165 * random_generator.random() ** 2)
        color_type = random_generator.random()

        if color_type < 0.70:
            color = (brightness, brightness, brightness)
        elif color_type < 0.87:
            # A small number of stars appear slightly blue or warm.
            color = (int(brightness * 0.82), int(brightness * 0.90), brightness)
        else:
            color = (brightness, int(brightness * 0.88), int(brightness * 0.72))

        radius = 2 if brightness > 220 else 1
        has_glow = brightness > 235
        stars.append((x, y, radius, color, has_glow))

    return stars


# The seed above keeps the same natural-looking star field between runs.
STAR_FIELD = create_star_field()
