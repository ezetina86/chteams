import time
import logging
from datetime import datetime, timedelta
from rich.live import Live
from pynput import keyboard
from .macos import MacOSController
from .ui import create_dashboard

logger = logging.getLogger(__name__)


class ActivityEngine:
    """Orchestrates the simulation loop to maintain active status.

    Attributes:
        controller (MacOSController): The platform-specific controller for actions.
        interval (int): Seconds between each activity simulation.
        is_running (bool): Flag indicating if the engine is currently active.
    """

    def __init__(self, controller: MacOSController, interval: int = 240):
        """Initializes the engine with a controller and simulation interval.

        Args:
            controller (MacOSController): The controller to execute system commands.
            interval (int): Seconds to wait between interactions. Defaults to 240.
        """
        self.controller = controller
        self.interval = interval
        self.is_running = False
        self.paused = False
        self.start_time = None
        self.last_action_time = "Never"
        self.activity_count = 0
        self._listener = None

    def _on_press(self, key):
        """Callback for keyboard events to toggle pause."""
        try:
            if hasattr(key, "char") and key.char == "p":
                self.paused = not self.paused
                logger.info(f"Engine {'paused' if self.paused else 'resumed'}")
        except AttributeError:
            pass

    def _get_uptime(self) -> str:
        """Calculates and formats the uptime.

        Returns:
            str: Formatted uptime string (HH:MM:SS).
        """
        if not self.start_time:
            return "00:00:00"
        delta = datetime.now() - self.start_time
        return str(timedelta(seconds=int(delta.total_seconds())))

    def run(self) -> tuple[str, int]:
        """Starts the infinite activity loop.

        Activates system-level sleep prevention and periodically executes
        interaction commands until stopped.

        Returns:
            tuple[str, int]: A tuple containing (total_uptime_string, activity_count).
        """
        self.is_running = True
        self.start_time = datetime.now()
        self.controller.start_caffeinate()
        consecutive_failures = 0
        max_failures = 3

        # Start keyboard listener
        self._listener = keyboard.Listener(on_press=self._on_press)
        self._listener.start()

        logger.info(f"Engine started. Interval: {self.interval}s")

        with Live(
            create_dashboard("Starting...", "00:00:00", "Never", "N/A", self.interval),
            refresh_per_second=1,
        ) as live:
            try:
                while self.is_running:
                    if self.paused:
                        current_status = "PAUSED"
                    else:
                        current_status = "Simulating Activity"
                        try:
                            self.controller.focus_teams_and_interact()
                            self.activity_count += 1
                            self.last_action_time = datetime.now().strftime("%H:%M:%S")
                            consecutive_failures = 0
                        except RuntimeError as e:
                            consecutive_failures += 1
                            logger.error(f"Activity simulation failed ({consecutive_failures}/{max_failures}): {e}")
                            self.controller.notify("CHTEAMS Error", f"Failed to interact with Teams ({consecutive_failures}/{max_failures})")
                            
                            if consecutive_failures >= max_failures:
                                logger.critical("Too many consecutive failures. Shutting down.")
                                self.controller.notify("CHTEAMS Shutting Down", "Stopping engine due to persistent errors.")
                                self.is_running = False
                                current_status = "ERROR - SHUTTING DOWN"

                    if not self.is_running:
                        # Final update before exit
                        live.update(
                            create_dashboard(
                                current_status,
                                self._get_uptime(),
                                self.last_action_time,
                                "Stopped",
                                self.interval,
                            )
                        )
                        break

                    # Sleep in small increments to allow for faster interruption
                    # and UI updates
                    for remaining in range(self.interval, 0, -1):
                        if not self.is_running:
                            break
                        
                        status_msg = "PAUSED" if self.paused else "Waiting"
                        next_act_str = f"{remaining}s" if not self.paused else "Paused"
                        live.update(
                            create_dashboard(
                                status_msg,
                                self._get_uptime(),
                                self.last_action_time,
                                next_act_str,
                                self.interval,
                            )
                        )
                        time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
            finally:
                self.controller.stop_caffeinate()
                if self._listener:
                    self._listener.stop()

        return self._get_uptime(), self.activity_count

    def stop(self):
        """Stops the activity loop gracefully."""
        self.is_running = False
        logger.info("Stopping engine...")
    def stop(self):
        """Stops the activity loop gracefully."""
        self.is_running = False
        logger.info("Stopping engine...")
