import logging

from PySide2.QtWidgets import QWidget, QStackedLayout

from media_manager.application.api.module import ModuleWindow

from.layer import MainWidgetLayer


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__layers: list[MainWidgetLayer] = {}
        self.__stack = QStackedLayout(self)
        self.__setup()

    def __setup(self):
        self.__stack.setContentsMargins(0, 0, 0, 0)

    def window_add(self, module: ModuleWindow):
        layer = MainWidgetLayer(module)

        if layer in self.__layers:
            logging.warning(f'{type(self).__name__}: Attempting to add already added module window')
            return
        self.__layers.append(layer)
        self.__stack.addWidget(layer)
