import ctypes
import logging
import os
import pathlib
import sys

from media_manager.application import Application
from media_manager.application.constants import (
    APPLICATION_AUTHOR, APPLICATION_NAME, APPLICATION_VERSION, APPLICATION_API_VERSION
)

if os.name == "nt":
    application_id = f"{APPLICATION_AUTHOR}:{APPLICATION_NAME}:{APPLICATION_VERSION}:{APPLICATION_API_VERSION}"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(application_id)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)7s: %(filename)s %(funcName)s: %(message)s",
        level=logging.DEBUG)

    location = pathlib.Path(__file__).parent
    application = Application(location)
    sys.exit(application.start())
