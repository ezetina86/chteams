import logging
import sys
from .macos import MacOSController
from .engine import ActivityEngine

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    setup_logging()
    
    controller = MacOSController()
    engine = ActivityEngine(controller=controller)
    
    try:
        engine.run()
    except KeyboardInterrupt:
        print("
Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
