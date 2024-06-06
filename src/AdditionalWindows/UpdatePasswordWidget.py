from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PySide6.QtGui import QIcon, QImage
from src.styles import *
from PySide6.QtCore import Qt, QSize


# Віджет для зміни пароля
class UpdatePasswordWidget(QWidget):
    def __init__(self, main_window, employee):
        super().__init__()
        self.employee = employee
        self.main_window = main_window

        # Ініціалізація головної розмітки
        main_layout = QHBoxLayout()

        # Ініціалізація розмітки зміни паролю
        update_password_layout = QVBoxLayout()

        # Надпис "Зміна пароля"
        updating_label = QLabel("Зміна паролю")
        updating_label.setStyleSheet(text_style)
        updating_label.setFont(text_font5)
        updating_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Надпис "Введіть старий пароль"
        old_password_label = QLabel("Введіть старий пароль")
        old_password_label.setStyleSheet(text_style)
        old_password_label.setFont(text_font5)
        old_password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок для введення старого паролю
        # Іконка "Пароль"
        old_password_icon_pixmap = QPixmap("../resources/icons/lock_icon.svg").scaled(100, 100)
        old_password_icon_label = QLabel()
        old_password_icon_label.setPixmap(old_password_icon_pixmap)

        # Текстове поле для паролю
        input_old_password_line_edit = QLineEdit()
        input_old_password_line_edit.setPlaceholderText("Старий пароль")
        input_old_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        input_old_password_line_edit.setStyleSheet(text_line_style)
        input_old_password_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        input_old_password_line_edit.setCursor(main_window.text_cursor)
        input_old_password_line_edit.enterEvent = main_window.on_line_edit_enter
        input_old_password_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Кнопка для приховання пароля
        old_eye_icon = QPushButton()
        old_eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
        old_eye_icon.setFixedSize(100, 100)
        old_eye_icon.setIconSize(QSize(100, 100))
        old_eye_icon.setStyleSheet("""
                            QPushButton {
                                border: none;
                                background-color: transparent;
                            }     
                        """)

        # Функція для приховання/відкриття пароля
        def toggle_old_password_visibility():
            if input_old_password_line_edit.echoMode() == QLineEdit.EchoMode.Normal:
                input_old_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                old_eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
            else:
                input_old_password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                old_eye_icon.setIcon(QIcon("../resources/icons/eye_open_icon.svg").pixmap(200, 200))

        old_eye_icon.clicked.connect(toggle_old_password_visibility)

        # Підключення обробників подій для зміни курсора
        old_eye_icon.enterEvent = main_window.on_enter_event
        old_eye_icon.leaveEvent = main_window.on_leave_event

        # Збираємо три елементи в один рядок
        old_password_layout = QHBoxLayout()
        old_password_layout.addWidget(old_password_icon_label)
        old_password_layout.addWidget(input_old_password_line_edit)
        old_password_layout.addWidget(old_eye_icon)
        old_password_layout.setSpacing(30)
        old_password_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        old_password_widget = QWidget()
        old_password_widget.setLayout(old_password_layout)

        # Надпис "Введіть новий пароль"
        new_password_label = QLabel("Введіть новий пароль")
        new_password_label.setStyleSheet(text_style)
        new_password_label.setFont(text_font5)
        new_password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок для введення нового паролю
        # Іконка "Пароль"
        new_password_icon_pixmap = QPixmap("../resources/icons/lock_icon.svg").scaled(100, 100)
        new_password_icon_label = QLabel()
        new_password_icon_label.setPixmap(new_password_icon_pixmap)

        # Текстове поле для паролю
        input_new_password_line_edit = QLineEdit()
        input_new_password_line_edit.setPlaceholderText("Новий пароль")
        input_new_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        input_new_password_line_edit.setStyleSheet(text_line_style)
        input_new_password_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        input_new_password_line_edit.setCursor(main_window.text_cursor)
        input_new_password_line_edit.enterEvent = main_window.on_line_edit_enter
        input_new_password_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Кнопка для приховання пароля
        new_eye_icon = QPushButton()
        new_eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
        new_eye_icon.setFixedSize(100, 100)
        new_eye_icon.setIconSize(QSize(100, 100))
        new_eye_icon.setStyleSheet("""
                            QPushButton {
                                border: none;
                                background-color: transparent;
                            }     
                        """)

        # Функція для приховання/відкриття пароля
        def toggle_new_password_visibility():
            if input_new_password_line_edit.echoMode() == QLineEdit.EchoMode.Normal:
                input_new_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                new_eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
            else:
                input_new_password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                new_eye_icon.setIcon(QIcon("../resources/icons/eye_open_icon.svg").pixmap(200, 200))

        new_eye_icon.clicked.connect(toggle_new_password_visibility)

        # Підключення обробників подій для зміни курсора
        new_eye_icon.enterEvent = main_window.on_enter_event
        new_eye_icon.leaveEvent = main_window.on_leave_event

        # Збираємо три елементи в один рядок
        new_password_layout = QHBoxLayout()
        new_password_layout.addWidget(new_password_icon_label)
        new_password_layout.addWidget(input_new_password_line_edit)
        new_password_layout.addWidget(new_eye_icon)
        new_password_layout.setSpacing(30)
        new_password_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        new_password_widget = QWidget()
        new_password_widget.setLayout(new_password_layout)

        # Кнопка "Змінити пароль"
        update_password_button = QPushButton()
        update_password_button.setIcon(QIcon("../resources/icons/wrench_icon.svg"))
        update_password_button.setText("Змінити пароль")
        update_password_button.setIconSize(update_password_button.sizeHint() * 3)
        update_password_button.setStyleSheet(button_style)
        update_password_button.setFont(text_font5)
        update_password_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Функція обробки події натискання кнопки "Змінити пароль"
        def update_password_button_clicked():
            # Збираємо дані з текстових полів
            old_password = input_old_password_line_edit.text().strip()
            new_password = input_new_password_line_edit.text().strip()

            # Якщо користувач не заповнив усі поля, вилізає повідомлення з відповідною помилкою
            if old_password == "Старий пароль" or new_password == "Новий пароль" or not old_password or not new_password:
                QMessageBox.critical(self, "Помилка", "Будь ласка, заповніть усі поля.")
                return

            # Оновлення паролю
            try:
                self.employee.update_password(old_password, new_password)
                QMessageBox.information(self, "Пароль змінено", "Пароль успішно змінено!")
            except Exception as e:
                QMessageBox.critical(self, "Помилка зміни", f"Помилка при зміні паролю: {e}")

        update_password_button.clicked.connect(update_password_button_clicked)

        # Підключення обробників подій для зміни курсора
        update_password_button.enterEvent = main_window.on_enter_event
        update_password_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Відмінити"
        exit_updating_password_button = QPushButton()
        exit_updating_password_button.setIcon(QIcon('../resources/icons/cancel_icon.svg'))
        exit_updating_password_button.setText("Відмінити")
        exit_updating_password_button.setIconSize(exit_updating_password_button.sizeHint() * 3)
        exit_updating_password_button.setStyleSheet(button_style)
        exit_updating_password_button.setFont(text_font5)
        exit_updating_password_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        exit_updating_password_button.clicked.connect(self.exit_updating_password_widget)

        # Підключення обробників подій для зміни курсора
        exit_updating_password_button.enterEvent = main_window.on_enter_event
        exit_updating_password_button.leaveEvent = main_window.on_leave_event

        update_password_layout.addWidget(updating_label)
        update_password_layout.addWidget(old_password_label)
        update_password_layout.addWidget(old_password_widget)
        update_password_layout.addWidget(new_password_label)
        update_password_layout.addWidget(new_password_widget)
        update_password_layout.addWidget(update_password_button)
        update_password_layout.addWidget(exit_updating_password_button)
        update_password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        update_password_layout.setSpacing(23)

        # Створення віджету для розмітки налаштувань
        update_password_widget = QWidget()
        update_password_widget.setLayout(update_password_layout)

        # Додавання картинки
        picture_label = QLabel()
        picture_image = QImage("../resources/icons/profile_settings.png")

        # Збільшення зображення
        scaled_image = picture_image.scaled(
            int(picture_image.width() * 2.5),
            int(picture_image.height() * 2.5),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        tram_picture_pixmap = QPixmap(scaled_image)
        picture_label.setPixmap(tram_picture_pixmap)

        # Додавання до головної розмітки налаштувань і картинки
        main_layout.addWidget(update_password_widget)
        main_layout.addWidget(picture_label)

        self.setLayout(main_layout)

    # Обробка події натискання кнопки "Відмінити"
    def exit_updating_password_widget(self):
        self.main_window.show_profile_settings_widget(employee=self.employee)
