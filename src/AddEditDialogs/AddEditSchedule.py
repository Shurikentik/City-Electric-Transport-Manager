from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                               QLineEdit, QPushButton, QMessageBox, QComboBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *
from models.Transport import Transport
from models.Route import Route
from models.Schedule import Schedule


# Вікно додавання/зміни розкладу
class AddEditScheduleDialog(QDialog):
    def __init__(self, model_class, table_dialog, instance=None, parent=None):
        super().__init__(parent)
        self.model_class = model_class
        self.table_dialog = table_dialog
        self.instance = instance
        self.transport_id = None
        self.route_id = None
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
        title_label = QLabel(f"{"Змінити" if self.instance else "Додати новий"} розклад")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Якщо розклад тільки додається, необхідно спочатку обрати день тижня, транспорт і маршрут
        if not self.instance:
            # Надпис "Оберіть день тижня"
            day_of_week_label = QLabel("Оберіть день тижня")
            day_of_week_label.setStyleSheet(text_style)
            day_of_week_label.setFont(text_font5)
            day_of_week_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(day_of_week_label)

            # Рядок для обирання дня тижня
            # Іконка календаря
            calendar_icon_pixmap = QPixmap("../resources/icons/calendar_icon.svg").scaled(100, 100)
            calendar_icon_label = QLabel()
            calendar_icon_label.setPixmap(calendar_icon_pixmap)

            # Випадаючий список вибору дня тижня
            day_of_week_combobox = QComboBox()
            day_of_week_combobox.setStyleSheet(combo_box_style)
            day_of_week_combobox.setFont(text_font4)
            day_of_week_combobox.setEditable(False)
            day_of_week_combobox.setCursor(self.click_cursor)
            day_of_week_combobox.setFixedWidth(600)
            day_of_week_combobox.setFixedHeight(100)

            # Додавання елементів до комбобоксу
            day_of_week_combobox.addItems(["Понеділок", "Вівторок", "Середа", "Четвер",
                                           "П'ятниця", "Субота", "Неділя"])
            day_of_week_combobox.setCurrentIndex(-1)

            # Функції зміни курсора
            day_of_week_combobox.enterEvent = self.on_enter_event
            day_of_week_combobox.leaveEvent = self.on_leave_event

            # Об'єднання рядку обирання дня тижня
            pick_day_of_week_layout = QHBoxLayout()
            pick_day_of_week_layout.addWidget(calendar_icon_label)
            pick_day_of_week_layout.addWidget(day_of_week_combobox)
            pick_day_of_week_layout.setSpacing(20)
            pick_day_of_week_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addLayout(pick_day_of_week_layout)

            # Надпис "Оберіть номер транспорту"
            transport_label = QLabel("Оберіть номер транспорту")
            transport_label.setStyleSheet(text_style)
            transport_label.setFont(text_font5)
            transport_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addWidget(transport_label)

            # Рядок для обирання електротранспорту
            # Іконка транспорту
            route_icon_pixmap = QPixmap("../resources/icons/trolleybus_icon.svg").scaled(100, 100)
            route_icon_label = QLabel()
            route_icon_label.setPixmap(route_icon_pixmap)

            # Випадаючий список вибору електротранспорту
            transport_combobox = QComboBox()
            transport_combobox.setStyleSheet(combo_box_style)
            transport_combobox.setFont(text_font4)
            transport_combobox.setEditable(False)
            transport_combobox.setCursor(self.click_cursor)
            transport_combobox.setFixedWidth(600)
            transport_combobox.setFixedHeight(100)

            # Встановлення елементів списку
            transports = Transport.get_all()
            transport_numbers = [transport.transport_number for transport in transports]
            transport_combobox.addItems(transport_numbers)
            transport_combobox.setCurrentIndex(-1)

            # Поєднання елементів списку з індексами
            transport_index_map = {}
            for i, transport in enumerate(transports):
                transport_index_map[transport.transport_number] = i

            # Функція переключення транспорту
            def transport_combobox_change(text):
                transport_index = transport_index_map.get(text)
                if transport_index is not None:
                    self.transport_id = transports[transport_index].transport_id

            # Підключення функції до комбобоксу
            transport_combobox.currentTextChanged.connect(transport_combobox_change)

            # Функції зміни курсора
            transport_combobox.enterEvent = self.on_enter_event
            transport_combobox.leaveEvent = self.on_leave_event

            # Об'єднання рядку обирання типу електротранспорту
            pick_transport_layout = QHBoxLayout()
            pick_transport_layout.addWidget(route_icon_label)
            pick_transport_layout.addWidget(transport_combobox)
            pick_transport_layout.setSpacing(20)
            pick_transport_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addLayout(pick_transport_layout)

            # Надпис "Оберіть номер маршруту"
            route_label = QLabel("Оберіть номер маршруту")
            route_label.setStyleSheet(text_style)
            route_label.setFont(text_font5)
            route_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addWidget(route_label)

            # Рядок для обирання номеру маршруту
            # Іконка маршруту
            route_icon_pixmap = QPixmap("../resources/icons/route_icon.svg").scaled(100, 100)
            route_icon_label = QLabel()
            route_icon_label.setPixmap(route_icon_pixmap)

            # Випадаючий список вибору номеру маршруту
            route_combobox = QComboBox()
            route_combobox.setStyleSheet(combo_box_style)
            route_combobox.setFont(text_font4)
            route_combobox.setEditable(False)
            route_combobox.setCursor(self.click_cursor)
            route_combobox.setFixedWidth(600)
            route_combobox.setFixedHeight(100)

            # Встановлення елементів списку
            routes = Route.get_all()
            route_numbers = [route.route_number for route in routes]
            route_combobox.addItems(route_numbers)
            route_combobox.setCurrentIndex(-1)

            # Поєднання елементів списку з індексами
            route_index_map = {}
            for i, route in enumerate(routes):
                route_index_map[route.route_id] = i

            # Функція переключення маршруту
            def route_combobox_change(text):
                route_index = route_index_map.get(text)
                if route_index is not None:
                    self.route_id = routes[route_index].route_id

            # Підключення функції до комбобоксу
            route_combobox.currentTextChanged.connect(route_combobox_change)

            # Функції зміни курсора
            route_combobox.enterEvent = self.on_enter_event
            route_combobox.leaveEvent = self.on_leave_event

            # Об'єднання рядку обирання маршруту
            pick_route_layout = QHBoxLayout()
            pick_route_layout.addWidget(route_icon_label)
            pick_route_layout.addWidget(route_combobox)
            pick_route_layout.setSpacing(20)
            pick_route_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addLayout(pick_route_layout)

        # Для додавання/зміни розкладу потрібно встановити час початку і кінця руху
        # Надпис "Введіть час початку руху"
        input_number_label = QLabel("Введіть час початку руху")
        input_number_label.setStyleSheet(text_style)
        input_number_label.setFont(text_font5)
        input_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_number_label)

        # Рядок "Час початку руху"
        # Іконка часу
        time_icon_pixmap = QPixmap("../resources/icons/time_icon.svg").scaled(100, 100)
        time_icon_label = QLabel()
        time_icon_label.setPixmap(time_icon_pixmap)

        # Текстове поле для часу
        start_time_line_edit = QLineEdit()
        if self.instance:
            start_time_line_edit.setText(f"{self.instance.start_time}")
        start_time_line_edit.setPlaceholderText("Час початку")
        start_time_line_edit.setStyleSheet(text_line_style)
        start_time_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        start_time_line_edit.setCursor(self.text_cursor)
        start_time_line_edit.enterEvent = self.on_line_edit_enter
        start_time_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з часом початку руху
        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(time_icon_label)
        start_time_layout.addWidget(start_time_line_edit)
        start_time_layout.setSpacing(20)
        start_time_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(start_time_layout)

        # Надпис "Введіть час закінчення руху"
        input_number_label = QLabel("Введіть час закінчення руху")
        input_number_label.setStyleSheet(text_style)
        input_number_label.setFont(text_font5)
        input_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_number_label)

        # Рядок "Час закінчення руху"
        # Іконка часу
        time_icon_pixmap2 = QPixmap("../resources/icons/time_icon.svg").scaled(100, 100)
        time_icon_label2 = QLabel()
        time_icon_label2.setPixmap(time_icon_pixmap2)

        # Текстове поле для часу закінчення руху
        end_time_line_edit = QLineEdit()
        if self.instance:
            end_time_line_edit.setText(f"{self.instance.end_time}")
        end_time_line_edit.setPlaceholderText("Час закінчення")
        end_time_line_edit.setStyleSheet(text_line_style)
        end_time_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        end_time_line_edit.setCursor(self.text_cursor)
        end_time_line_edit.enterEvent = self.on_line_edit_enter
        end_time_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з часом закінчення руху
        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(time_icon_label2)
        end_time_layout.addWidget(end_time_line_edit)
        end_time_layout.setSpacing(20)
        end_time_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(end_time_layout)

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

        # Підключення кнопки до команди

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
