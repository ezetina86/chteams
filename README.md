# Teams Active Script

A robust macOS utility to prevent Microsoft Teams from automatically switching your status to "Away".

## Features

- **AppleScript Integration**: Periodically focuses Microsoft Teams and simulates safe activity (switching to the Activity tab).
- **System Notifications**: Sends macOS notifications on interaction failures or if the script needs to shut down.
- **Auto-Shutdown**: Automatically stops the engine after 3 consecutive failures to prevent infinite error loops.
- **Caffeinate**: Uses the native macOS `caffeinate` tool to prevent system-wide idle and sleep modes.
- **Beautiful Dashboard**: Real-time visual feedback using the `rich` library, including uptime and last action timestamp.
- **Debug Mode**: Dedicated `--debug` flag for detailed execution logs and troubleshooting.
- **Pause/Resume**: Toggle activity simulation on the fly by pressing the **'P'** key.
- **Session Summary**: Get a detailed report of your total uptime and interactions when you finish.
- **Python-powered**: Simple, transparent script running in a modular package structure.

## Prerequisites

- macOS
- Microsoft Teams
- Python 3.14+
- `uv` (recommended for package management)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. Run the script:
   ```bash
   .venv/bin/python keep_active.py
   ```

   To enable debug logging:
   ```bash
   .venv/bin/python keep_active.py --debug
   ```

## Controls

- **Ctrl+P**: Toggle Pause/Resume. (Only works when Terminal/iTerm/Code is focused).
- **Ctrl+C**: Stop the script and show the session summary.

## Development

The project follows modern Python best practices and is fully modular.

### Running Tests
```bash
uv pip install pytest pytest-cov
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest --cov=chteams
```

### Code Quality
The project uses `ruff` for linting and formatting:
```bash
uv pip install ruff
ruff check .
ruff format .
```