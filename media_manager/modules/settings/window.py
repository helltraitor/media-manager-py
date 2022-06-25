from weakref import ReferenceType

from PySide2.QtCore import QEvent, QItemSelectionModel, QModelIndex
from PySide2.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)

from media_manager.application.api.context import Context
from media_manager.application.api.module.components.window import CWindow
from media_manager.application.api.module.components.window.abc import Window
from media_manager.application.api.module.features import FWindow

from .storage import Storage, DomainStorage


class EditableSection(QWidget):
    def __init__(self):
        super().__init__()
        # Key
        self.__key_origin: str | None = None
        self.__key = QLineEdit("key")
        # Value
        self.__domain: DomainStorage | None = None
        self.__value = QLineEdit("value")
        # Buttons
        self.__create = QPushButton("Create")
        self.__update = QPushButton("Update")
        self.__delete = QPushButton("Delete")
        # Layout
        self.__layout = QHBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.disable()
        # Key
        self.__key.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__layout.addWidget(self.__key)
        # Value
        self.__value.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__layout.addWidget(self.__value)
        # Create
        self.__create.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.__create.clicked.connect(self.create_editable)
        self.__layout.addWidget(self.__create)
        # Update
        self.__update.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.__update.clicked.connect(self.apply_editable)
        self.__layout.addWidget(self.__update)
        # Delete
        self.__delete.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.__delete.clicked.connect(self.delete_editable)
        self.__layout.addWidget(self.__delete)

    def enable(self):
        self.__key.setEnabled(True)
        self.__value.setEnabled(True)
        self.__update.setEnabled(True)
        self.__delete.setEnabled(True)

    def disable(self):
        self.__key.setDisabled(True)
        self.__value.setDisabled(True)
        self.__update.setDisabled(True)
        self.__delete.setDisabled(True)

    def apply_editable(self):
        key = self.__key.text()
        value = self.__value.text()

        if key == self.__key_origin:
            self.__domain.set(key, value)
        else:
            self.__domain.set(key, value)
            self.__domain.delete(self.__key_origin)

        self.__key_origin = key

    def create_editable(self):
        key = self.__key.text()
        value = self.__value.text()

        if key == self.__key_origin:
            return
        self.__domain.set(key, value)
        self.reset_editable()

    def delete_editable(self):
        self.__domain.delete(self.__key_origin)
        self.reset_editable()

    def set_editable(self, domain: DomainStorage, key: str, value: str):
        self.__domain = domain
        self.__key_origin = key
        self.__key.setText(key)
        self.__value.setText(value)
        self.enable()

    def reset_editable(self):
        self.__key_origin = None
        self.__domain = None
        self.__key.setText("key")
        self.__value.setText("value")
        self.disable()


class TableWidget(QListWidget):
    def __init__(self, edit: EditableSection):
        super().__init__()
        self.__edit = edit
        self.__storage = Storage()
        self.__setup()

    def __setup(self):
        self.__storage.subscribe(action="set", callback=self.refill)
        self.__storage.subscribe(action="delete", callback=self.refill)
        self.__storage.subscribe(action="update", callback=self.refill)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.refill()

    def selectionCommand(self, index: QModelIndex, event: QEvent | None = None) -> QItemSelectionModel.SelectionFlags:
        if (index.row(), index.column()) < (0, 0):
            self.__edit.reset_editable()
            return super().selectionCommand(index, event)
        text = self.itemFromIndex(index).text()
        domain, key, value, *_ = text.split(" :: ")
        if self.__storage.exists(domain[1:-1]):
            self.__edit.set_editable(self.__storage.domain(domain[1:-1]), key[1:-1], value[1:-1])
        return super().selectionCommand(index, event)

    def refill(self):
        self.clear()
        items = ((domain, key, value)  # EXECUTED THIRDLY
                 for (domain, settings) in self.__storage.ONLINE_STORAGE.items()  # EXECUTED FIRSTLY
                 for (key, value) in settings.items())  # EXECUTED SECONDLY
        self.addItems(tuple(f"`{domain}` :: `{key}` :: `{value}`" for domain, key, value in items))


class SettingsWindow(Window):
    def __init__(self, component: ReferenceType[CWindow]):
        super().__init__(component)
        self.__title = QLabel()
        self.__edit = EditableSection()
        self.__table = TableWidget(self.__edit)
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        # Label
        font = self.__title.font()
        font.setPointSize(18)
        self.__title.setText("Settings")
        self.__title.setFont(font)
        self.__title.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.__layout.addWidget(self.__title)
        # EditableSection
        self.__edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__edit)
        # Table
        self.__table.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__table)


class CSettingsWindow(CWindow):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__window = SettingsWindow(ReferenceType(self))

    def window(self) -> QWidget:
        return self.__window
