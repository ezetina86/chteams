import time
import logging
from datetime import datetime, timedelta
from rich.live import Live
from .macos import MacOSController
from .ui import create_dashboard
from threading import Thread, Event

logger = logging.getLogger(__name__)


class InputHandler(Thread):
    """A dedicated thread to handle blocking user input."""
    def __init__(self):
        super().__init__(daemon=True)
        self.pause_requested = Event()
        self.stopped = Event()

    def run(self):
        while not self.stopped.is_set():
            try:
                # This will block until the user presses Enter
                line = input() 
                logger.info(f"[INPUT THREAD] Received: '{line.strip()}'")
                if line.strip().lower() == 'p':
                    self.pause_requested.set()
            except EOFError:
                # This can happen if stdin is closed
                break
    
    def stop(self):
        self.stopped.set()


class ActivityEngine:
    """Orchestrates the simulation loop to maintain active status."""

    def __init__(self, controller: MacOSController, interval: int = 240, debug: bool = False):
        """Initializes the engine with a controller and simulation interval."""
        self.controller = controller
        self.interval = interval
        self.debug = debug
        self.is_running = False
        self.paused = False
        self.start_time = None
        self.last_action_time = "Never"
        self.activity_count = 0
        self.last_message = ""
        self.message_expiry = None
        self.input_handler = InputHandler()

    def _handle_input(self):
        """Checks if the input handler has requested a pause."""
        if self.input_handler.pause_requested.is_set():
            self.paused = not self.paused
            msg = f"Engine {'paused' if self.paused else 'resumed'}"
            self._set_message(msg)
            logger.info(msg)
            self.input_handler.pause_requested.clear() # Reset for next toggle

    def _set_message(self, msg: str, duration: int = 5):
        """Sets a message to be displayed on the dashboard for a duration."""
        self.last_message = msg
        self.message_expiry = datetime.now() + timedelta(seconds=duration)

    def _get_current_message(self) -> str:
        """Returns the current message if not expired."""
        if self.message_expiry and datetime.now() < self.message_expiry:
            return self.last_message
        return ""

    def _get_uptime(self) -> str:
        """Calculates and formats the uptime."""
        if not self.start_time:
            return "00:00:00"
        delta = datetime.now() - self.start_time
        return str(timedelta(seconds=int(delta.total_seconds())))

    def run(self) -> tuple[str, int]:
        """Starts the main execution loop."""
        self.is_running = True
        self.start_time = datetime.now()
        self.controller.start_caffeinate()
        self.input_handler.start()

        logger.info(f"Engine started. Interval: {self.interval}s. Press 'p' then Enter to pause.")
        
        try:
            if self.debug:
                logger.info("Running in debug mode. Dashboard disabled.")
                self._run_debug_mode()
            else:
                self._run_live_mode()
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.input_handler.stop()
            self.controller.stop_caffeinate()

        return self._get_uptime(), self.activity_count

    def _run_debug_mode(self):
        """A simple, log-focused run loop for debugging."""
        while self.is_running:
            self._handle_input()
            if self.paused:
                logger.info("Engine is paused. Skipping activity.")
            else:
                logger.info("Simulating activity...")
                try:
                    self.controller.focus_teams_and_interact()
                    self.activity_count += 1
                    logger.info("Activity simulation successful.")
                except RuntimeError as e:
                    logger.error(f"Activity simulation failed: {e}")
            
            logger.info(f"Waiting for {self.interval} seconds...")
            for _ in range(self.interval):
                if not self.is_running:
                    break
                self._handle_input()
                time.sleep(1)

    def _run_live_mode(self):
        """The main run loop with the Rich live dashboard."""
        consecutive_failures = 0
        max_failures = 3

        with Live(create_dashboard("Starting...", "00:00:00", "Never", "N/A", self.interval, self._get_current_message()), refresh_per_second=1) as live:
            while self.is_running:
                self._handle_input() 
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
                    live.update(create_dashboard(current_status, self._get_uptime(), self.last_action_time, "Stopped", self.interval, self._get_current_message()))
                    break

                for remaining in range(self.interval, 0, -1):
                    if not self.is_running:
                        break
                    self._handle_input()
                    status_msg = "PAUSED" if self.paused else "Waiting"
                    next_act_str = f"{remaining}s" if not self.paused else "Paused"
                    live.update(create_dashboard(status_msg, self._get_uptime(), self.last_action_time, next_act_str, self.interval, self._get_current_message()))
                    time.sleep(1)

    def stop(self):
        """Stops the activity loop gracefully."""
        self.is_running = False
        logger.info("Stopping engine...")
