# Operation Aerospace 2026

Operation Aerospace 2026 is a beginner-friendly orbital mechanics simulator made
with Python and Pygame. It uses kilometer-based physics to show a satellite
orbiting Earth while displaying its motion, orbital measurements, and Kepler's
Laws.

This is an educational simulation rather than a production flight-dynamics
tool.

## Features

- Realistic Earth and satellite image sprites
- Procedurally generated star field with varied brightness and color
- Inverse-square gravitational acceleration
- Earth's standard gravitational parameter in km³/s²
- Circular, elliptical, and optional escape trajectories
- Velocity and acceleration vectors
- Orbital trail visualization
- Periapsis, apoapsis, eccentricity, and semi-major axis measurements
- Theoretical and measured orbital periods
- Bound-or-escape orbit classification
- Kepler's First, Second, and Third Law measurements
- Pause, reset, trail, and HUD controls

## Requirements

You need:

- Python 3.10 or newer
- Pygame 2.5 or newer
- A terminal such as PowerShell, Command Prompt, Terminal, or the VS Code
  terminal

Git is optional. You only need it if you want to clone the repository instead of
downloading it as a ZIP file.

## Download the project

Either clone the repository with Git:

```bash
git clone https://github.com/Pradyumna-Y/orbital-simulator.git
cd orbital-simulator
```

Or download the repository as a ZIP file and extract it.

Afterward, open a terminal in the `Orbital-Simulator` folder. This is the project
root—the folder containing `README.md`, `requirements.txt`, `assets`, and `src`.

## Setup on Windows

Check that Python is installed:

```powershell
py --version
```

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, allow it for the current terminal
session and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install the project dependency:

```powershell
py -m pip install -r requirements.txt
```

Run the simulator:

```powershell
py src\main.py
```

If the `py` launcher is unavailable, replace `py` with `python` in each command.

## Setup on macOS or Linux

Check that Python is installed:

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependency:

```bash
python3 -m pip install -r requirements.txt
```

Run the simulator:

```bash
python3 src/main.py
```

## Quick setup without a virtual environment

A virtual environment is recommended because it keeps project packages separate,
but the simulator can also be run with:

```powershell
python -m pip install -r requirements.txt
python src\main.py
```

On macOS or Linux, use `python3` and `src/main.py` instead.

## Controls

| Key | Action |
| --- | --- |
| `SPACE` | Pause or resume the simulation |
| `R` | Reset the orbit and all measurements |
| `T` | Show or hide the orbital trail |
| `H` | Show or hide the engineering HUD |
| Window close button | Exit the simulator |

## Project structure

```text
Orbital-Simulator/
├── assets/
│   ├── earth.png            # Transparent Earth sprite
│   └── satellite.png        # Transparent satellite sprite
├── src/
│   ├── main.py              # Small program entry point
│   ├── application.py       # Pygame setup, controls, drawing, and main loop
│   ├── assets.py            # Image loading and proportional resizing
│   ├── simulation_state.py  # Changing orbit state and measurements
│   ├── simulation.py        # Reusable physics calculations
│   ├── renderer.py          # Drawing functions and engineering HUD
│   ├── constants.py         # Physics and display configuration
│   └── stars.py             # Procedural star-field generation
├── requirements.txt         # Python package requirements
└── README.md
```

The program starts in `main.py`. That file creates an `OrbitalSimulator` from
`application.py`. The application handles input and drawing, while
`SimulationState` stores and updates the orbit. The formulas themselves remain
in `simulation.py`, making each module responsible for one main job.

## Changing simulation settings

Beginner-friendly settings are stored in `src/constants.py`. Stop the simulator,
change a value, save the file, and start the program again.

Useful settings include:

- `FPS` — target frames per second
- `INITIAL_ORBIT_RADIUS_KM` — starting distance from Earth's center
- `KM_PER_PIXEL` — visual zoom level
- `ORBIT_VELOCITY_SCALE` — starting speed relative to circular-orbit speed
- `ESCAPE_TEST_MODE` — change to `True` to test an escape trajectory
- `NUMBER_OF_STARS` — number of background stars

Physics positions use kilometers. `KM_PER_PIXEL` changes only how those positions
are displayed on screen.

## Physics used

Earth's standard gravitational parameter is:

$$
\mu = 398600.4418\ \text{km}^3/\text{s}^2
$$

Gravitational acceleration:

$$
a = \frac{\mu}{r^2}
$$

Circular orbital velocity:

$$
v_c = \sqrt{\frac{\mu}{r}}
$$

Escape velocity:

$$
v_e = \sqrt{\frac{2\mu}{r}}
$$

Specific orbital energy:

$$
\epsilon = \frac{v^2}{2} - \frac{\mu}{r}
$$

The simulator uses semi-implicit Euler integration. It updates velocity first and
then uses the new velocity to update position. Small numerical errors are normal
because the program approximates continuous motion with individual time steps.

## Troubleshooting

### `No module named pygame`

Install the requirements using the same Python command used to start the project:

```powershell
python -m pip install -r requirements.txt
python src\main.py
```

### `python` or `py` is not recognized

Install Python 3 from the official Python website, then close and reopen the
terminal. On Windows, make sure the installer option to add Python to `PATH` is
enabled.

### PowerShell will not activate `.venv`

Run this once in the current PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### An image cannot be loaded

Make sure `assets/earth.png` and `assets/satellite.png` are still inside the
project. Keep the project folders together rather than copying only `main.py`.

### The window opens and immediately closes

Run the project from a terminal instead of double-clicking `main.py`. The terminal
will remain visible and show the error message that needs to be fixed.

## Exiting the virtual environment

When you finish working with the project, enter:

```text
deactivate
```

## Possible future improvements

- Earth-Moon system
- Multiple satellites
- Adjustable orbital parameters in the window
- Velocity Verlet or another higher-accuracy numerical integrator
- Additional mission-planning visualizations
