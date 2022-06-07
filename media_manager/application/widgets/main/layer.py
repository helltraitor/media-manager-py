from PySide2.QtWidgets import QWidget, QVBoxLayout

from media_manager.application.api.module.window import ModuleWindow


class MainWidgetLayer(QWidget):
    def __init__(self, window: ModuleWindow):
        super().__init__()
        self.__container = QVBoxLayout(self)
        self.__window = window
        self.__setup()

    def __setup(self):
        # Layout
        self.__container.setContentsMargins(0, 0, 0, 0)
        self.__container.addWidget(self.__window.window())
