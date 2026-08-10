# Operation Aerospace 2026

## Overview

Operation Aerospace 2026 is a Python/Pygame orbital mechanics simulator built to explore how mathematics and Newtonian gravity predict orbital motion. It uses Earth-centered, kilometer-based physics while scaling positions to a Pygame window for visualization.

The project is an educational simulation, not a production flight-dynamics tool. Its goal is to make core orbital mechanics concepts visible, measurable, and testable in code.

## Motivation

I built this project to connect an interest in orbital mechanics with the mathematics behind Kepler's Laws and gravitational motion. The simulator provides a way to see how initial velocity, distance, and inverse-square gravity combine to produce circular, elliptical, and escape trajectories.

## Features

- Inverse-square gravitational acceleration
- Earth's real standard gravitational parameter
- Kilometer and second-based physics units
- Circular-orbit velocity calculation
- Elliptical orbits from gravity and initial velocity
- Optional escape-trajectory test mode
- Orbital trail visualization
- Periapsis and apoapsis tracking
- Eccentricity, semi-major axis, and focus-distance calculations
- Theoretical and measured orbital periods
- Specific orbital energy and bound/escape classification
- Kepler's First, Second, and Third Law demonstrations
- Velocity and acceleration vector visualizations
- Pause, reset, trail, and HUD controls

## Physics

The simulator uses Earth's standard gravitational parameter, \(\mu\), rather than a pixel-based gravity constant. For Earth:

\[
\mu = 398600.4418\ \text{km}^3/\text{s}^2
\]

Gravitational acceleration magnitude:

\[
a = \frac{\mu}{r^2}
\]

Circular orbital velocity:

\[
v_c = \sqrt{\frac{\mu}{r}}
\]

Escape velocity:

\[
v_e = \sqrt{\frac{2\mu}{r}}
\]

Specific orbital energy:

\[
\epsilon = \frac{v^2}{2} - \frac{\mu}{r}
\]

Kepler's Third Law relationship:

\[
\frac{T^2}{a^3} = \frac{4\pi^2}{\mu}
\]

Here, \(r\) is distance from Earth's center, \(v\) is speed, \(T\) is orbital period, and \(a\) is the semi-major axis.

## Kepler's Laws

1. **Kepler I — Elliptical orbits:** The simulator calculates periapsis, apoapsis, semi-major axis, eccentricity, and focus distance from the gravity-generated trajectory. Earth remains at the central gravitational focus.
2. **Kepler II — Equal areas in equal times:** The simulator samples triangle areas swept out over equal simulation-time intervals. It also tracks speed, showing that the satellite moves faster near periapsis and slower near apoapsis.
3. **Kepler III — Period relationship:** The simulation compares its measured \(T^2/a^3\) ratio with the theoretical value derived from Earth's \(\mu\).

## Validation Results

Representative results obtained during development include:

- Circular orbital period error of approximately **0.04%**
- Kepler III ratio error of approximately **0.09%**
- Elliptical-orbit eccentricity of approximately **0.19** in one test
- Swept-area measurements that remained close despite using a triangle approximation

Exact results can vary slightly with the timestep, initial settings, and numerical accumulation over time.

## Numerical Method

The simulator uses a semi-implicit, or symplectic Euler, update:

\[
\text{velocity} \leftarrow \text{velocity} + \text{acceleration} \cdot \Delta t
\]

\[
\text{position} \leftarrow \text{position} + \text{velocity} \cdot \Delta t
\]

Velocity is updated first, then the updated velocity is used to update position. Numerical simulations approximate continuous motion with small time steps, so small measurement and energy errors are expected.

## Architecture

The project is divided into small modules to separate application control, physics, and visualization:

- `main.py` — Coordinates the program loop, controls, state, telemetry, and module calls
- `constants.py` — Stores physical constants, rendering scale, colors, and configuration values
- `simulation.py` — Contains orbital calculations, gravity, numerical updates, and Kepler-law measurements
- `renderer.py` — Draws Earth, the satellite, vectors, trails, labels, and the engineering HUD
- `stars.py` — Creates the fixed procedural star field used as the background

Physics positions are stored in kilometers relative to Earth. The renderer converts those values to pixels only when drawing.

## Controls

| Key | Action |
| --- | --- |
| `SPACE` | Pause / Resume |
| `R` | Reset the simulation and analysis measurements |
| `T` | Toggle the orbital trail |
| `H` | Toggle the HUD |

## Installation

Requirements:

- Python 3.10 or newer
- Pygame

Clone or download this repository, open a terminal in the project folder, and install Pygame:

```powershell
py -m pip install pygame
```

If the `py` launcher is unavailable, use:

```powershell
python -m pip install pygame
```

## Running

From the project root, start the simulator with:

```powershell
py src\main.py
```

Or:

```powershell
python src\main.py
```

## What I Learned

- Vectors, direction, and component-based motion
- Inverse-square gravity and gravitational acceleration
- Circular and escape velocity calculations
- Numerical integration and timestep-related error
- Validating a simulation against theoretical orbital relationships
- Modular software design that separates physics, rendering, constants, and program control

## Future Work

- Earth-Moon system
- Multiple satellites
- Improved numerical integrators such as Velocity Verlet
- Adjustable orbital parameters
- More advanced mission visualization
