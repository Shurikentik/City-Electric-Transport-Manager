from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt, QSize
from models.Employee import Employee


class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # Титульний надпис
        # Завантаження зображення
        tram_pixmap = QPixmap("../resources/icons/tram_icon.svg").scaled(130, 130)

        # Створення лейбла з іконкою
        title_icon_label = QLabel()
        title_icon_label.setPixmap(tram_pixmap)

        # Створення текстового лейбла
        title_text_label = QLabel("City Electric Transport Manager")
        title_text_label.setStyleSheet("""
                    background-color:none;
                    color:white;
                """)
        title_text_label_font = QFont()
        title_text_label_font.setFamily("Sitka Banner")
        title_text_label_font.setPointSize(100)
        title_text_label_font.setBold(True)
        title_text_label.setFont(title_text_label_font)

        # Компонування лейблів у горизонтальний макет
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_icon_label)
        title_layout.addWidget(title_text_label)
        title_layout.setSpacing(30)

        # Розміщення макету у верхній частині вікна посередині
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Створення title_widget
        title_widget = QWidget()
        title_widget.setLayout(title_layout)
        title_widget.setStyleSheet("max-height: 200px;")

        # Додавання елементів для вікна входу

        # Надпис "Увійти"
        sign_in_label = QLabel("Вхід у систему")
        sign_in_label.setStyleSheet("""
                    background-color:none;
                    color:white;
                    font-size: 72px;
                """)
        sign_in_label_font = QFont()
        sign_in_label_font.setFamily("appetite")
        sign_in_label_font.setPointSize(100)
        sign_in_label_font.setItalic(True)
        sign_in_label.setFont(sign_in_label_font)

        sign_in_label_layout = QHBoxLayout()
        sign_in_label_layout.addWidget(sign_in_label)
        sign_in_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        sign_in_label_widget = QWidget()
        sign_in_label_widget.setLayout(sign_in_label_layout)

        # Надпис "Введіть ваш логін"
        input_login_label = QLabel("Введіть ваш логін:")
        input_login_label.setStyleSheet("""
                    background-color:none;
                    color:white;
                    font-size: 52px;
                """)
        input_login_label_font = QFont()
        input_login_label_font.setFamily("appetite")
        input_login_label_font.setPointSize(100)
        input_login_label.setFont(input_login_label_font)

        input_login_label_layout = QHBoxLayout()
        input_login_label_layout.addWidget(input_login_label)
        input_login_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        input_login_label_widget = QWidget()
        input_login_label_widget.setLayout(input_login_label_layout)

        # Іконка "Логін" і текстове поле

        # Іконка "Логін"
        login_icon_pixmap = QPixmap("../resources/icons/user_login_icon.svg").scaled(100, 100)
        login_icon_label = QLabel()
        login_icon_label.setPixmap(login_icon_pixmap)

        # Текстове поле для логіну
        input_login_line_edit = QLineEdit()

        input_login_line_edit.setPlaceholderText("Логін")

        input_login_line_edit.setStyleSheet("""
                    border-radius: 7px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: white;
                    color: white;
                    background-color: rgba(255, 255, 255, 0.25);
                """)

        input_login_line_edit_font = QFont()
        input_login_line_edit_font.setFamily("Sitka Banner")
        input_login_line_edit_font.setPointSize(50)
        input_login_line_edit.setFont(input_login_line_edit_font)

        # Підключення обробників подій для зміни курсора
        input_login_line_edit.setCursor(main_window.text_cursor)
        input_login_line_edit.enterEvent = main_window.on_line_edit_enter
        input_login_line_edit.leaveEvent = main_window.on_line_edit_leave

        login_layout = QHBoxLayout()
        login_layout.addWidget(login_icon_label)
        login_layout.addWidget(input_login_line_edit)
        login_layout.setSpacing(30)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        login_widget = QWidget()
        login_widget.setLayout(login_layout)

        # Надпис "Введіть ваш пароль"
        input_password_label = QLabel("Введіть ваш пароль:")
        input_password_label.setStyleSheet("""
                           background-color:none;
                           color:white;
                           font-size: 52px;
                       """)
        input_password_label_font = QFont()
        input_password_label_font.setFamily("appetite")
        input_password_label_font.setPointSize(100)
        input_password_label.setFont(input_password_label_font)

        input_password_label_layout = QHBoxLayout()
        input_password_label_layout.addWidget(input_password_label)
        input_password_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        input_password_label_widget = QWidget()
        input_password_label_widget.setLayout(input_password_label_layout)

        # Іконка "Пароль" і текстове поле і кнопка приховання пароля

        # Іконка "Пароль"
        password_icon_pixmap = QPixmap("../resources/icons/lock_icon.svg").scaled(100, 100)
        password_icon_label = QLabel()
        password_icon_label.setPixmap(password_icon_pixmap)

        # Текстове поле для паролю
        input_password_line_edit = QLineEdit()
        input_password_line_edit.setPlaceholderText("Пароль")
        input_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        input_password_line_edit.setStyleSheet("""
                            border-radius: 7px;
                            border-width: 1px;
                            border-style: solid;
                            border-color: white;
                            color: white;
                            background-color: rgba(255, 255, 255, 0.25);
                        """)

        input_password_line_edit_font = QFont()
        input_password_line_edit_font.setFamily("Sitka Banner")
        input_password_line_edit_font.setPointSize(50)
        input_password_line_edit.setFont(input_password_line_edit_font)

        # Підключення обробників подій для зміни курсора
        input_password_line_edit.setCursor(main_window.text_cursor)
        input_password_line_edit.enterEvent = main_window.on_line_edit_enter
        input_password_line_edit.leaveEvent = main_window.on_line_edit_leave

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
            if input_password_line_edit.echoMode() == QLineEdit.EchoMode.Normal:
                input_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                eye_icon.setIcon(QIcon("../resources/icons/eye_closed_icon.svg").pixmap(200, 200))
            else:
                input_password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                eye_icon.setIcon(QIcon("../resources/icons/eye_open_icon.svg").pixmap(200, 200))

        eye_icon.clicked.connect(toggle_password_visibility)

        # Підключення обробників подій для зміни курсора
        eye_icon.enterEvent = main_window.on_enter_event
        eye_icon.leaveEvent = main_window.on_leave_event

        # Збираємо три елементи в один рядок
        password_layout = QHBoxLayout()
        password_layout.addWidget(password_icon_label)
        password_layout.addWidget(input_password_line_edit)
        password_layout.addWidget(eye_icon)
        password_layout.setSpacing(30)
        password_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        password_widget = QWidget()
        password_widget.setLayout(password_layout)

        # Кнопка "Увійти"
        sign_in_button = QPushButton("Увійти")
        sign_in_button.setFixedSize(300, 100)
        sign_in_button.setStyleSheet("""
                    QPushButton {
                        border-color: blue;
                           border-style: solid;
                           border-width: 2px;
                           border-radius: 15px;
                           color: white;
                           background-color: qlineargradient(
                               spread:pad, x1:0.3525, y1:0.472, x2:0.971591, y2:0.96, 
                               stop:0 rgba(0, 81, 168, 255), 
                               stop:1 rgba(147, 113, 255, 255)
                           );
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 30);
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 100);
                    }
                """)
        sign_in_button_font = QFont()
        sign_in_button_font.setFamily("appetite")
        sign_in_button_font.setPointSize(52)
        sign_in_button.setFont(sign_in_button_font)

        # Підключення обробників подій для зміни курсора
        sign_in_button.enterEvent = main_window.on_enter_event
        sign_in_button.leaveEvent = main_window.on_leave_event

        # Функція обробки події входу
        def sign_in_button_clicked():
            # Збираємо введені логін та пароль
            login = input_login_line_edit.text().strip()
            password = input_password_line_edit.text().strip()

            # Якщо користувач не заповнив усі поля, вилізає повідомлення з відповідною помилкою
            if login == "Логін" or password == "Пароль" or not login or not password:
                QMessageBox.critical(self, "Помилка", "Будь ласка, заповніть усі поля.")
                return

            # Верифікація користувача та визначення його посади
            employee = Employee.verify_login_password(login, password)
            if employee:
                employee_position = employee.employee_position
                if employee_position == "Адміністратор":
                    main_window.show_admin_widget(employee=employee)
                elif employee_position == "Диспетчер":
                    main_window.show_dispatcher_widget(employee=employee)
                elif employee_position == "Водій":
                    main_window.show_driver_widget(employee=employee)
                elif employee_position == "Касир":
                    main_window.show_cashier_widget(employee=employee)
                else:
                    QMessageBox.critical(self, "Помилка", "Невідома посада користувача.")
            else:
                QMessageBox.critical(self, "Помилка", "Невірний логін або пароль.")

        # Підключення кнопки до відповідної функції
        sign_in_button.clicked.connect(sign_in_button_clicked)

        sign_in_button_layout = QHBoxLayout()
        sign_in_button_layout.addWidget(sign_in_button)
        sign_in_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        sign_in_button_widget = QWidget()
        sign_in_button_widget.setLayout(sign_in_button_layout)

        # Створення розмітки sign_in_layout
        sign_in_layout = QVBoxLayout()
        sign_in_layout.addWidget(sign_in_label_widget)
        sign_in_layout.addWidget(input_login_label_widget)
        sign_in_layout.addWidget(login_widget)
        sign_in_layout.addWidget(input_password_label_widget)
        sign_in_layout.addWidget(password_widget)
        sign_in_layout.addWidget(sign_in_button_widget)
        sign_in_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Створення sign_in_widget
        sign_in_widget = QWidget()
        sign_in_widget.setLayout(sign_in_layout)

        # Додавання картинки трамвая
        tram_picture_label = QLabel()
        tram_picture_image = QImage("../resources/icons/tram_picture1.png")

        # Увеличение изображения
        scaled_image = tram_picture_image.scaled(
            int(tram_picture_image.width() * 1.3),
            int(tram_picture_image.height() * 1.3),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        tram_picture_pixmap = QPixmap(scaled_image)
        tram_picture_label.setPixmap(tram_picture_pixmap)

        tram_picture_layout = QHBoxLayout()
        tram_picture_layout.addWidget(tram_picture_label)
        tram_picture_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tram_picture_widget = QWidget()
        tram_picture_widget.setLayout(tram_picture_layout)

        # З'єднання картинки з елементами для входу
        tram_picture_and_sign_in_layout = QHBoxLayout()
        tram_picture_and_sign_in_layout.addWidget(tram_picture_widget)
        tram_picture_and_sign_in_layout.addWidget(sign_in_widget)
        tram_picture_and_sign_in_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        tram_picture_and_sign_in_widget = QWidget()
        tram_picture_and_sign_in_widget.setLayout(tram_picture_and_sign_in_layout)

        # Додавання кнопки для виходу
        exit_button = QPushButton("Вийти із програми")
        exit_button.setFixedSize(700, 100)
        exit_button.setStyleSheet("""
                    QPushButton {
                        border-color: blue;
                           border-style: solid;
                           border-width: 2px;
                           border-radius: 15px;
                           color: white;
                           background-color: qlineargradient(
                               spread:pad, x1:0.3525, y1:0.472, x2:0.971591, y2:0.96, 
                               stop:0 rgba(0, 81, 168, 255), 
                               stop:1 rgba(147, 113, 255, 255)
                           );
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 30);
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 100);
                    }
                """)
        exit_button_font = QFont()
        exit_button_font.setFamily("appetite")
        exit_button_font.setPointSize(52)
        exit_button.setFont(exit_button_font)

        exit_button.clicked.connect(main_window.close)

        # Підключення обробників подій для зміни курсора
        exit_button.enterEvent = main_window.on_enter_event
        exit_button.leaveEvent = main_window.on_leave_event

        exit_button_layout = QHBoxLayout()
        exit_button_layout.addWidget(exit_button)
        exit_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        exit_button_widget = QWidget()
        exit_button_widget.setLayout(exit_button_layout)
        exit_button_widget.setStyleSheet("max-height: 200px;")

        # Створення main_layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_widget)
        main_layout.addWidget(tram_picture_and_sign_in_widget)
        main_layout.addWidget(exit_button_widget)

        self.setLayout(main_layout)
