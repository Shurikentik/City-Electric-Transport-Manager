from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt
from styles import *
from AdditionalWindows.ConfirmDialog import ConfirmDialog


# Вікно для водіїв
class DriverWidget(QWidget):
    def __init__(self, main_window, employee):
        super().__init__()
        self.employee = employee
        self.main_window = main_window
        
        self.init_ui()
    
    def init_ui(self):
        # Ініціалізація головної розмітки
        layout = QHBoxLayout()
        
        # Ініціалізація розмітки меню
        menu_layout = QVBoxLayout()

        # Надпис з привітанням
        welcome_label = QLabel(f"Вітаємо, {self.employee.full_name.split()[1]}")
        welcome_label.setStyleSheet(text_style)
        welcome_label.setFont(text_font7)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        menu_layout.addWidget(welcome_label)

        # Кнопка "Налаштування профілю"
        change_profile_button = QPushButton()
        change_profile_button.setIcon(QIcon('../resources/icons/settings_icon.svg'))
        change_profile_button.setText("Налаштування профілю")
        change_profile_button.setIconSize(change_profile_button.sizeHint() * 3)
        change_profile_button.setStyleSheet(button_style)
        change_profile_button.setFont(text_font2)
        change_profile_button.setFixedWidth(1250)
        change_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        change_profile_button.clicked.connect(self.open_profile_settings)
        menu_layout.addWidget(change_profile_button)

        # Підключення обробників подій для зміни курсора
        change_profile_button.enterEvent = self.main_window.on_enter_event
        change_profile_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Повідомити про несправність"
        inform_failure_button = QPushButton()
        inform_failure_button.setIcon(QIcon('../resources/icons/send_icon.svg'))
        inform_failure_button.setText("Повідомити про несправність")
        inform_failure_button.setIconSize(inform_failure_button.sizeHint() * 3)
        inform_failure_button.setStyleSheet(button_style)
        inform_failure_button.setFont(text_font2)
        inform_failure_button.setFixedWidth(1250)
        inform_failure_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        menu_layout.addWidget(inform_failure_button)

        # Підключення обробників подій для зміни курсора
        inform_failure_button.enterEvent = self.main_window.on_enter_event
        inform_failure_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Вийти із облікового запису"
        exit_profile_button = QPushButton()
        exit_profile_button.setIcon(QIcon('../resources/icons/exit_icon.svg'))
        exit_profile_button.setText("Вийти із облікового запису")
        exit_profile_button.setIconSize(exit_profile_button.sizeHint() * 3)
        exit_profile_button.setStyleSheet(button_style)
        exit_profile_button.setFont(text_font2)
        exit_profile_button.setFixedWidth(1250)
        exit_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        exit_profile_button.clicked.connect(self.exit_profile)
        menu_layout.addWidget(exit_profile_button)

        # Підключення обробників подій для зміни курсора
        exit_profile_button.enterEvent = self.main_window.on_enter_event
        exit_profile_button.leaveEvent = self.main_window.on_leave_event

        # Додавання розмітки меню до головної розмітки
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.setSpacing(60)
        layout.addLayout(menu_layout)

        # Додавання картинки водія
        driver_picture_label = QLabel()
        driver_image = QImage("../resources/icons/driver_picture.png")
        # Збільшення зображення
        scaled_image = driver_image.scaled(
            int(driver_image.width() * 2.5),
            int(driver_image.height() * 2.5),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        driver_picture_pixmap = QPixmap(scaled_image)
        driver_picture_label.setPixmap(driver_picture_pixmap)
        layout.addWidget(driver_picture_label)

        self.setLayout(layout)

    # Обробка події при натисканні кнопки "Налаштування профілю"
    def open_profile_settings(self):
        self.main_window.show_profile_settings_widget(employee=self.employee)

    # Обробка події при натисканні кнопки "Вийти із облікового запису"
    def exit_profile(self):
        dialog = ConfirmDialog("Ви впевнені, що хочете вийти?")
        if dialog.exec() == QDialog.Accepted:
            self.main_window.show_login_widget()
