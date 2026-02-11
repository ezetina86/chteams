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

## Development

The project has been refactored into a modular package structure in `src/chteams`.

### Running Tests
```bash
uv pip install pytest
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest
```

### New Features
- **Logging**: Better visibility into what the script is doing.
- **Unit Tested**: Core logic is verified with mocks.
- **Modular**: Easier to extend or port to other OSes.

