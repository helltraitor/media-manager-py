from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout

from media_manager.application.api.module.widget import Widget


class SideBarWidget(QWidget):
    def __init__(self, widget: Widget):
        super().__init__()
        # Data
        self.__selected = False
        # Gui
        self.__layout = QVBoxLayout(self)
        self.__widget = widget
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__widget, alignment=Qt.AlignCenter)
        # Widget
        self.__widget.setFixedSize(72, 72)

    def mousePressEvent(self, event: QMouseEvent):
        if event.type() is QMouseEvent.MouseButtonPress and event.button() is Qt.LeftButton:
            if not self.__selected:
                self.__selected = True
                # TODO: Send message `widget was chosen`
            else:
                # TODO: Send message `widget was chosen again`
                pass

    def selected(self) -> bool:
        return self.__selected

    def reset_selection(self):
        self.__selected = False
        # TODO: Send message `widget selection was reset`
