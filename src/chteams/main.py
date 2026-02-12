"""Main entry point for the chteams utility.

This module initializes logging and orchestrates the MacOSController and
ActivityEngine to keep the system and Teams active.
"""
import logging
import sys
import argparse
from .macos import MacOSController
from .engine import ActivityEngine
from .ui import show_banner, show_summary

logger = logging.getLogger(__name__)


def setup_logging(debug=False):
    """Configures the root logger for the application.

    Sets up a stream handler that prints formatted logs to stdout.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    """Initializes and runs the activity engine.

    Sets up the controller and engine, then starts the main execution loop.
    Handles keyboard interrupts for graceful shutdown.
    """
    parser = argparse.ArgumentParser(description="Microsoft Teams Anti-Away Utility")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(args.debug)
    show_banner()

    controller = MacOSController()
    engine = ActivityEngine(controller=controller)

    try:
        uptime, count = engine.run()
        show_summary(uptime, count)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
