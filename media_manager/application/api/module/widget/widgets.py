from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QMouseEvent

from media_manager.application.api.events.module.widget import (
    WidgetHoveredEvent, WidgetFocusedEvent, WidgetUnhoveredEvent
)

from .abc import Widget, ModuleWidget


class FocusableWidget(Widget):
    def __init__(self, widget: ModuleWidget):
        super().__init__(widget)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.widget().events.announce(WidgetFocusedEvent(self.widget()))


class HoverableWidget(Widget):
    def __init__(self, widget: ModuleWidget):
        super().__init__(widget)

    def enterEvent(self, event: QEvent):
        super().enterEvent(event)
        self.widget().events.announce(WidgetHoveredEvent(self.widget()))

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self.widget().events.announce(WidgetUnhoveredEvent(self.widget()))
