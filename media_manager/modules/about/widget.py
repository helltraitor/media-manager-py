from pathlib import Path

from media_manager.application.api.module.components import CDefaultWidget
from media_manager.application.api.module.features import FDefaultWidget


class CAboutDefaultWidget(CDefaultWidget):
    def icon(self) -> str:
        return str(Path(__file__).parent / "resources" / "carol-liao-inform-icon.svg")

    def title(self) -> str:
        return "About"

    def type(self) -> str:
        return "System"
