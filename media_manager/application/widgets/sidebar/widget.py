import logging

from PySide2.QtCore import Qt, QEvent, QRect
from PySide2.QtGui import QIcon, QMouseEvent
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget

from media_manager.application.api import ModuleWidget

from media_manager.application.callbacks import Callback
from media_manager.application.filters import AllFilter, SingleFilter

from .painters import (
    SideBarWidgetGrayPainter, SideBarWidgetWhitePainter, SideBarWidgetNonePainter
)


class SideBarWidget(QWidget):
    def __init__(self, widget: ModuleWidget):
        super().__init__()
        self.__callbacks: dict[str, Callback] = {}
        self.widget = widget
        self.painter = SideBarWidgetNonePainter

        self.v_layout = QVBoxLayout(self)
        self.icon = QIcon(widget.icon())
        self.icon_label = QLabel()
        self.title_label = QLabel()
        self.__setup()

    def __setup(self):
        # Label
        self.icon_label.setContentsMargins(0, 0, 0, 0)
        self.icon_label.setPixmap(self.icon.pixmap(36, 36))
        self.title_label.setText(self.widget.title())
        # Layout
        self.v_layout.setContentsMargins(6, 6, 6, 6)
        self.v_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        self.v_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        # Self
        self.setFixedSize(72, 72)
        self.__setup_callbacks()

    def __setup_callbacks(self):
        # Hover events
        self.callback_set("set-painter-on-hover-enter", Callback(
            lambda: setattr(self, "painter", SideBarWidgetGrayPainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QEvent) and e.type() == QEvent.Enter,
                    lambda obj: self.painter is not SideBarWidgetWhitePainter)))
        self.callback_set("set-painter-on-hover-leave", Callback(
            lambda: setattr(self, "painter", SideBarWidgetNonePainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QEvent) and e.type() == QEvent.Leave,
                    lambda _: self.painter is not SideBarWidgetWhitePainter)))
        # Click event
        self.callback_set("set_painter-on-left-click", Callback(
            lambda: setattr(self, "painter", SideBarWidgetWhitePainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QMouseEvent),
                    lambda e: e.button() == Qt.LeftButton and e.type() == QMouseEvent.MouseButtonPress,
                    lambda _: self.painter is not SideBarWidgetWhitePainter)))
        # Paint event
        self.callback_set("background-paint", Callback(
            lambda: self.painter.paint(self))
                .with_filter(SingleFilter(lambda e: isinstance(e, QEvent) and e.type() == QEvent.Paint)))

    @property
    def active_rect(self) -> QRect:
        rect = self.rect()
        return QRect(rect.x() + 3, rect.y() + 3, rect.width() - 6, rect.height() - 6)

    def event(self, event: QEvent) -> bool:
        for callback in self.__callbacks.values():
            callback.call_on(event)
        return False

    def callback_set(self, key: str, callback: Callback):
        self.__callbacks[key] = callback

    def callback_remove(self, key: str):
        callback = self.__callbacks.pop(key, None)
        if callback is None:
            logging.warning(f'{type(self).__name__}: Attempting to remove non-existing callback')

    def selected(self) -> bool:
        return self.painter is SideBarWidgetWhitePainter

    def reset_selection(self):
        self.painter = SideBarWidgetNonePainter
        self.repaint()
