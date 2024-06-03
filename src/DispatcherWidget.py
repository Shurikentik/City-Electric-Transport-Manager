from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DispatcherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Dispatcher Dashboard")
        layout.addWidget(label)
        self.setLayout(layout)