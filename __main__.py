from pathlib import Path

from media_manager.application import Application


if __name__ == "__main__":
    app_location = Path(__file__).parent
    modules_location = app_location / "media_manager" / "modules"

    application = Application(app_location)
    application.add_modules_location(modules_location)

    exit(application.start())
