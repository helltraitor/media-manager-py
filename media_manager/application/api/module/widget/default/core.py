from abc import abstractmethod
from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPaintEvent
from PySide2.QtWidgets import QLabel, QVBoxLayout

from media_manager.application.api.events.gui import GuiEvent

from ..abc import ModuleWidget
from ..widgets import FocusableWidget, HoverableWidget

from .painters import ModuleWidgetNoneBackgroundPainter
from .listeners import DefaultBackgroundListener, DefaultBackgroundPaintEventListener


class DefaultWidget(FocusableWidget, HoverableWidget):
    def __init__(self, widget: ModuleWidget, icon: QIcon, title: str):
        super().__init__(widget)
        # Data
        self.painter = ModuleWidgetNoneBackgroundPainter
        # GUI
        self.__icon = icon
        self.__icon_label = QLabel()
        self.__title = title
        self.__title_label = QLabel()
        self.__layout = QVBoxLayout(self)
        # Setup
        self.__setup()

    def __setup(self):
        # Labels
        self.__icon_label.setContentsMargins(0, 0, 0, 0)
        self.__icon_label.setPixmap(self.__icon.pixmap(36, 36))
        self.__title_label.setText(self.__title)
        # Layout
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__icon_label, alignment=Qt.AlignCenter)
        self.__layout.addWidget(self.__title_label, alignment=Qt.AlignCenter)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        self.widget().events.announce(GuiEvent(event, self))


class ModuleDefaultWidget(ModuleWidget):
    def __init__(self):
        super().__init__()
        self.__widget = DefaultWidget(self, QIcon(self.icon()), self.title())
        self.__setup()

    def __setup(self):
        self.events.subscribe(DefaultBackgroundListener(self))
        self.events.subscribe(DefaultBackgroundPaintEventListener(self))

    def icon(self) -> str:
        return str(Path(__file__).parent.parent.parent.parent.parent.parent / "resources" / "carol-liao-solve-icon")

    @abstractmethod
    def title(self) -> str:
        pass

    def widget(self) -> DefaultWidget:
        return self.__widget
