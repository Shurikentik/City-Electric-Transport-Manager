from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                               QLineEdit, QPushButton, QMessageBox, QComboBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *
from models.TransportType import TransportType
from models.ValidityType import ValidityType


# Вікно додавання/зміни тарифу
class AddEditTariffDialog(QDialog):
    def __init__(self, model_class, table_dialog, instance=None, parent=None):
        super().__init__(parent)
        self.model_class = model_class
        self.table_dialog = table_dialog
        self.instance = instance
        self.transport_type_id = None
        self.validity_type_id = None
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
        title_label = QLabel(f"{"Змінити" if self.instance else "Додати новий"} тариф")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Якщо тариф додається, необхідно також обрати тип транспорту і терміну чинності
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

            # Надпис "Оберіть тип чинності квитка"
            validity_type_label = QLabel("Оберіть тип чинності квитка")
            validity_type_label.setStyleSheet(text_style)
            validity_type_label.setFont(text_font5)
            validity_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(validity_type_label)

            # Рядок для обирання типу чинності квитка
            # Іконка часу
            validity_icon_pixmap = QPixmap("../resources/icons/time_icon.svg").scaled(100, 100)
            validity_icon_label = QLabel()
            validity_icon_label.setPixmap(validity_icon_pixmap)

            # Випадаючий список вибору типу чинності квитка
            validity_type_combobox = QComboBox()
            validity_type_combobox.setStyleSheet(combo_box_style)
            validity_type_combobox.setFont(text_font4)
            validity_type_combobox.setEditable(False)
            validity_type_combobox.setCursor(click_cursor)
            validity_type_combobox.setFixedWidth(500)
            validity_type_combobox.setFixedHeight(100)

            # Встановлення елементів списку
            validity_types = ValidityType.get_all()
            validity_type_names = [validity_type.validity_name for validity_type in validity_types]
            validity_type_combobox.addItems(validity_type_names)
            validity_type_combobox.setCurrentIndex(-1)

            # Поєднання елементів списку з індексами
            validity_type_index_map = {}
            for i, validity_type in enumerate(validity_types):
                validity_type_index_map[validity_type.validity_name] = i

            # Функція переключення типів терміну чинності
            def validity_type_combobox_change(text):
                validity_type_index = validity_type_index_map.get(text)
                if validity_type_index is not None:
                    self.validity_type_id = validity_types[validity_type_index].validity_type_id

            # Підключення функції до комбобоксу
            validity_type_combobox.currentTextChanged.connect(validity_type_combobox_change)

            # Функції зміни курсора
            validity_type_combobox.enterEvent = self.on_enter_event
            validity_type_combobox.leaveEvent = self.on_leave_event

            # Об'єднання рядку обирання типу чинності квитка
            pick_validity_type_layout = QHBoxLayout()
            pick_validity_type_layout.addWidget(validity_icon_label)
            pick_validity_type_layout.addWidget(validity_type_combobox)
            pick_validity_type_layout.setSpacing(20)
            pick_validity_type_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout.addLayout(pick_validity_type_layout)

        # Надпис "Введіть ціну квитка"
        input_price_label = QLabel("Введіть ціну квитка")
        input_price_label.setStyleSheet(text_style)
        input_price_label.setFont(text_font5)
        input_price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_price_label)

        # Рядок "Ціна"
        # Іконка монет
        coins_icon_pixmap = QPixmap("../resources/icons/coins_icon.svg").scaled(100, 100)
        coins_icon_label = QLabel()
        coins_icon_label.setPixmap(coins_icon_pixmap)

        # Текстове поле для ціни
        price_line_edit = QLineEdit()
        if self.instance:
            price_line_edit.setText(f"{self.instance.ticket_price}")
        price_line_edit.setPlaceholderText("Ціна квитка")
        price_line_edit.setStyleSheet(text_line_style)
        price_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        price_line_edit.setCursor(self.text_cursor)
        price_line_edit.enterEvent = self.on_line_edit_enter
        price_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з ціною
        price_layout = QHBoxLayout()
        price_layout.addWidget(coins_icon_label)
        price_layout.addWidget(price_line_edit)
        price_layout.setSpacing(20)
        price_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(price_layout)

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
        def save_tariff():
            # Перевірка формату вказання ціни квитка
            try:
                ticket_price = float(price_line_edit.text().strip())
            except ValueError:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                      "Ціну квитка вказано у неправильному форматі")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return
            # Перевірка, чи є ціна більшою за 0
            if not ticket_price > 0:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                      "Ціна квитка має бути більшою за 0")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            # Додавання нового об'єкта
            if not self.instance:
                # Перевірка, чи вибраний тип електротранспорту і терміну чинності
                if not (self.transport_type_id and self.validity_type_id):
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Ви не обрали тип електротранспорту і терміну чинності для створення тарифу")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                # Перевірка наявності тарифу з таким же типом транспорту та терміном чинності
                existing_tariff = self.model_class.get_tariff_by_transport_and_validity(self.transport_type_id,
                                                                                        self.validity_type_id)
                if existing_tariff:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Тариф з таким типом електротранспорту і терміном чинності вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    new_tariff = self.model_class(ticket_price=ticket_price, transport_type_id=self.transport_type_id,
                                                  validity_type_id=self.validity_type_id)
                    new_tariff.save()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Тариф успішно додано")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

            # Зміна існуючого об'єкта
            else:
                if ticket_price == self.instance.ticket_price:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Ви не змінили ціну квитка")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    self.instance.ticket_price = ticket_price
                    self.instance.update()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Тариф успішно змінено")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

        # Підключення кнопки до команди
        add_edit_button.clicked.connect(save_tariff)

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
