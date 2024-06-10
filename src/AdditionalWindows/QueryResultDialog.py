from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QAbstractItemView)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *


# Клас вікна з результатом запиту
class QueryResultDialog(QDialog):
    def __init__(self, title_label, query_function, table_width, parent=None, table_max_height=None):
        super().__init__(parent)
        # Приховання назви вікна (верхньої панелі)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.title_label = title_label
        self.query_function = query_function
        self.table_width = table_width
        self.table_max_height = table_max_height

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
                        border: 1px solid white;
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
        title_label = QLabel(f"{self.title_label}")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Додавання QTableWidget
        self.table_widget = QTableWidget()

        # Виконання запиту та отримання результату
        column_names, result = self.query_function()
        if result:
            column_count = len(column_names)
            self.table_widget.setRowCount(len(result))
            self.table_widget.setColumnCount(column_count)
            self.table_widget.setHorizontalHeaderLabels(column_names)

            for row, row_data in enumerate(result):
                for col, value in enumerate(row_data):
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_widget.setItem(row, col, table_item)

            # Приховати колонку з ID (першу колонку)
            self.table_widget.setColumnHidden(0, True)

        self.table_widget.setStyleSheet(table_style)
        self.table_widget.setFont(text_font6)
        self.table_widget.horizontalHeader().setFont(text_font6)
        self.table_widget.verticalHeader().setFont(text_font6)
        self.table_widget.setFixedWidth(self.table_width)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        if self.table_max_height:
            self.table_widget.setFixedHeight(self.table_max_height)
        else:
            self.table_widget.setFixedHeight(580)

        # Зміна ширини колонок відповідно до вмісту
        self.table_widget.resizeColumnsToContents()
        for col in range(self.table_widget.columnCount()):
            self.table_widget.setColumnWidth(col, self.table_widget.columnWidth(col) + 30)

        # Встановлення висоти рядків
        self.table_widget.resizeRowsToContents()

        # Розташування таблиці по центру
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_widget)
        table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(table_layout)

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
