from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DriverWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Driver Dashboard")
        layout.addWidget(label)
        self.setLayout(layout)
