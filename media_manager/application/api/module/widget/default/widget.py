import logging

from abc import ABC

from PySide2.QtCore import Qt, QEvent, QRect
from PySide2.QtGui import QIcon, QMouseEvent
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget

from media_manager.application.api.module.widget import ModuleWidget
from media_manager.application.callbacks import Callback
from media_manager.application.filters import AllFilter, SingleFilter

from .painters import (
    ModuleWidgetGrayBackgroundPainter, ModuleWidgetNoneBackgroundPainter, ModuleWidgetWhiteBackgroundPainter
)


# class ModuleDefaultWidget(ABC, ModuleWidget):
class ModuleDefaultWidget(ModuleWidget):
    def __init__(self):
        super().__init__()
        self.__callbacks: dict[str, Callback] = {}
        self.painter = ModuleWidgetNoneBackgroundPainter

        self.v_layout = QVBoxLayout(self)
        self.icon = QIcon(self.module_icon())
        self.icon_label = QLabel()
        self.title_label = QLabel()
        self.__setup()

    def __setup(self):
        # Label
        self.icon_label.setContentsMargins(0, 0, 0, 0)
        self.icon_label.setPixmap(self.icon_.pixmap(36, 36))
        self.title_label.setText(self.module_title())
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
            lambda: setattr(self, "painter", ModuleWidgetGrayBackgroundPainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QEvent) and e.type() == QEvent.Enter,
                    lambda obj: self.painter is not ModuleWidgetWhiteBackgroundPainter)))
        self.callback_set("set-painter-on-hover-leave", Callback(
            lambda: setattr(self, "painter", ModuleWidgetNoneBackgroundPainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QEvent) and e.type() == QEvent.Leave,
                    lambda _: self.painter is not ModuleWidgetWhiteBackgroundPainter)))
        # Click event
        self.callback_set("set_painter-on-left-click", Callback(
            lambda: setattr(self, "painter", ModuleWidgetWhiteBackgroundPainter),
            lambda: self.repaint())
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QMouseEvent),
                    lambda e: e.button() == Qt.LeftButton and e.type() == QMouseEvent.MouseButtonPress,
                    lambda _: self.painter is not ModuleWidgetWhiteBackgroundPainter)))
        # Paint event
        self.callback_set("background-paint", Callback(
            lambda: self.painter.paint(self))
                .with_filter(SingleFilter(lambda e: isinstance(e, QEvent) and e.type() == QEvent.Paint)))

    @property
    def active_rect(self) -> QRect:
        rect = self.rect()
        return QRect(rect.x() + 3, rect.y() + 3, rect.width() - 6, rect.height() - 6)

    def selected(self) -> bool:
        return self.painter is ModuleWidgetWhiteBackgroundPainter

    def reset_selection(self):
        self.painter = ModuleWidgetNoneBackgroundPainter
        self.repaint()
