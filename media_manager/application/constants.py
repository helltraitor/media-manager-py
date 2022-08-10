from pathlib import Path

from media_manager.application.api.version import Version

APPLICATION_AUTHOR = "Helltraitor"
APPLICATION_ICON = Path(__file__).parent.parent / "resources" / "carol-liao-organize-icon.svg"
APPLICATION_NAME = "Media manager"
APPLICATION_VERSION = Version(0, 0, 1)
APPLICATION_API_VERSION = Version(0, 0, 1)
