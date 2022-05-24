import logging

from PySide2.QtCore import Qt, QEvent, QRect
from PySide2.QtGui import QIcon, QMouseEvent, QPaintEvent
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget

from media_manager.application.api import ModuleWidget

from media_manager.application.callbacks import Callback

from .painters import (
    SideBarWidgetGrayPainter, SideBarWidgetWhitePainter, SideBarWidgetNonePainter
)


class SideBarWidget(QWidget):
    def __init__(self, widget: ModuleWidget):
        super().__init__()
        self.__callbacks: dict[str, Callback] = {}
        self.widget = widget

        self.painter_on_hover = SideBarWidgetGrayPainter
        self.painter_on_click = SideBarWidgetWhitePainter
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

    @property
    def active_rect(self) -> QRect:
        rect = self.rect()
        return QRect(rect.x() + 3, rect.y() + 3, rect.width() - 6, rect.height() - 6)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.painter = self.painter_on_click
        self.repaint()

        # Temporally
        for callback in self.__callbacks.values():
            callback.call_on(event)

    def enterEvent(self, event: QEvent):
        if self.painter is not self.painter_on_click:
            self.painter = self.painter_on_hover
        self.repaint()

        # Temporally
        for callback in self.__callbacks.values():
            callback.call_on(event)

    def leaveEvent(self, event: QEvent):
        if self.painter is not self.painter_on_click:
            self.painter = None
        self.repaint()

        # Temporally
        for callback in self.__callbacks.values():
            callback.call_on(event)

    def paintEvent(self, event: QPaintEvent):
        self.painter.paint(self)

        # Temporally
        for callback in self.__callbacks.values():
            callback.call_on(event)

    def callback_set(self, key: str, callback: Callback):
        self.__callbacks[key] = callback

    def callback_remove(self, key: str):
        callback = self.__callbacks.pop(key, None)
        if callback is None:
            logging.warning(f'{type(self).__name__}: Attempting to remove non-existing callback')

    def selected(self) -> bool:
        return self.painter is self.painter_on_click

    def reset_selection(self):
        self.painter = SideBarWidgetNonePainter
