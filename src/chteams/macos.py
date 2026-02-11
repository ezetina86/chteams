import subprocess
import logging

logger = logging.getLogger(__name__)


class MacOSController:
    """Handles macOS specific system commands."""

    def __init__(self):
        self._caffeinate_proc = None

    def start_caffeinate(self) -> bool:
        """Prevents system sleep/idle using caffeinate."""
        try:
            self._caffeinate_proc = subprocess.Popen(["caffeinate", "-di"])
            logger.info("System 'caffeinate' activated.")
            return True
        except FileNotFoundError:
            logger.warning("'caffeinate' not found on this system.")
            return False

    def stop_caffeinate(self):
        """Allows system to sleep/idle again."""
        if self._caffeinate_proc:
            self._caffeinate_proc.terminate()
            logger.info("System 'caffeinate' deactivated.")

    def focus_teams_and_interact(self):
        """Uses AppleScript to focus Teams and simulate a keystroke."""
        script = """
        tell application "Microsoft Teams"
            activate
        end tell
        delay 1
        tell application "System Events"
            keystroke "1" using {command down}
        end tell
        """
        try:
            subprocess.run(["osascript", "-e", script], capture_output=True, check=True)
            logger.debug("Teams interaction successful.")
        except subprocess.CalledProcessError as e:
            logger.error(f"AppleScript failed: {e.stderr.decode().strip()}")
