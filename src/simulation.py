def update_satellite(
    satellite_x,
    satellite_y,
    satellite_velocity_x,
    satellite_velocity_y,
    dt,
):
    """Update the satellite position using velocity and delta time."""
    # Multiplying velocity by delta time keeps movement
    # consistent even if the frame rate changes.
    satellite_x += satellite_velocity_x * dt
    satellite_y += satellite_velocity_y * dt

    return satellite_x, satellite_y
