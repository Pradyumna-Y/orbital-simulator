# -----------------------------
# Window Settings
# -----------------------------
WIDTH = 1000
HEIGHT = 700

# -----------------------------
# Simulation Timing
# -----------------------------
FPS = 60

# Scaled simulation constant used for the simplified gravity model.
GRAVITY_STRENGTH = 100000

# Scales circular speed so gravity can create an elliptical orbit naturally.
ORBIT_VELOCITY_SCALE = 0.9

# Enable this mode to initialize the satellite at the calculated escape speed.
ESCAPE_TEST_MODE = False
ESCAPE_TEST_SCALE = 1.0

# Simulation seconds between Kepler's Second Law area measurements.
KEPLER_AREA_INTERVAL = 2.0
MAX_SWEPT_AREA_SAMPLES = 10

# -----------------------------
# Colors
# -----------------------------
SPACE = (15, 15, 30)
WHITE = (255, 255, 255)
EARTH_BLUE = (50, 120, 255)
SATELLITE_RED = (255, 0, 0)

# -----------------------------
# Object Sizes
# -----------------------------
EARTH_RADIUS = 60
SATELLITE_RADIUS = 30
SATELLITE_DISTANCE = 150

# -----------------------------
# Star Field
# -----------------------------
NUMBER_OF_STARS = 200

# -----------------------------
# Orbit Trail
# -----------------------------
MAX_TRAIL_POINTS = 5000
TRAIL_COLOR = (180, 180, 200)
