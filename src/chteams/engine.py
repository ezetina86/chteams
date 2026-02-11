import time
import logging
from .macos import MacOSController

logger = logging.getLogger(__name__)

class ActivityEngine:
    """Orchestrates the activity simulation loop."""

    def __init__(self, controller: MacOSController, interval: int = 240):
        self.controller = controller
        self.interval = interval
        self.is_running = False

    def run(self):
        """Starts the infinite loop to keep the session active."""
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
        """Stops the activity loop."""
        self.is_running = False
        logger.info("Stopping engine...")
