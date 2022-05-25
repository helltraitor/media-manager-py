import logging

from PySide2.QtWidgets import QWidget, QStackedLayout

from media_manager.application.modules import Module

from.layer import MainWidgetLayer


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__layers: dict[str, MainWidgetLayer] = {}
        self.__stack = QStackedLayout(self)
        self.__setup()

    def __setup(self):
        self.__stack.setContentsMargins(0, 0, 0, 0)

    def window_add(self, module: Module):
        layer = MainWidgetLayer(module.module_window)

        if self.__layers.get(module.id, None) is not None:
            logging.warning(f'{type(self).__name__}: Attempting to add a module window with the same `{module.id}` id')
            return
        self.__layers[module.id] = layer
        self.__stack.addWidget(layer)

    def window_remove(self, module: Module):
        layer = self.__layers.pop(module.id, None)
        if layer is None:
            logging.error(
                f'{type(self).__name__}: {type(layer).__name__} is not found for module with `{module.id}` id')
            return
        self.__stack.removeWidget(layer)
