from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from media_manager.application.modules import Module


class ModuleBarItem(QWidget):
    def __init__(self, module: Module):
        super().__init__()
        self.module = module

        self.v_layout = QVBoxLayout(self)
        self.icon = QIcon(str(module.module_widget.icon()))
        self.icon_label = QLabel()
        self.title_label = QLabel()
        self.__setup()

    def __setup(self):
        # Label
        self.icon_label.setContentsMargins(0, 0, 0, 0)
        self.icon_label.setPixmap(self.icon.pixmap(36, 36))
        self.title_label.setText(self.module.module_widget.title())
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

    def reload_widgets(self):
        modules = QApplication.instance().keeper.module_all()
        removed = (item for item in self.items if item.module.id not in {module.id for module in modules})
        for item in removed:
            self.items.remove(item)
            self.v_layout.removeWidget(item)

        added = (module for module in modules if module.id not in {item.module.id for item in self.items})
        added = (module for module in added if module.module_widget is not None)
        for module in added:
            item = ModuleBarItem(module)
            self.items.append(item)
            self.v_layout.addWidget(item)
