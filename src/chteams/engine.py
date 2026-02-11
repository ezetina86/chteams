import time
import logging
from datetime import datetime, timedelta
from rich.live import Live
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
        self.start_time = None
        self.last_action_time = "Never"

    def _get_uptime(self) -> str:
        """Calculates and formats the uptime.

        Returns:
            str: Formatted uptime string (HH:MM:SS).
        """
        if not self.start_time:
            return "00:00:00"
        delta = datetime.now() - self.start_time
        return str(timedelta(seconds=int(delta.total_seconds())))

    def run(self):
        """Starts the infinite activity loop.

        Activates system-level sleep prevention and periodically executes
        interaction commands until stopped.
        """
        self.is_running = True
        self.start_time = datetime.now()
        self.controller.start_caffeinate()

        logger.info(f"Engine started. Interval: {self.interval}s")

        with Live(
            create_dashboard("Starting...", "00:00:00", "Never", self.interval),
            refresh_per_second=1,
        ) as live:
            try:
                while self.is_running:
                    live.update(
                        create_dashboard(
                            "Simulating Activity",
                            self._get_uptime(),
                            self.last_action_time,
                            self.interval,
                        )
                    )
                    self.controller.focus_teams_and_interact()
                    self.last_action_time = datetime.now().strftime("%H:%M:%S")

                    # Sleep in small increments to allow for faster interruption
                    # and UI updates
                    for _ in range(self.interval):
                        if not self.is_running:
                            break
                        live.update(
                            create_dashboard(
                                "Waiting",
                                self._get_uptime(),
                                self.last_action_time,
                                self.interval,
                            )
                        )
                        time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
            finally:
                self.controller.stop_caffeinate()

    def stop(self):
        """Stops the activity loop gracefully."""
        self.is_running = False
        logger.info("Stopping engine...")
