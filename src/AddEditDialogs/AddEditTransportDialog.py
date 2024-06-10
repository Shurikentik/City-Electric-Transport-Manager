from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                               QLineEdit, QPushButton, QMessageBox, QComboBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *
from models.TransportType import TransportType
from models.Employee import Employee
from models.Transport import Transport


# Вікно додавання/зміни транспорту
class AddEditTransportDialog(QDialog):
    def __init__(self, model_class, table_dialog, instance=None, parent=None):
        super().__init__(parent)
        self.model_class = model_class
        self.table_dialog = table_dialog
        self.instance = instance
        self.transport_type_id = None
        self.driver_id = None
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
        title_label = QLabel(f"{"Змінити" if self.instance else "Додати новий"} транспорт")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Якщо транспорт додається, необхідно також обрати тип транспорту
        if not self.instance:
            # Надпис "Оберіть тип електротранспорту"
            transport_type_label = QLabel("Оберіть тип електротранспорту")
            transport_type_label.setStyleSheet(text_style)
            transport_type_label.setFont(text_font5)
            transport_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addWidget(transport_type_label)

            # Рядок для обирання типу електротранспорту
            # Іконка транспорту
            transport_icon_pixmap = QPixmap("../resources/icons/trolleybus_icon.svg").scaled(100, 100)
            transport_icon_label = QLabel()
            transport_icon_label.setPixmap(transport_icon_pixmap)

            # Випадаючий список вибору типу електротранспорту
            transport_type_combobox = QComboBox()
            transport_type_combobox.setStyleSheet(combo_box_style)
            transport_type_combobox.setFont(text_font4)
            transport_type_combobox.setEditable(False)
            transport_type_combobox.setCursor(self.click_cursor)
            transport_type_combobox.setFixedWidth(500)
            transport_type_combobox.setFixedHeight(100)

            # Встановлення елементів списку
            transport_types = TransportType.get_all()
            transport_type_names = [transport_type.transport_name for transport_type in transport_types]
            transport_type_combobox.addItems(transport_type_names)
            transport_type_combobox.setCurrentIndex(-1)

            # Поєднання елементів списку з індексами
            transport_type_index_map = {}
            for i, transport_type in enumerate(transport_types):
                transport_type_index_map[transport_type.transport_name] = i

            # Функція переключення типів транспорту
            def transport_type_combobox_change(text):
                transport_type_index = transport_type_index_map.get(text)
                if transport_type_index is not None:
                    self.transport_type_id = transport_types[transport_type_index].transport_type_id

            # Підключення функції до комбобоксу
            transport_type_combobox.currentTextChanged.connect(transport_type_combobox_change)

            # Функції зміни курсора
            transport_type_combobox.enterEvent = self.on_enter_event
            transport_type_combobox.leaveEvent = self.on_leave_event

            # Об'єднання рядку обирання типу електротранспорту
            pick_transport_type_layout = QHBoxLayout()
            pick_transport_type_layout.addWidget(transport_icon_label)
            pick_transport_type_layout.addWidget(transport_type_combobox)
            pick_transport_type_layout.setSpacing(20)
            pick_transport_type_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addLayout(pick_transport_type_layout)

        # Надпис "Введіть номер транспорту"
        input_number_label = QLabel("Введіть номер транспорту")
        input_number_label.setStyleSheet(text_style)
        input_number_label.setFont(text_font5)
        input_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_number_label)

        # Рядок "Номер транспорту"
        # Іконка номеру
        number_icon_pixmap = QPixmap("../resources/icons/transport_number_icon.svg").scaled(100, 100)
        number_icon_label = QLabel()
        number_icon_label.setPixmap(number_icon_pixmap)

        # Текстове поле для номеру
        number_line_edit = QLineEdit()
        if self.instance:
            number_line_edit.setText(f"{self.instance.transport_number}")
        number_line_edit.setPlaceholderText("Номер")
        number_line_edit.setStyleSheet(text_line_style)
        number_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        number_line_edit.setCursor(self.text_cursor)
        number_line_edit.enterEvent = self.on_line_edit_enter
        number_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з номером транспорту
        number_layout = QHBoxLayout()
        number_layout.addWidget(number_icon_label)
        number_layout.addWidget(number_line_edit)
        number_layout.setSpacing(20)
        number_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(number_layout)

        # Надпис "Призначити водію"
        employee_label = QLabel("Призначити водію")
        employee_label.setStyleSheet(text_style)
        employee_label.setFont(text_font5)
        employee_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(employee_label)

        # Рядок для обирання водія
        # Іконка водія
        driver_icon_pixmap = QPixmap("../resources/icons/human_icon.svg").scaled(100, 100)
        driver_icon_label = QLabel()
        driver_icon_label.setPixmap(driver_icon_pixmap)

        # Випадаючий список вибору водія
        driver_combobox = QComboBox()
        driver_combobox.setStyleSheet(combo_box_style)
        driver_combobox.setFont(text_font4)
        driver_combobox.setEditable(False)
        driver_combobox.setCursor(click_cursor)
        driver_combobox.setFixedWidth(1000)
        driver_combobox.setFixedHeight(100)

        # Встановлення елементів списку
        drivers = Employee.get_all_drivers()
        driver_names = [driver.full_name for driver in drivers]
        driver_combobox.addItems(driver_names)
        driver_combobox.setCurrentIndex(-1)

        # Якщо ми змінюємо елемент, то встановлюємо поточного водія
        if self.instance and self.instance.employee_id:
            current_driver = Employee.get_by_id(self.instance.employee_id)
            if current_driver:
                driver_combobox.setCurrentText(current_driver.full_name)
                self.driver_id = current_driver.employee_id

        # Поєднання елементів списку з індексами
        driver_index_map = {}
        for i, driver in enumerate(drivers):
            driver_index_map[driver.full_name] = i

        # Функція переключення водіїв
        def driver_combobox_change(text):
            driver_index = driver_index_map.get(text)
            if driver_index is not None:
                self.driver_id = drivers[driver_index].employee_id

        # Підключення функції до комбобоксу
        driver_combobox.currentTextChanged.connect(driver_combobox_change)

        # Функції зміни курсора
        driver_combobox.enterEvent = self.on_enter_event
        driver_combobox.leaveEvent = self.on_leave_event

        # Об'єднання рядку обирання водія
        pick_driver_layout = QHBoxLayout()
        pick_driver_layout.addWidget(driver_icon_label)
        pick_driver_layout.addWidget(driver_combobox)
        pick_driver_layout.setSpacing(20)
        pick_driver_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(pick_driver_layout)

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
        def save_transport():
            transport_number = number_line_edit.text().strip()

            if not self.instance:
                # Додавання нового транспорту
                if not self.transport_type_id:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Оберіть тип електротранспорту")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                if not transport_number or transport_number == "Номер":
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть номер транспорту")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                if Transport.is_transport_number_exists(transport_number):
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Транспорт з таким номером вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                try:
                    new_transport = self.model_class(transport_number=transport_number,
                                                     transport_type_id=self.transport_type_id,
                                                     employee_id=self.driver_id,
                                                     availability=True,  # За замовчуванням встановлюємо як доступний
                                                     technical_condition=True)  # За замовчуванням справний
                    new_transport.save()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Транспорт успішно додано")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

            else:
                # Зміна існуючого транспорту
                if transport_number == self.instance.transport_number and self.driver_id == self.instance.employee_id:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Ви нічого не змінили")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                if not transport_number or transport_number == "Номер":
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Введіть номер транспорту")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                if transport_number != self.instance.transport_number and Transport.is_transport_number_exists(
                        transport_number):
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Транспорт з таким номером вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return

                try:
                    self.instance.transport_number = transport_number
                    self.instance.employee_id = self.driver_id
                    self.instance.update()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Транспорт успішно змінено")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

        # Підключення кнопки до команди
        add_edit_button.clicked.connect(save_transport)

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
