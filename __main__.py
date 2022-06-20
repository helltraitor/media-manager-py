import logging
import sys

from pathlib import Path

from media_manager.application import Application


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)7s: %(filename)s %(funcName)s: %(message)s",
        level=logging.DEBUG)

    location = Path(__file__).parent
    application = Application(location)
    sys.exit(application.start())
