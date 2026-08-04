import random
from constants import HEIGHT, NUMBER_OF_STARS, WIDTH

# Generated once when this module is imported; the positions stay fixed per run.
STAR_COORDINATES = [
    (random.randrange(WIDTH), random.randrange(HEIGHT))
    for _ in range(NUMBER_OF_STARS)
]
