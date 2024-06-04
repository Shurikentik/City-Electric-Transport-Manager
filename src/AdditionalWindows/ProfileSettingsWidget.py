from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QIcon
from src.styles import *
from PySide6.QtCore import Qt


# Віджет для налаштування профілю
class ProfileSettingsWidget(QWidget):
    def __init__(self, main_window, employee):
        super().__init__()
        self.employee = employee
        self.main_window = main_window

        layout = QVBoxLayout()

        # Надпис "Прізвище, ім'я, по-батькові"
        full_name_label = QLabel("Прізвище, ім'я, по-батькові")
        full_name_label.setStyleSheet(text_style)
        full_name_label.setFont(text_font2)
        full_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Іконка і текстове поле "ПІБ"
        # Іконка "ПІБ"
        full_name_icon_pixmap = QPixmap("../resources/icons/human_icon.svg").scaled(100, 100)
        full_name_icon_label = QLabel()
        full_name_icon_label.setPixmap(full_name_icon_pixmap)

        # Текстове поле "ПІБ"
        full_name_line_edit = QLineEdit()
        full_name_line_edit.setText(self.employee.full_name)
        full_name_line_edit.setStyleSheet(text_line_style)
        full_name_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        full_name_line_edit.setCursor(text_cursor)
        full_name_line_edit.enterEvent = main_window.on_line_edit_enter
        full_name_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Поєднання іконки і текстового поля в одне ціле
        full_name_layout = QHBoxLayout()
        full_name_layout.addWidget(full_name_icon_label)
        full_name_layout.addWidget(full_name_line_edit)
        full_name_layout.setSpacing(30)
        full_name_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        full_name_widget = QWidget()
        full_name_widget.setLayout(full_name_layout)

        # Надпис "Адреса"
        # Надпис "Прізвище, ім'я, по-батькові
        address_label = QLabel("Адреса")
        address_label.setStyleSheet(text_style)
        address_label.setFont(text_font2)
        address_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Іконка і текстове поле "Адреса"
        # Іконка "Адреса"
        address_icon_pixmap = QPixmap("../resources/icons/home_icon.svg").scaled(100, 100)
        address_icon_label = QLabel()
        address_icon_label.setPixmap(address_icon_pixmap)

        # Текстове поле "Адреса"
        address_line_edit = QLineEdit()
        address_line_edit.setText(self.employee.address)
        address_line_edit.setStyleSheet(text_line_style)
        address_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        address_line_edit.setCursor(text_cursor)
        address_line_edit.enterEvent = main_window.on_line_edit_enter
        address_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Поєднання іконки і текстового поля в одне ціле
        address_layout = QHBoxLayout()
        address_layout.addWidget(address_icon_label)
        address_layout.addWidget(address_line_edit)
        address_layout.setSpacing(30)
        address_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        address_widget = QWidget()
        address_widget.setLayout(address_layout)

        # Надпис "Номер телефону"
        phone_number_label = QLabel("Номер телефону")
        phone_number_label.setStyleSheet(text_style)
        phone_number_label.setFont(text_font2)
        phone_number_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Іконка і текстове поле "Номер телефону"
        # Іконка "Номер телефону"
        phone_number_icon_pixmap = QPixmap("../resources/icons/phone_icon.svg").scaled(100, 100)
        phone_number_icon_label = QLabel()
        phone_number_icon_label.setPixmap(phone_number_icon_pixmap)

        # Текстове поле "Номер телефону"
        phone_number_line_edit = QLineEdit()
        phone_number_line_edit.setText(self.employee.phone_number)
        phone_number_line_edit.setStyleSheet(text_line_style)
        phone_number_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        phone_number_line_edit.setCursor(text_cursor)
        phone_number_line_edit.enterEvent = main_window.on_line_edit_enter
        phone_number_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Поєднання іконки і текстового поля в одне ціле
        phone_number_layout = QHBoxLayout()
        phone_number_layout.addWidget(phone_number_icon_label)
        phone_number_layout.addWidget(phone_number_line_edit)
        phone_number_layout.setSpacing(30)
        phone_number_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        phone_number_widget = QWidget()
        phone_number_widget.setLayout(phone_number_layout)

        # Кнопка "Оновити дані профілю"
        update_profile_button = QPushButton()
        update_profile_button.setIcon(QIcon("../resources/icons/wrench_icon.svg"))
        update_profile_button.setText("Оновити дані профілю")
        update_profile_button.setIconSize(update_profile_button.sizeHint() * 3)
        update_profile_button.setStyleSheet(button_style)
        update_profile_button.setFont(text_font2)
        update_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        update_profile_button.clicked.connect(self.update_profile)

        # Підключення обробників подій для зміни курсора
        update_profile_button.enterEvent = main_window.on_enter_event
        update_profile_button.leaveEvent = main_window.on_leave_event

        # Кнопки "Змінити пароль" та "Вийти з налаштувань"
        # Кнопка "Змінити пароль"
        update_password_button = QPushButton()
        update_password_button.setIcon(QIcon('../resources/icons/lock_icon.svg'))
        update_password_button.setText("Змінити пароль")
        update_password_button.setIconSize(update_password_button.sizeHint() * 3)
        update_password_button.setStyleSheet(button_style)
        update_password_button.setFont(text_font2)
        update_password_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        update_password_button.clicked.connect(self.update_password_open)

        # Підключення обробників подій для зміни курсора
        update_password_button.enterEvent = main_window.on_enter_event
        update_password_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Вийти з налаштувань"
        exit_settings_button = QPushButton()
        exit_settings_button.setIcon(QIcon('../resources/icons/cancel_icon.svg'))
        exit_settings_button.setText("Вийти з налаштувань")
        exit_settings_button.setIconSize(exit_settings_button.sizeHint() * 3)
        exit_settings_button.setStyleSheet(button_style)
        exit_settings_button.setFont(text_font2)
        exit_settings_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        exit_settings_button.clicked.connect(self.exit_settings_widget)

        # Підключення обробників подій для зміни курсора
        exit_settings_button.enterEvent = main_window.on_enter_event
        exit_settings_button.leaveEvent = main_window.on_leave_event

        # Додавання усіх елементів до віджету
        layout.addWidget(full_name_label)
        layout.addWidget(full_name_widget)
        layout.addWidget(address_label)
        layout.addWidget(address_widget)
        layout.addWidget(phone_number_label)
        layout.addWidget(phone_number_widget)
        layout.addWidget(update_profile_button)
        layout.addWidget(update_password_button)
        layout.addWidget(exit_settings_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        self.setLayout(layout)

    # Обробка події натискання кнопки "Оновити профіль"
    def update_profile(self):
        print()

    # Обробка події натискання кнопки "Змінити пароль"
    def update_password_open(self):
        print()

    # Обробка події натискання кнопки "Вийти з налаштувань"
    def exit_settings_widget(self):
        self.main_window.show_cashier_widget(employee=self.employee)
