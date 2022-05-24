import logging

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from media_manager.application.api import ModuleWidget
from media_manager.application.modules import Module


class ModuleBarItem(QWidget):
    def __init__(self, widget: ModuleWidget):
        super().__init__()
        self.widget = widget

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
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        # Self
        self.setFixedSize(72, 72)


class ModuleBar(QWidget):
    def __init__(self):
        super().__init__()

        self.items: list[ModuleBarItem] = []

        self.v_layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.v_layout.setContentsMargins(0, 0, 0, 0)

    def widget_add(self, widget: ModuleWidget):
        item = ModuleBarItem(widget)

        str_alignment = widget.alignment()
        qt_alignment = {
            "BEGIN": Qt.AlignTop,
            "END": Qt.AlignBottom
        }.get(str_alignment, Qt.AlignTop)

        self.items.append(item)
        self.v_layout.addWidget(item, alignment=qt_alignment)

    def widget_remove(self, module: Module):
        module_item: ModuleBarItem | None = None
        for item in self.items:
            if item.widget is module.module_widget:
                module_item = item

        if module_item is None:
            logging.error(f'ModuleBar: ModuleBarItem is not found for module with `{module.id}` id')
            return

        self.v_layout.removeWidget(module_item.widget)
        self.items.remove(module_item)
