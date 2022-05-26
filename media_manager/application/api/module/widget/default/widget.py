from abc import abstractmethod

from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QIcon, QMouseEvent
from PySide2.QtWidgets import QLabel, QVBoxLayout

from media_manager.application.api.module.widget import Widget, ModuleWidget
from media_manager.application.callbacks import Callback
from media_manager.application.filters import AllFilter, SingleFilter

from .painters import (
    ModuleWidgetGrayBackgroundPainter, ModuleWidgetNoneBackgroundPainter, ModuleWidgetWhiteBackgroundPainter
)


class DefaultWidget(Widget):
    def __init__(self, icon: QIcon, title: str):
        super().__init__()
        # ICON
        self.icon = icon
        self.icon_label = QLabel()
        # TITLE
        self.title = title
        self.title_label = QLabel()
        # OTHER
        self.v_layout = QVBoxLayout(self)
        self.painter = ModuleWidgetNoneBackgroundPainter
        self.__setup()

    def __setup(self):
        # Labels
        self.icon_label.setContentsMargins(0, 0, 0, 0)
        self.icon_label.setPixmap(self.icon.pixmap(36, 36))
        self.title_label.setText(self.title)
        # Layout
        self.v_layout.setContentsMargins(6, 6, 6, 6)
        self.v_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        self.v_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        # Self
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

    def selected(self) -> bool:
        return self.painter is ModuleWidgetWhiteBackgroundPainter

    def reset_selection(self):
        self.painter = ModuleWidgetNoneBackgroundPainter
        self.repaint()


class ModuleDefaultWidget(ModuleWidget):
    def __init__(self):
        self.__widget = DefaultWidget(QIcon(self.icon()), self.title())

    @abstractmethod
    def icon(self) -> str:
        pass

    @abstractmethod
    def title(self) -> str:
        pass

    def widget(self) -> Widget:
        return self.__widget
