from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *


# Вікно додавання/зміни типу терміну чинності
class AddEditValidityTypeDialog(QDialog):
    def __init__(self, model_class, table_dialog, instance=None, parent=None):
        super().__init__(parent)
        self.model_class = model_class
        self.table_dialog = table_dialog
        self.instance = instance
        # Приховання назви вікна (верхньої панелі)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("""
                    QDialog {
                        background-color: qradialgradient(
                            spread: reflect, cx: 0.231, cy: 0.738364, radius: 0.343, 
                            fx: 0.267894, fy: 0.625, 
                            stop: 0.40113 rgba(0, 61, 173, 255), 
                            stop: 0.983051 rgba(58, 16, 145, 255), 
                            stop: 1 rgba(140, 255, 225, 255)
                        );
                        text-color: white;
                        border: 1px solid white;
                    }
                """)
        # Встановлення іконки вікна
        icon = QIcon("../resources/icons/main_window_icon.svg")
        self.setWindowIcon(icon)
        # Встановлення курсорів
        self.arrow_cursor = arrow_cursor
        self.click_cursor = click_cursor
        self.text_cursor = text_cursor
        self.setCursor(self.arrow_cursor)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Додавання назви вікна
        title_label = QLabel(f"{"Змінити" if self.instance else "Додати новий"} тип терміну чинності")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Надпис "Введіть назву типу транспорту"
        input_type_label = QLabel("Введіть назву типу терміну чинності")
        input_type_label.setStyleSheet(text_style)
        input_type_label.setFont(text_font5)
        input_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_type_label)

        # Рядок "Назва типу"
        # Іконка терміну чинності
        time_icon_pixmap = QPixmap("../resources/icons/time_icon.svg").scaled(100, 100)
        time_icon_label = QLabel()
        time_icon_label.setPixmap(time_icon_pixmap)

        # Текстове поле для типу терміну чинності
        type_line_edit = QLineEdit()
        if self.instance:
            type_line_edit.setText(self.instance.validity_name)
        else:
            type_line_edit.setPlaceholderText("Тип терміну чинності")
        type_line_edit.setStyleSheet(text_line_style)
        type_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        type_line_edit.setCursor(self.text_cursor)
        type_line_edit.enterEvent = self.on_line_edit_enter
        type_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з типом транспорту
        type_layout = QHBoxLayout()
        type_layout.addWidget(time_icon_label)
        type_layout.addWidget(type_line_edit)
        type_layout.setSpacing(20)
        type_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(type_layout)

        # Додавання кнопок
        button_layout = QHBoxLayout()

        # Кнопка "Додати/Змінити"
        add_edit_button = QPushButton()
        add_edit_button.setIcon(QIcon("../resources/icons/edit_icon.svg" if self.instance
                                      else "../resources/icons/add_icon.svg"))
        add_edit_button.setText("Змінити" if self.instance else "Додати")
        add_edit_button.setIconSize(add_edit_button.sizeHint() * 3)
        add_edit_button.setStyleSheet(button_style)
        add_edit_button.setFont(text_font2)
        add_edit_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        add_edit_button.setFixedWidth(550)

        # Підключення обробників подій для зміни курсора
        add_edit_button.enterEvent = self.on_enter_event
        add_edit_button.leaveEvent = self.on_leave_event

        add_edit_button_layout = QHBoxLayout()
        add_edit_button_layout.addWidget(add_edit_button)
        add_edit_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        add_edit_button_widget = QWidget()
        add_edit_button_widget.setLayout(add_edit_button_layout)

        # Обробка події натискання кнопки "Додати/Змінити"
        def save_validity_type():
            validity_name = type_line_edit.text().strip()

            if not self.instance:
                # Додавання нового об'єкта
                if not validity_name or validity_name == "Тип терміну чинності":
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Ви не вказали назву типу терміну чинності")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                # Перевірка унікальності назви
                existing_types = [validity.validity_name for validity in self.model_class.get_all()]
                if validity_name in existing_types:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Тип терміну чинності з такою назвою вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    new_validity_type = self.model_class(validity_name=validity_name)
                    new_validity_type.save()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Тип терміну чинності успішно додано")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
            else:
                # Зміна існуючого об'єкта
                if validity_name == self.instance.validity_name:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Ви нічого не змінили у назві терміну чинності")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                # Перевірка унікальності назви
                existing_types = [validity.validity_name for validity in self.model_class.get_all() if
                                  validity.validity_type_id != self.instance.validity_type_id]
                if validity_name in existing_types:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Тип терміну чинності з такою назвою вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    self.instance.validity_name = validity_name
                    self.instance.update()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Тип терміну чинності успішно змінено")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

        # Підключення кнопки до команди
        add_edit_button.clicked.connect(save_validity_type)

        # Кнопка "Відмінити"
        exit_button = QPushButton()
        exit_button.setIcon(QIcon('../resources/icons/cancel_icon.svg'))
        exit_button.setText("Відмінити")
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

        button_layout.addWidget(add_edit_button_widget)
        button_layout.addWidget(exit_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    # Функції зміни курсора
    def on_enter_event(self, event):
        self.setCursor(self.click_cursor)
        event.accept()

    def on_leave_event(self, event):
        self.setCursor(self.arrow_cursor)
        event.accept()

    def on_line_edit_enter(self, event):
        self.setCursor(self.text_cursor)
        event.accept()

    def on_line_edit_leave(self, event):
        self.setCursor(self.arrow_cursor)
        event.accept()
