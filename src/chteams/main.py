"""Main entry point for the chteams utility.

This module initializes logging and orchestrates the MacOSController and
ActivityEngine to keep the system and Teams active.
"""
import logging
import sys
from .macos import MacOSController
from .engine import ActivityEngine
from .ui import show_banner, show_summary

logger = logging.getLogger(__name__)


def setup_logging():
    """Configures the root logger for the application.

    Sets up a stream handler that prints formatted logs to stdout.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    """Initializes and runs the activity engine.

    Sets up the controller and engine, then starts the main execution loop.
    Handles keyboard interrupts for graceful shutdown.
    """
    setup_logging()
    show_banner()

    controller = MacOSController()
    engine = ActivityEngine(controller=controller)

    try:
        uptime, count = engine.run()
        show_summary(uptime, count)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
