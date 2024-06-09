from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,
                               QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from src.styles import *
from models.Employee import Employee


# Вікно додавання співробітника
class AddEmployeeDialog(QDialog):
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
        title_label = QLabel("Додати нового користувача")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Надпис "Введіть ПІБ співробітника"
        input_full_name_label = QLabel("Введіть ПІБ співробітника")
        input_full_name_label.setStyleSheet(text_style)
        input_full_name_label.setFont(text_font5)
        input_full_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_full_name_label)

        # Рядок "ПІБ співробітника"
        # Іконка людини
        human_icon_pixmap = QPixmap("../resources/icons/human_icon.svg").scaled(100, 100)
        human_icon_label = QLabel()
        human_icon_label.setPixmap(human_icon_pixmap)

        # Текстове поле для ПІБ
        full_name_line_edit = QLineEdit()
        full_name_line_edit.setPlaceholderText("ПІБ співробітника")
        full_name_line_edit.setStyleSheet(text_line_style)
        full_name_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        full_name_line_edit.setCursor(self.text_cursor)
        full_name_line_edit.enterEvent = self.on_line_edit_enter
        full_name_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з ПІБ співробітника
        full_name_layout = QHBoxLayout()
        full_name_layout.addWidget(human_icon_label)
        full_name_layout.addWidget(full_name_line_edit)
        full_name_layout.setSpacing(20)
        full_name_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(full_name_layout)

        # Надпис "Оберіть посаду співробітника"
        employee_position_label = QLabel("Оберіть посаду співробітника")
        employee_position_label.setStyleSheet(text_style)
        employee_position_label.setFont(text_font5)
        employee_position_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(employee_position_label)

        # Рядок для обирання посади
        # Іконка співробітника
        employee_icon_pixmap = QPixmap("../resources/icons/employee_icon.svg").scaled(100, 100)
        employee_icon_label = QLabel()
        employee_icon_label.setPixmap(employee_icon_pixmap)

        # Випадаючий список вибору посади
        employee_position_combobox = QComboBox()
        employee_position_combobox.setStyleSheet(combo_box_style)
        employee_position_combobox.setFont(text_font4)
        employee_position_combobox.setEditable(False)
        employee_position_combobox.setCursor(self.click_cursor)
        employee_position_combobox.setFixedWidth(600)
        employee_position_combobox.setFixedHeight(100)

        # Додавання елементів до комбобоксу
        employee_position_combobox.addItems(["Касир", "Водій", "Диспетчер", "Адміністратор"])
        employee_position_combobox.setCurrentIndex(-1)

        # Функції зміни курсора
        employee_position_combobox.enterEvent = self.on_enter_event
        employee_position_combobox.leaveEvent = self.on_leave_event

        # Об'єднання рядку обирання посади
        pick_employee_position_layout = QHBoxLayout()
        pick_employee_position_layout.addWidget(employee_icon_label)
        pick_employee_position_layout.addWidget(employee_position_combobox)
        pick_employee_position_layout.setSpacing(20)
        pick_employee_position_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(pick_employee_position_layout)

        # Надпис "Введіть адресу проживання співробітника"
        input_address_label = QLabel("Введіть адресу проживання співробітника")
        input_address_label.setStyleSheet(text_style)
        input_address_label.setFont(text_font5)
        input_address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_address_label)

        # Рядок "Адреса"
        # Іконка будинку
        house_icon_pixmap = QPixmap("../resources/icons/home_icon.svg").scaled(100, 100)
        house_icon_label = QLabel()
        house_icon_label.setPixmap(house_icon_pixmap)

        # Текстове поле для адреси співробітника
        address_line_edit = QLineEdit()
        address_line_edit.setPlaceholderText("Адреса")
        address_line_edit.setStyleSheet(text_line_style)
        address_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        address_line_edit.setCursor(self.text_cursor)
        address_line_edit.enterEvent = self.on_line_edit_enter
        address_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з адресою
        address_layout = QHBoxLayout()
        address_layout.addWidget(house_icon_label)
        address_layout.addWidget(address_line_edit)
        address_layout.setSpacing(20)
        address_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(address_layout)

        # Надпис "Введіть номер телефону співробітника"
        input_phone_number_label = QLabel("Введіть номер телефону співробітника")
        input_phone_number_label.setStyleSheet(text_style)
        input_phone_number_label.setFont(text_font5)
        input_phone_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_phone_number_label)

        # Рядок "Номер телефону"
        # Іконка телефону
        phone_icon_pixmap = QPixmap("../resources/icons/phone_icon.svg").scaled(100, 100)
        phone_icon_label = QLabel()
        phone_icon_label.setPixmap(phone_icon_pixmap)

        # Текстове поле для номеру телефону
        phone_number_line_edit = QLineEdit()
        phone_number_line_edit.setPlaceholderText("Номер телефону")
        phone_number_line_edit.setStyleSheet(text_line_style)
        phone_number_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        phone_number_line_edit.setCursor(self.text_cursor)
        phone_number_line_edit.enterEvent = self.on_line_edit_enter
        phone_number_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з номером телефону
        phone_number_layout = QHBoxLayout()
        phone_number_layout.addWidget(phone_icon_label)
        phone_number_layout.addWidget(phone_number_line_edit)
        phone_number_layout.setSpacing(20)
        phone_number_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(phone_number_layout)

        # Надпис "Введіть логін співробітника"
        input_login_label = QLabel("Введіть логін співробітника")
        input_login_label.setStyleSheet(text_style)
        input_login_label.setFont(text_font5)
        input_login_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_login_label)

        # Рядок "Логін"
        # Іконка логіну
        login_icon_pixmap = QPixmap("../resources/icons/user_login_icon.svg").scaled(100, 100)
        login_icon_label = QLabel()
        login_icon_label.setPixmap(login_icon_pixmap)

        # Текстове поле для логіну
        login_line_edit = QLineEdit()
        login_line_edit.setPlaceholderText("Логін")
        login_line_edit.setStyleSheet(text_line_style)
        login_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        login_line_edit.setCursor(self.text_cursor)
        login_line_edit.enterEvent = self.on_line_edit_enter
        login_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з логіном
        login_layout = QHBoxLayout()
        login_layout.addWidget(login_icon_label)
        login_layout.addWidget(login_line_edit)
        login_layout.setSpacing(20)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(login_layout)

        # Надпис "Придумайте пароль для акаунту співробітника"
        input_password_label = QLabel("Придумайте пароль для акаунту співробітника")
        input_password_label.setStyleSheet(text_style)
        input_password_label.setFont(text_font5)
        input_password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_password_label)

        # Рядок "Пароль"
        # Іконка паролю
        lock_icon_pixmap = QPixmap("../resources/icons/lock_icon.svg").scaled(100, 100)
        lock_icon_label = QLabel()
        lock_icon_label.setPixmap(lock_icon_pixmap)

        # Текстове поле для паролю
        password_line_edit = QLineEdit()
        password_line_edit.setPlaceholderText("Пароль")
        password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_line_edit.setStyleSheet(text_line_style)
        password_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        password_line_edit.setCursor(self.text_cursor)
        password_line_edit.enterEvent = self.on_line_edit_enter
        password_line_edit.leaveEvent = self.on_line_edit_leave

        # Кнопка для приховання пароля
        eye_icon = QPushButton()
        eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
        eye_icon.setFixedSize(100, 100)
        eye_icon.setIconSize(QSize(100, 100))
        eye_icon.setStyleSheet("""
                            QPushButton {
                                border: none;
                                background-color: transparent;
                            }     
                        """)

        # Функція для приховання/відкриття пароля
        def toggle_password_visibility():
            if password_line_edit.echoMode() == QLineEdit.EchoMode.Normal:
                password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
            else:
                password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                eye_icon.setIcon(QIcon("../resources/icons/eye_open_icon.svg").pixmap(200, 200))

        eye_icon.clicked.connect(toggle_password_visibility)

        # Підключення обробників подій для зміни курсора
        eye_icon.enterEvent = self.on_enter_event
        eye_icon.leaveEvent = self.on_leave_event

        # Збираємо три елементи в один рядок
        password_layout = QHBoxLayout()
        password_layout.addWidget(lock_icon_label)
        password_layout.addWidget(password_line_edit)
        password_layout.addWidget(eye_icon)
        password_layout.setSpacing(20)
        password_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(password_layout)

        # Додавання кнопок
        button_layout = QHBoxLayout()

        # Кнопка "Додати"
        add_button = QPushButton()
        add_button.setIcon(QIcon("../resources/icons/add_icon.svg"))
        add_button.setText("Додати")
        add_button.setIconSize(add_button.sizeHint() * 3)
        add_button.setStyleSheet(button_style)
        add_button.setFont(text_font2)
        add_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        add_button.setFixedWidth(550)

        # Підключення обробників подій для зміни курсора
        add_button.enterEvent = self.on_enter_event
        add_button.leaveEvent = self.on_leave_event

        add_button_layout = QHBoxLayout()
        add_button_layout.addWidget(add_button)
        add_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        add_button_widget = QWidget()
        add_button_widget.setLayout(add_button_layout)

        # Обробка події натискання кнопки "Додати"
        def add_employee():
            full_name = full_name_line_edit.text().strip()
            employee_position = employee_position_combobox.currentText().strip()
            address = address_line_edit.text().strip()
            phone_number = phone_number_line_edit.text().strip()
            login = login_line_edit.text().strip()
            password = password_line_edit.text().strip()

            # Перевірка заповненості полів
            if ((not full_name or full_name == "ПІБ співробітника") or (not employee_position) or
                    (not address or address == "Адреса") or (not phone_number or phone_number == "Номер телефону") or
                    (not login or login == "Логін") or (not password or password == "Пароль")):
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Всі поля мають бути заповнені")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            # Перевірка унікальності логіну
            if not Employee.is_login_unique(login):
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Користувач з таким логіном вже існує")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            # Додавання нового співробітника
            try:
                new_employee = Employee(
                    full_name=full_name,
                    employee_position=employee_position,
                    address=address,
                    phone_number=phone_number,
                    login=login,
                    employee_password=password
                )
                new_employee.save()
                msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Співробітника успішно додано")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                self.close()
            except Exception as e:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()

        # Підключення команди до кнопки
        add_button.clicked.connect(add_employee)

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

        button_layout.addWidget(add_button_widget)
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
