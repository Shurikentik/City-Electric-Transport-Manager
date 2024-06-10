from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,
                               QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *
from models.Route import Route


# Вікно додавання/зміни маршруту
class AddEditRouteDialog(QDialog):
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
        title_label = QLabel(f"{'Змінити' if self.instance else 'Додати новий'} маршрут")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Надпис "Введіть номер маршруту" (тільки для додавання)
        if not self.instance:
            input_number_label = QLabel("Введіть номер маршруту")
            input_number_label.setStyleSheet(text_style)
            input_number_label.setFont(text_font5)
            input_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(input_number_label)

            # Рядок "Номер маршруту"
            # Іконка номеру маршруту
            number_icon_pixmap = QPixmap("../resources/icons/route_number_icon.svg").scaled(100, 100)
            number_icon_label = QLabel()
            number_icon_label.setPixmap(number_icon_pixmap)

            # Текстове поле для номеру маршруту
            self.number_line_edit = QLineEdit()
            self.number_line_edit.setPlaceholderText("Номер маршруту")
            self.number_line_edit.setStyleSheet(text_line_style)
            self.number_line_edit.setFont(text_font4)

            # Підключення обробників подій для зміни курсора
            self.number_line_edit.setCursor(self.text_cursor)
            self.number_line_edit.enterEvent = self.on_line_edit_enter
            self.number_line_edit.leaveEvent = self.on_line_edit_leave

            # Об'єднання рядку з номером маршруту
            number_layout = QHBoxLayout()
            number_layout.addWidget(number_icon_label)
            number_layout.addWidget(self.number_line_edit)
            number_layout.setSpacing(20)
            number_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addLayout(number_layout)
        else:
            # Показати номер маршруту, але не дозволяти його змінювати
            number_label = QLabel(f"Номер маршруту: {self.instance.route_number}")
            number_label.setStyleSheet(text_style)
            number_label.setFont(text_font5)
            number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(number_label)

        # Надпис "Введіть початкову станцію"
        input_start_station_label = QLabel("Введіть початкову станцію")
        input_start_station_label.setStyleSheet(text_style)
        input_start_station_label.setFont(text_font5)
        input_start_station_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_start_station_label)

        # Рядок "Початкова станція"
        # Іконка станції
        start_station_icon_pixmap = QPixmap("../resources/icons/station_icon.svg").scaled(100, 100)
        start_station_icon_label = QLabel()
        start_station_icon_label.setPixmap(start_station_icon_pixmap)

        # Текстове поле для початкової станції
        self.start_station_line_edit = QLineEdit()
        if self.instance:
            self.start_station_line_edit.setText(self.instance.start_station)
        self.start_station_line_edit.setPlaceholderText("Початкова станція")
        self.start_station_line_edit.setStyleSheet(text_line_style)
        self.start_station_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        self.start_station_line_edit.setCursor(self.text_cursor)
        self.start_station_line_edit.enterEvent = self.on_line_edit_enter
        self.start_station_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з початковою станцією
        start_station_layout = QHBoxLayout()
        start_station_layout.addWidget(start_station_icon_label)
        start_station_layout.addWidget(self.start_station_line_edit)
        start_station_layout.setSpacing(20)
        start_station_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(start_station_layout)

        # Надпис "Введіть кінцеву станцію"
        input_end_station_label = QLabel("Введіть кінцеву станцію")
        input_end_station_label.setStyleSheet(text_style)
        input_end_station_label.setFont(text_font5)
        input_end_station_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_end_station_label)

        # Рядок "Кінцева станція"
        # Іконка станції
        end_station_icon_pixmap = QPixmap("../resources/icons/station_icon.svg").scaled(100, 100)
        end_station_icon_label = QLabel()
        end_station_icon_label.setPixmap(end_station_icon_pixmap)

        # Текстове поле для кінцевої станції
        self.end_station_line_edit = QLineEdit()
        if self.instance:
            self.end_station_line_edit.setText(self.instance.end_station)
        self.end_station_line_edit.setPlaceholderText("Кінцева станція")
        self.end_station_line_edit.setStyleSheet(text_line_style)
        self.end_station_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        self.end_station_line_edit.setCursor(self.text_cursor)
        self.end_station_line_edit.enterEvent = self.on_line_edit_enter
        self.end_station_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з кінцевою станцією
        end_station_layout = QHBoxLayout()
        end_station_layout.addWidget(end_station_icon_label)
        end_station_layout.addWidget(self.end_station_line_edit)
        end_station_layout.setSpacing(20)
        end_station_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(end_station_layout)

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

        # Підключення кнопки до команди
        add_edit_button.clicked.connect(self.save_route)

        add_edit_button_layout = QHBoxLayout()
        add_edit_button_layout.addWidget(add_edit_button)
        add_edit_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        add_edit_button_widget = QWidget()
        add_edit_button_widget.setLayout(add_edit_button_layout)

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

    def save_route(self):
        start_station = self.start_station_line_edit.text().strip()
        end_station = self.end_station_line_edit.text().strip()

        if not self.instance:
            # Додавання нового маршруту
            route_number = self.number_line_edit.text().strip()

            if not route_number or route_number == "Номер маршруту":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть номер маршруту")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            if not start_station or start_station == "Початкова станція":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть початкову станцію")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            if not end_station or end_station == "Кінцева станція":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть кінцеву станцію")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            if Route.is_route_number_exists(route_number):
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Маршрут з таким номером вже існує")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            try:
                new_route = self.model_class(route_number=route_number,
                                             start_station=start_station,
                                             end_station=end_station)
                new_route.save()
                msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Маршрут успішно додано")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                self.close()
            except Exception as e:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()

        else:
            # Зміна існуючого маршруту
            if start_station == self.instance.start_station and end_station == self.instance.end_station:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Ви нічого не змінили")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            if not start_station or start_station == "Початкова станція":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть початкову станцію")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            if not end_station or end_station == "Кінцева станція":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть кінцеву станцію")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            try:
                self.instance.start_station = start_station
                self.instance.end_station = end_station
                self.instance.update()
                msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Маршрут успішно змінено")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                self.close()
            except Exception as e:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()

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
