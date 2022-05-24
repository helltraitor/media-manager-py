import logging

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

from media_manager.application.api import ModuleWidget
from media_manager.application.modules import Module


class SideBarWidget(QWidget):
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


class SideBar(QWidget):
    def __init__(self):
        super().__init__()

        self.widgets: dict[str, SideBarWidget] = {}

        self.v_layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.setFixedWidth(84)
        self.v_layout.setContentsMargins(0, 0, 0, 0)

    def widget_add(self, module: Module):
        sb_widget = SideBarWidget(module.module_widget)

        str_alignment = sb_widget.widget.alignment()
        qt_alignment = {
            "BEGIN": Qt.AlignTop,
            "END": Qt.AlignBottom
        }.get(str_alignment, Qt.AlignTop)

        if self.widgets.get(module.id, None) is not None:
            logging.warning(f'{type(self).__name__}: Attempting to add a module widget with the same `{module.id}` id')
            return

        self.widgets[module.id] = sb_widget
        self.v_layout.addWidget(sb_widget, alignment=qt_alignment)

    def widget_remove(self, module: Module):
        widget = self.widgets.pop(module.id, None)
        if widget is None:
            logging.error(
                f'{type(self).__name__}: {type(widget).__name__} is not found for module with `{module.id}` id')
            return

        self.v_layout.removeWidget(widget)
