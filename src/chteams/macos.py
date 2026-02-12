import subprocess
import logging

logger = logging.getLogger(__name__)


class MacOSController:
    """Handles macOS specific system commands for preventing sleep and simulating activity.

    This controller manages the 'caffeinate' process and executes AppleScripts to
    interact with Microsoft Teams.
    """

    def __init__(self):
        """Initializes the MacOSController with no active caffeinate process."""
        self._caffeinate_proc = None

    def start_caffeinate(self) -> bool:
        """Prevents system sleep and idle by starting the caffeinate utility.

        Returns:
            bool: True if caffeinate was successfully started, False otherwise.
        """
        try:
            self._caffeinate_proc = subprocess.Popen(["caffeinate", "-di"])
            logger.info("System 'caffeinate' activated.")
            return True
        except FileNotFoundError:
            logger.warning("'caffeinate' not found on this system.")
            return False

    def stop_caffeinate(self):
        """Terminates the active caffeinate process, allowing the system to sleep."""
        if self._caffeinate_proc:
            self._caffeinate_proc.terminate()
            logger.info("System 'caffeinate' deactivated.")

    def focus_teams_and_interact(self):
        """Brings Microsoft Teams to focus and simulates a Command+1 keystroke.

        Uses AppleScript to ensure Teams is the active application and triggers
        the 'Activity' tab shortcut to signal user presence.

        Raises:
            RuntimeError: If the AppleScript execution fails.
        """
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
            error_msg = e.stderr.decode().strip()
            logger.error(f"AppleScript failed: {error_msg}")
            raise RuntimeError(f"Failed to interact with Teams: {error_msg}")

    def notify(self, title: str, message: str):
        """Displays a macOS system notification.

        Args:
            title: The title of the notification.
            message: The body content of the notification.
        """
        script = f'display notification "{message}" with title "{title}"'
        try:
            subprocess.run(["osascript", "-e", script], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send notification: {e}")

    def get_frontmost_app(self) -> str:
        """Returns the name of the currently active (frontmost) application.

        Returns:
            str: The name of the frontmost application, or empty string if failed.
        """
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        try:
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""
