# Orbital Simulator

A small Python/Pygame project that displays Earth in space with a satellite nearby.

## Requirements

- Python 3.10 or newer
- `pygame`

## Setup

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install the dependency:

   ```powershell
   py -m pip install pygame
   ```

   If `py` is not available on your system, use:

   ```powershell
   python -m pip install pygame
   ```

## Run the project

From the project root, run:

```powershell
py src\main.py
```

Or, if needed:

```powershell
python src\main.py
```

A 1000 x 700 window titled **Operation Aerospace 2026** should open. It shows a blue Earth on a dark space background and a satellite with solar panels. Close the window to exit the program.

## Project structure

```text
Orbital-Simulator/
├── src/
│   └── main.py      # Main Pygame application
├── assets/          # Project assets (currently not required to run the app)
└── README.md
```
