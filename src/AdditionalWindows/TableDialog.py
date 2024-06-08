from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QHBoxLayout, QTableView
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt
from src.styles import *


# Вікно для показування таблиць бази даних
class TableDialog(QDialog):
    def __init__(self, title_name, table_name, model_class, parent=None):
        super().__init__(parent)
        # Приховання назви вікна (верхньої панелі)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.title_name = title_name
        self.table_name = table_name
        self.model_class = model_class

        # Встановлення градієнтного фону через стилі
        self.setStyleSheet("""
                    QDialog {
                        background-color: qradialgradient(
                            spread: reflect, cx: 0.231, cy: 0.738364, radius: 0.343, 
                            fx: 0.267894, fy: 0.625, 
                            stop: 0.40113 rgba(0, 61, 173, 255), 
                            stop: 0.983051 rgba(58, 16, 145, 255), 
                            stop: 1 rgba(140, 255, 225, 255)
                        );
                    }
                """)

        # Встановлення курсорів
        self.arrow_cursor = arrow_cursor
        self.click_cursor = click_cursor
        self.setCursor(self.arrow_cursor)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Додавання назви таблиці
        title_label = QLabel(f"Таблиця '{self.title_name}'")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Додавання кнопок
        button_layout = QHBoxLayout()

        # Кнопка "Додати"
        add_button = QPushButton()
        add_button.setIcon(QIcon('../resources/icons/add_icon.svg'))
        add_button.setText("Додати")
        add_button.setIconSize(add_button.sizeHint() * 3)
        add_button.setStyleSheet(button_style)
        add_button.setFont(text_font2)
        add_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        add_button.setFixedWidth(550)

        # Підключення обробників подій для зміни курсора
        add_button.enterEvent = self.on_enter_event
        add_button.leaveEvent = self.on_leave_event

        # Кнопка "Змінити"
        edit_button = QPushButton()
        edit_button.setIcon(QIcon('../resources/icons/edit_icon.svg'))
        edit_button.setText("Змінити")
        edit_button.setIconSize(edit_button.sizeHint() * 3)
        edit_button.setStyleSheet(button_style)
        edit_button.setFont(text_font2)
        edit_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        edit_button.setFixedWidth(550)

        # Підключення обробників подій для зміни курсора
        edit_button.enterEvent = self.on_enter_event
        edit_button.leaveEvent = self.on_leave_event

        # Кнопка "Видалити"
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('../resources/icons/delete_icon.svg'))
        delete_button.setText("Видалити")
        delete_button.setIconSize(delete_button.sizeHint() * 3)
        delete_button.setStyleSheet(button_style)
        delete_button.setFont(text_font2)
        delete_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        delete_button.setFixedWidth(550)

        # Підключення обробників подій для зміни курсора
        delete_button.enterEvent = self.on_enter_event
        delete_button.leaveEvent = self.on_leave_event

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(button_layout)

        # Додавання QTableView
        self.table_view = QTableView()

        items = self.model_class.get_all()
        if items:
            column_count = len(items[0].__dict__)
            self.model = QStandardItemModel(len(items), column_count)
            self.model.setHorizontalHeaderLabels(list(items[0].__dict__.keys()))

            for row, item in enumerate(items):
                for col, (key, value) in enumerate(item.__dict__.items()):
                    self.model.setItem(row, col, QStandardItem(str(value)))

            self.table_view.setModel(self.model)

        self.table_view.setStyleSheet("""
                    QTableView {
                        border-radius: 7px;
                        border-width: 1px;
                        border-style: solid;
                        border-color: white;
                        color: white;
                        background-color: rgba(255, 255, 255, 0.25);
                    }
                    QTableView::item:selected {
                        background-color: rgba(255, 255, 255, 0.4);
                    }
                """)
        self.table_view.setFont(text_font6)
        for row in range(self.table_view.model().rowCount()):
            self.table_view.setRowHeight(row, 70)
        for column in range(self.table_view.model().columnCount()):
            self.table_view.setColumnWidth(column, 300)
        layout.addWidget(self.table_view)

        # Кнопка "Вихід"
        exit_button = QPushButton()
        exit_button.setIcon(QIcon('../resources/icons/exit_icon.svg'))
        exit_button.setText("Вихід")
        exit_button.setIconSize(exit_button.sizeHint() * 3)
        exit_button.setStyleSheet(button_style)
        exit_button.setFont(text_font2)
        exit_button.setFixedWidth(550)
        exit_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        exit_button.enterEvent = self.on_enter_event
        exit_button.leaveEvent = self.on_leave_event

        # Підключення кнопки до команди
        exit_button.clicked.connect(self.close)

        # Встановлення кнопки по центру
        exit_layout = QHBoxLayout()
        exit_layout.addWidget(exit_button)
        exit_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        exit_widget = QWidget()
        exit_widget.setLayout(exit_layout)

        layout.addWidget(exit_widget)
        self.setLayout(layout)

    # Функції зміни курсора
    def on_enter_event(self, event):
        self.setCursor(self.click_cursor)
        event.accept()

    def on_leave_event(self, event):
        self.setCursor(self.arrow_cursor)
        event.accept()
