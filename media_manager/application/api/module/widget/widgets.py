from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QMouseEvent

from media_manager.application.api.events.module.widget import (
    WidgetHoveredEvent, WidgetFocusedEvent, WidgetUnhoveredEvent
)

from .abc import Widget, ModuleWidget


class FocusableWidget(Widget):
    def __init__(self, module: ModuleWidget):
        super().__init__(module)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.module.events.announce(WidgetFocusedEvent(self.module))


class HoverableWidget(Widget):
    def __init__(self, module: ModuleWidget):
        super().__init__(module)

    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.module.events.announce(WidgetHoveredEvent(self.module))

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.module.events.announce(WidgetUnhoveredEvent(self.module))
