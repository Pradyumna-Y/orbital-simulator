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