import time
import logging
from .macos import MacOSController

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

    def run(self):
        """Starts the infinite activity loop.

        Activates system-level sleep prevention and periodically executes
        interaction commands until stopped.
        """
        self.is_running = True
        self.controller.start_caffeinate()

        logger.info(f"Engine started. Interval: {self.interval}s")
        try:
            while self.is_running:
                logger.info("Performing activity...")
                self.controller.focus_teams_and_interact()

                # Sleep in small increments to allow for faster interruption
                for _ in range(self.interval):
                    if not self.is_running:
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.controller.stop_caffeinate()

    def stop(self):
        """Stops the activity loop gracefully."""
        self.is_running = False
        logger.info("Stopping engine...")
