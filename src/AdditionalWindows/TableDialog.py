from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QAbstractItemView, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.AdditionalWindows.ConfirmDialog import ConfirmDialog
from src.styles import *


# Вікно для показування таблиць бази даних
class TableDialog(QDialog):
    def __init__(self, title_name, table_name, model_class, add_edit_class, table_width,
                 parent=None, table_max_height=None, is_add_button=True, is_edit_button=True):
        super().__init__(parent)
        # Приховання назви вікна (верхньої панелі)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.title_name = title_name
        self.table_name = table_name
        self.model_class = model_class
        self.add_edit_class = add_edit_class  # Клас вікна додавання/зміни елементів
        self.table_width = table_width
        self.table_max_height = table_max_height
        self.is_add_button = is_add_button
        self.is_edit_button = is_edit_button

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
                        text-color: white;
                    }
                """)
        # Встановлення іконки вікна
        icon = QIcon("../resources/icons/main_window_icon.svg")
        self.setWindowIcon(icon)
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
        if self.is_add_button:
            add_button = QPushButton()
            add_button.setIcon(QIcon('../resources/icons/add_icon.svg'))
            add_button.setText("Додати")
            add_button.setIconSize(add_button.sizeHint() * 3)
            add_button.setStyleSheet(button_style)
            add_button.setFont(text_font2)
            add_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            add_button.setFixedWidth(550)
            add_button.clicked.connect(self.open_add_dialog)

            # Підключення обробників подій для зміни курсора
            add_button.enterEvent = self.on_enter_event
            add_button.leaveEvent = self.on_leave_event

            add_button_layout = QHBoxLayout()
            add_button_layout.addWidget(add_button)
            add_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            add_button_widget = QWidget()
            add_button_widget.setLayout(add_button_layout)
            button_layout.addWidget(add_button_widget)

        # Кнопка "Змінити"
        if self.is_edit_button:
            edit_button = QPushButton()
            edit_button.setIcon(QIcon('../resources/icons/edit_icon.svg'))
            edit_button.setText("Змінити")
            edit_button.setIconSize(edit_button.sizeHint() * 3)
            edit_button.setStyleSheet(button_style)
            edit_button.setFont(text_font2)
            edit_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            edit_button.setFixedWidth(550)
            edit_button.clicked.connect(self.open_edit_dialog)

            # Підключення обробників подій для зміни курсора
            edit_button.enterEvent = self.on_enter_event
            edit_button.leaveEvent = self.on_leave_event

            edit_button_layout = QHBoxLayout()
            edit_button_layout.addWidget(edit_button)
            edit_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            edit_button_widget = QWidget()
            edit_button_widget.setLayout(edit_button_layout)
            button_layout.addWidget(edit_button_widget)

        # Кнопка "Видалити"
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('../resources/icons/delete_icon.svg'))
        delete_button.setText("Видалити")
        delete_button.setIconSize(delete_button.sizeHint() * 3)
        delete_button.setStyleSheet(button_style)
        delete_button.setFont(text_font2)
        delete_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        delete_button.setFixedWidth(550)
        delete_button.clicked.connect(self.delete_item)

        # Підключення обробників подій для зміни курсора
        delete_button.enterEvent = self.on_enter_event
        delete_button.leaveEvent = self.on_leave_event

        delete_button_layout = QHBoxLayout()
        delete_button_layout.addWidget(delete_button)
        delete_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        delete_button_widget = QWidget()
        delete_button_widget.setLayout(delete_button_layout)
        button_layout.addWidget(delete_button_widget)

        layout.addLayout(button_layout)

        # Додавання QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet(table_style)
        self.table_widget.setFont(text_font8)
        self.table_widget.horizontalHeader().setFont(text_font6)
        self.table_widget.verticalHeader().setFont(text_font6)
        self.table_widget.setFixedWidth(self.table_width)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        if self.table_max_height:
            self.table_widget.setFixedHeight(self.table_max_height)
        else:
            self.table_widget.setFixedHeight(580)

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
        self.load_table_data()
        self.setLayout(layout)

    def load_table_data(self):
        items = self.model_class.get_all()
        if items:
            column_count = len(items[0].__dict__)
            self.table_widget.setRowCount(len(items))
            self.table_widget.setColumnCount(column_count)
            self.table_widget.setHorizontalHeaderLabels(list(items[0].__dict__.keys()))

            for row, item in enumerate(items):
                for col, (key, value) in enumerate(item.__dict__.items()):
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрування тексту в ячейках
                    self.table_widget.setItem(row, col, table_item)

            # Приховати колонку employee_password, якщо така є
            header_labels = list(items[0].__dict__.keys())
            if "employee_password" in header_labels:
                col_index = header_labels.index("employee_password")
                self.table_widget.hideColumn(col_index)

        # Зміна ширини колонок відповідно до вмісту
        self.table_widget.resizeColumnsToContents()
        # Збільшення ширини кожної колонки на 30 пунктів
        for col in range(self.table_widget.columnCount()):
            self.table_widget.setColumnWidth(col, self.table_widget.columnWidth(col) + 30)

        # Встановлення висоти рядків
        self.table_widget.resizeRowsToContents()

    def open_add_dialog(self):
        dialog = self.add_edit_class(self.model_class, self)
        dialog.exec_()
        self.load_table_data()

    def open_edit_dialog(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Виберіть елемент для редагування")
            msg_box.setStyleSheet(message_box_style)
            msg_box.exec()
            return

        selected_row = self.table_widget.row(selected_items[0])
        item_id = self.table_widget.item(selected_row, 0).text()
        instance = self.model_class.get_by_id(item_id)

        dialog = self.add_edit_class(self.model_class, self, instance)
        dialog.exec_()
        self.load_table_data()

    def delete_item(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Виберіть елемент для видалення")
            msg_box.setStyleSheet(message_box_style)
            msg_box.exec()
            return

        selected_row = self.table_widget.row(selected_items[0])
        item_id = self.table_widget.item(selected_row, 0).text()
        instance = self.model_class.get_by_id(item_id)

        dialog = ConfirmDialog(f"Ви впевнені, що хочете видалити елемент з ID {item_id}?")
        if dialog.exec() == QDialog.Accepted:
            instance.delete()
            self.load_table_data()

    # Функції зміни курсора
    def on_enter_event(self, event):
        self.setCursor(self.click_cursor)
        event.accept()

    def on_leave_event(self, event):
        self.setCursor(self.arrow_cursor)
        event.accept()
