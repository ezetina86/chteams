# Teams Active Script

A robust macOS utility to prevent Microsoft Teams from automatically switching your status to "Away".

## Features

- **AppleScript Integration**: Periodically focuses Microsoft Teams and simulates safe activity (switching to the Activity tab).
- **Caffeinate**: Uses the native macOS `caffeinate` tool to prevent system-wide idle and sleep modes.
- **Python-powered**: Simple, transparent script running in a virtual environment.

## Prerequisites

- macOS
- Microsoft Teams
- Python 3.14+
- `uv` (for package management)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install pyautogui
   ```

2. Run the script:
   ```bash
   .venv/bin/python keep_active.py
   ```

## Usage Notes

- The first time you run this, macOS will ask for permission to control Microsoft Teams and System Events. Please grant these in **System Settings > Privacy & Security > Accessibility**.
- The script switches to the Teams window every 4 minutes, simulates a keypress, and then returns control.
