from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QBrush, QColor, QPainterPath

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .widget import SideBarWidget


class SideBarWidgetPainter:
    def paint(self, widget: "SideBarWidget"):
        pass


class SideBarWidgetBackgroundPainter:
    def __init__(self, color: QColor):
        self.color = color

    def paint(self, widget: "SideBarWidget"):
        hover_path = QPainterPath()
        hover_path.addRoundRect(widget.active_rect, 18)

        painter = QPainter(widget)
        painter.setRenderHint(painter.Antialiasing)
        painter.fillPath(hover_path, QBrush(self.color))


SideBarWidgetGrayPainter = SideBarWidgetBackgroundPainter(Qt.lightGray)
SideBarWidgetWhitePainter = SideBarWidgetBackgroundPainter(Qt.white)
SideBarWidgetNonePainter = SideBarWidgetPainter()
