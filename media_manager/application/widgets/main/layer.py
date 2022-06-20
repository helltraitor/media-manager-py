from PySide2.QtWidgets import QWidget, QVBoxLayout

from media_manager.application.api.module.components.window.abc import Window


class MainWidgetLayer(QWidget):
    def __init__(self, window: Window):
        super().__init__()
        self.__container = QVBoxLayout(self)
        self.__window = window
        self.__setup()

    def __setup(self):
        # Layout
        self.__container.setContentsMargins(0, 0, 0, 0)
        self.__container.addWidget(self.__window)
