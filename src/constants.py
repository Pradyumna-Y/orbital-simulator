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

# -----------------------------
# Earth Physics Units
# -----------------------------
# Earth's standard gravitational parameter in km^3/s^2.
EARTH_MU = 398600.4418
EARTH_RADIUS_KM = 6371.0
INITIAL_ORBIT_RADIUS_KM = 7000.0

# Rendering scale only; physics calculations continue to use kilometers.
KM_PER_PIXEL = 50.0

# Scales circular speed so gravity can create an elliptical orbit naturally.
ORBIT_VELOCITY_SCALE = 0.9

# Enable this mode to initialize the satellite at the calculated escape speed.
ESCAPE_TEST_MODE = True
ESCAPE_TEST_SCALE = 1.05

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
# Earth is drawn to the same scale as kilometer-based positions.
EARTH_RADIUS = int(EARTH_RADIUS_KM / KM_PER_PIXEL)
# Satellite is a visible marker, not a scale model of its physical size.
SATELLITE_RADIUS = 6

# -----------------------------
# Star Field
# -----------------------------
NUMBER_OF_STARS = 200

# -----------------------------
# Orbit Trail
# -----------------------------
MAX_TRAIL_POINTS = 5000
TRAIL_COLOR = (180, 180, 200)
