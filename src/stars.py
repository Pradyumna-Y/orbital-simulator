import random


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
NUMBER_OF_STARS = 200

# Generated once when this module is imported; the positions stay fixed per run.
STAR_COORDINATES = [
    (random.randrange(WINDOW_WIDTH), random.randrange(WINDOW_HEIGHT))
    for _ in range(NUMBER_OF_STARS)
]
