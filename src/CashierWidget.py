from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt
from AdditionalWindows.ConfirmExitDialog import ConfirmExitDialog


class CashierWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Стилі
        text_style = "background-color:none; color:white;"
        button_style = """
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
                """

        # Шрифти
        text_font1 = QFont()
        text_font1.setFamily("appetite")
        text_font1.setPointSize(90)

        text_font2 = QFont()
        text_font2.setFamily("appetite")
        text_font2.setPointSize(52)

        # Додавання картинки касира
        cashier_picture_label = QLabel()
        cashier_picture_image = QImage("../resources/icons/woman_cashier.png")

        # Збільшення зображення
        scaled_image = cashier_picture_image.scaled(
            int(cashier_picture_image.width() * 0.25),
            int(cashier_picture_image.height() * 0.25),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        cashier_picture_pixmap = QPixmap(scaled_image)
        cashier_picture_label.setPixmap(cashier_picture_pixmap)

        cashier_picture_layout = QHBoxLayout()
        cashier_picture_layout.addWidget(cashier_picture_label)
        cashier_picture_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cashier_picture_widget = QWidget()
        cashier_picture_widget.setLayout(cashier_picture_layout)

        # Додавання меню
        cashier_menu_layout = QVBoxLayout()

        # Надпис Вітання
        welcome_label = QLabel(f"Вітаємо, ...")
        welcome_label.setStyleSheet(text_style)
        welcome_label.setFont(text_font1)

        welcome_label_layout = QHBoxLayout()
        welcome_label_layout.addWidget(welcome_label)
        welcome_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        welcome_label_widget = QWidget()
        welcome_label_widget.setLayout(welcome_label_layout)

        # Кнопка "Налаштування профілю"
        change_profile_button = QPushButton()
        change_profile_button.setIcon(QIcon('../resources/icons/settings_icon.svg'))
        change_profile_button.setText("Налаштування профілю")
        change_profile_button.setIconSize(change_profile_button.sizeHint() * 3)
        change_profile_button.setStyleSheet(button_style)
        change_profile_button.setFont(text_font2)
        change_profile_button.setFixedWidth(1100)
        change_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        change_profile_button.enterEvent = main_window.on_enter_event
        change_profile_button.leaveEvent = main_window.on_leave_event

        change_profile_button_layout = QHBoxLayout()
        change_profile_button_layout.addWidget(change_profile_button)
        change_profile_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        change_profile_button_widget = QWidget()
        change_profile_button_widget.setLayout(change_profile_button_layout)

        # Кнопка "Оформити продаж квитка"
        sale_ticket_button = QPushButton()
        sale_ticket_button.setIcon(QIcon('../resources/icons/ticket_icon.svg'))
        sale_ticket_button.setText("Оформити продаж квитка")
        sale_ticket_button.setIconSize(sale_ticket_button.sizeHint() * 3)
        sale_ticket_button.setStyleSheet(button_style)
        sale_ticket_button.setFont(text_font2)
        sale_ticket_button.setFixedWidth(1100)
        sale_ticket_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        sale_ticket_button.enterEvent = main_window.on_enter_event
        sale_ticket_button.leaveEvent = main_window.on_leave_event

        sale_ticket_button_layout = QHBoxLayout()
        sale_ticket_button_layout.addWidget(sale_ticket_button)
        sale_ticket_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        sale_ticket_button_widget = QWidget()
        sale_ticket_button_widget.setLayout(sale_ticket_button_layout)

        # Кнопка "Вийти із облікового запису"
        exit_profile_button = QPushButton()
        exit_profile_button.setIcon(QIcon('../resources/icons/exit_icon.svg'))
        exit_profile_button.setText("Вийти із облікового запису")
        exit_profile_button.setIconSize(exit_profile_button.sizeHint() * 3)
        exit_profile_button.setStyleSheet(button_style)
        exit_profile_button.setFont(text_font2)
        exit_profile_button.setFixedWidth(1100)
        exit_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        exit_profile_button.enterEvent = main_window.on_enter_event
        exit_profile_button.leaveEvent = main_window.on_leave_event

        # Підключення кнопки до команди
        exit_profile_button.clicked.connect(self.exit_profile)

        exit_profile_button_layout = QHBoxLayout()
        exit_profile_button_layout.addWidget(exit_profile_button)
        exit_profile_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        exit_profile_button_widget = QWidget()
        exit_profile_button_widget.setLayout(exit_profile_button_layout)

        cashier_menu_layout.addWidget(welcome_label_widget)
        cashier_menu_layout.addWidget(change_profile_button_widget)
        cashier_menu_layout.addWidget(sale_ticket_button_widget)
        cashier_menu_layout.addWidget(exit_profile_button_widget)
        cashier_menu_layout.setSpacing(40)
        cashier_menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cashier_menu_widget = QWidget()
        cashier_menu_widget.setLayout(cashier_menu_layout)

        cashier_layout = QHBoxLayout()
        cashier_layout.addWidget(cashier_picture_widget)
        cashier_layout.addWidget(cashier_menu_widget)
        self.setLayout(cashier_layout)

    # Обробка події при натисканні кнопки "Вийти із облікового запису"
    def exit_profile(self):
        dialog = ConfirmExitDialog()
        if dialog.exec() == QDialog.Accepted:
            self.main_window.show_login_widget()
