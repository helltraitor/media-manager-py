from PySide2.QtWidgets import QApplication


class Application(QApplication):
    def __init__(self):
        super().__init__()

        from PySide2.QtWidgets import QWidget
        self.window = QWidget()

    def start(self) -> int:
        self.window.show()
        return self.exec_()


if __name__ == "__main__":
    application = Application()
    exit(application.start())
