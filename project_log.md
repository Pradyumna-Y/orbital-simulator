# Day 1

## Goal
Prepare my Orbital Simulator development environment.

## Completed
- Installed Python 3.13
- Installed Pygame
- Installed NumPy
- Installed Matplotlib
- Created project structure
- Ran my first Pygame window

## What I Learned
- Python version compatibility matters.
- Pygame uses a game loop to keep the window open.

## Next Goal
Draw Earth in the center of the screen.

## Phase 2.1 – Object Position Variables

### What I Built
- Replaced hardcoded coordinates with variables for Earth and the satellite.
- Added named constants for radii and orbital distance.
- Configured VS Code to use the correct Python interpreter.

### What I Learned
- Objects in a simulation should have properties instead of hardcoded values.
- Position variables allow an object's location to change over time.
- Constants make code easier to understand and maintain.
- Python interpreter selection in VS Code affects package detection and execution.

### Engineering Reflection
This update did not visibly change the simulator, but it greatly improved its structure. The satellite now has a defined position, which will allow future lessons to introduce velocity, acceleration, and gravity without rewriting the drawing code.

## Phase 2.4 – Labels & HUD Foundation

### What I Built
- Added text labels for Earth and the satellite using Pygame's font rendering system.
- Positioned labels below their corresponding objects.
- Preserved the existing rendering pipeline and project structure.

### What I Learned
- Pygame renders text using Font objects and text surfaces.
- Rendering text follows the same draw-update cycle as graphical objects.
- Labels are the first step toward building a telemetry interface for the simulator.

### Engineering Reflection
Although the labels are simple, they establish the foundation for a future heads-up display (HUD). This system will later display engineering data such as velocity, altitude, orbital period, simulation time, and frame rate, similar to professional aerospace visualization software.