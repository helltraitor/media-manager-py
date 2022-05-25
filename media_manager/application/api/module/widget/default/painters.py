from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor, QPainter, QPainterPath
from PySide2.QtWidgets import QWidget


class ModuleWidgetDefaultPainter:
    def paint(self, widget: QWidget):
        pass


class ModuleWidgetBackgroundPainter:
    def __init__(self, color: QColor):
        self.__color = color

    def paint(self, widget: QWidget):
        hover_path = QPainterPath()
        hover_path.addRoundRect(widget.rect(), 18)

        painter = QPainter(widget)
        painter.setRenderHint(painter.Antialiasing)
        painter.fillPath(hover_path, QBrush(self.__color))


ModuleWidgetGrayBackgroundPainter = ModuleWidgetBackgroundPainter(Qt.lightGray)
ModuleWidgetWhiteBackgroundPainter = ModuleWidgetBackgroundPainter(Qt.white)
ModuleWidgetNoneBackgroundPainter = ModuleWidgetDefaultPainter()
