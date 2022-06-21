from pathlib import Path

from media_manager.application.api.module.components import CDefaultWidget
from media_manager.application.api.module.features import FDefaultWidget


class CSettingsDefaultWidget(CDefaultWidget):
    def icon(self) -> str:
        return str(Path(__file__).parent / "resources" / "carol-liao-adjust-icon.svg")

    def title(self) -> str:
        return "Settings"

    def type(self) -> str:
        return "System"
