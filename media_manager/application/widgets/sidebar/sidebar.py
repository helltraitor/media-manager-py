import logging

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

from media_manager.application.api.module import Module
from media_manager.application.callbacks import Callback
from media_manager.application.filters import AllFilter

from .widget import SideBarWidget


class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.__widgets: dict[str, SideBarWidget] = {}
        self.__layout = QVBoxLayout(self)

        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(0, 0, 0, 0)
        # Self
        self.setFixedWidth(84)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed))

    def __widget_chosen(self, chosen: SideBarWidget):
        for widget in self.__widgets.values():
            if widget is not chosen and widget.selected():
                widget.reset_selection()

    def widget_add(self, module: Module):
        m_widget = module.widget.widget()
        sb_widget = SideBarWidget(m_widget)

        m_widget.callback_set("reset-other-selections-on-click", Callback(
            lambda: self.__widget_chosen(sb_widget))
                .with_filter(AllFilter(
                    lambda e: isinstance(e, QMouseEvent),
                    lambda e: e.button() == Qt.LeftButton and e.type() == QMouseEvent.MouseButtonPress)))

        # str_alignment = sb_widget.widget.alignment()
        # qt_alignment = {
        #     "BEGIN": Qt.AlignTop,
        #     "END": Qt.AlignBottom
        # }.get(str_alignment, Qt.AlignTop)

        if self.__widgets.get(module.id, None) is not None:
            logging.warning(f'{type(self).__name__}: Attempting to add a module widget with the same `{module.id}` id')
            return

        self.__widgets[module.id] = sb_widget
        self.__layout.addWidget(sb_widget, alignment=Qt.AlignTop)

    def widget_remove(self, module: Module):
        widget = self.__widgets.pop(module.id, None)
        if widget is None:
            logging.error(
                f'{type(self).__name__}: {type(widget).__name__} is not found for module with `{module.id}` id')
            return

        self.v_layout.removeWidget(widget)
