from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PySide6.QtGui import QIcon, QImage
from PySide6.QtCore import Qt
from styles import *
from AdditionalWindows.ConfirmDialog import ConfirmDialog
from AdditionalWindows.TableDialog import TableDialog
from models.Benefit import Benefit
from models.Ticket import Ticket
from models.Tariff import Tariff
from models.ValidityType import ValidityType
from models.TransportType import TransportType
from models.Employee import Employee
from AddEditDialogs.AddEditTransportTypeDialog import AddEditTransportTypeDialog
from AddEditDialogs.AddEditValidityTypeDialog import AddEditValidityTypeDialog
from AddEditDialogs.AddEditBenefitDialog import AddEditBenefitDialog


class AdminWidget(QWidget):
    def __init__(self, main_window, employee):
        super().__init__()
        self.employee = employee
        self.main_window = main_window

        # Ініціалізація головної розмітки
        admin_layout = QHBoxLayout()

        # Ініціалізація розмітки меню
        menu_layout = QVBoxLayout()

        # Надпис з привітанням
        welcome_label = QLabel(f"Вітаємо, {self.employee.full_name.split()[1]}")
        welcome_label.setStyleSheet(text_style)
        welcome_label.setFont(text_font7)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

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

        # Підключення обробників подій для зміни курсора
        change_profile_button.enterEvent = main_window.on_enter_event
        change_profile_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Переглянути користувачів системи"
        employee_table_button = QPushButton()
        employee_table_button.setIcon(QIcon('../resources/icons/people_icon.svg'))
        employee_table_button.setText("Переглянути користувачів системи")
        employee_table_button.setIconSize(employee_table_button.sizeHint() * 3)
        employee_table_button.setStyleSheet(button_style)
        employee_table_button.setFont(text_font2)
        employee_table_button.setFixedWidth(1250)
        employee_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        employee_table_button.enterEvent = main_window.on_enter_event
        employee_table_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Типи транспорту"
        transport_type_button = QPushButton()
        transport_type_button.setIcon(QIcon('../resources/icons/trolleybus_icon.svg'))
        transport_type_button.setText("Типи транспорту")
        transport_type_button.setIconSize(transport_type_button.sizeHint() * 3)
        transport_type_button.setStyleSheet(button_style)
        transport_type_button.setFont(text_font2)
        transport_type_button.setFixedWidth(1250)
        transport_type_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        transport_type_button.clicked.connect(lambda: self.view_table("Типи електротранспорту", "transporttype",
                                                                      TransportType, AddEditTransportTypeDialog,
                                                                      820, table_max_height=322))

        # Підключення обробників подій для зміни курсора
        transport_type_button.enterEvent = main_window.on_enter_event
        transport_type_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Типи терміну чинності"
        validity_type_button = QPushButton()
        validity_type_button.setIcon(QIcon('../resources/icons/time_icon.svg'))
        validity_type_button.setText("Типи терміну чинності")
        validity_type_button.setIconSize(validity_type_button.sizeHint() * 3)
        validity_type_button.setStyleSheet(button_style)
        validity_type_button.setFont(text_font2)
        validity_type_button.setFixedWidth(1250)
        validity_type_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        validity_type_button.clicked.connect(lambda: self.view_table("Терміни чинності", "validitytype",
                                                                     ValidityType, AddEditValidityTypeDialog,
                                                                     885, table_max_height=322))

        # Підключення обробників подій для зміни курсора
        validity_type_button.enterEvent = main_window.on_enter_event
        validity_type_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Тарифи"
        tariff_table_button = QPushButton()
        tariff_table_button.setIcon(QIcon('../resources/icons/money_icon.svg'))
        tariff_table_button.setText("Тарифи")
        tariff_table_button.setIconSize(tariff_table_button.sizeHint() * 3)
        tariff_table_button.setStyleSheet(button_style)
        tariff_table_button.setFont(text_font2)
        tariff_table_button.setFixedWidth(1250)
        tariff_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        tariff_table_button.enterEvent = main_window.on_enter_event
        tariff_table_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Пільги"
        benefit_table_button = QPushButton()
        benefit_table_button.setIcon(QIcon('../resources/icons/percent_icon.svg'))
        benefit_table_button.setText("Пільги")
        benefit_table_button.setIconSize(benefit_table_button.sizeHint() * 3)
        benefit_table_button.setStyleSheet(button_style)
        benefit_table_button.setFont(text_font2)
        benefit_table_button.setFixedWidth(1250)
        benefit_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        benefit_table_button.clicked.connect(lambda: self.view_table("Пільги", "benefit",
                                                                     Benefit, AddEditBenefitDialog,
                                                                     1150, 322))

        # Підключення обробників подій для зміни курсора
        benefit_table_button.enterEvent = main_window.on_enter_event
        benefit_table_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Продані квитки"
        ticket_table_button = QPushButton()
        ticket_table_button.setIcon(QIcon('../resources/icons/ticket_icon.svg'))
        ticket_table_button.setText("Продані квитки")
        ticket_table_button.setIconSize(ticket_table_button.sizeHint() * 3)
        ticket_table_button.setStyleSheet(button_style)
        ticket_table_button.setFont(text_font2)
        ticket_table_button.setFixedWidth(1250)
        ticket_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        ticket_table_button.enterEvent = main_window.on_enter_event
        ticket_table_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Вийти із облікового запису"
        exit_profile_button = QPushButton()
        exit_profile_button.setIcon(QIcon('../resources/icons/exit_icon.svg'))
        exit_profile_button.setText("Вийти із облікового запису")
        exit_profile_button.setIconSize(exit_profile_button.sizeHint() * 3)
        exit_profile_button.setStyleSheet(button_style)
        exit_profile_button.setFont(text_font2)
        exit_profile_button.setFixedWidth(1250)
        exit_profile_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        exit_profile_button.enterEvent = main_window.on_enter_event
        exit_profile_button.leaveEvent = main_window.on_leave_event

        # Підключення кнопки до команди
        exit_profile_button.clicked.connect(self.exit_profile)

        # Додавання усіх елементів до розмітки меню
        menu_layout.addWidget(welcome_label)
        menu_layout.addWidget(change_profile_button)
        menu_layout.addWidget(employee_table_button)
        menu_layout.addWidget(transport_type_button)
        menu_layout.addWidget(validity_type_button)
        menu_layout.addWidget(tariff_table_button)
        menu_layout.addWidget(benefit_table_button)
        menu_layout.addWidget(ticket_table_button)
        menu_layout.addWidget(exit_profile_button)
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.setSpacing(30)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)

        # Ініціалізація розмітки статистики
        statistics_layout = QVBoxLayout()

        # Рядок "Розділ статистики"
        # Іконка "Статистика"
        statistics_icon_pixmap = QPixmap("../resources/icons/statistics_icon.svg").scaled(100, 100)
        statistics_icon_label = QLabel()
        statistics_icon_label.setPixmap(statistics_icon_pixmap)

        # Надпис "Розділ статистики"
        statistics_label = QLabel("Розділ Статистики")
        statistics_label.setStyleSheet(text_style)
        statistics_label.setFont(text_font7)
        statistics_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Збираємо три елементи в один рядок
        stat_layout = QHBoxLayout()
        stat_layout.addWidget(statistics_icon_label)
        stat_layout.addWidget(statistics_label)
        stat_layout.setSpacing(30)
        stat_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        stat_widget = QWidget()
        stat_widget.setLayout(stat_layout)

        # Кнопка "Усі квитки, продані за останній місяць"
        months_tickets_button = QPushButton()
        months_tickets_button.setIcon(QIcon('../resources/icons/ticket_icon.svg'))
        months_tickets_button.setText("Квитки за останній місяць")
        months_tickets_button.setIconSize(months_tickets_button.sizeHint() * 3)
        months_tickets_button.setStyleSheet(button_style)
        months_tickets_button.setFont(text_font2)
        months_tickets_button.setFixedWidth(1250)
        months_tickets_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        months_tickets_button.enterEvent = main_window.on_enter_event
        months_tickets_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Загальна кількість проданих квитків"
        all_tickets_button = QPushButton()
        all_tickets_button.setIcon(QIcon('../resources/icons/ticket_icon.svg'))
        all_tickets_button.setText("Загальна кількість квитків")
        all_tickets_button.setIconSize(all_tickets_button.sizeHint() * 3)
        all_tickets_button.setStyleSheet(button_style)
        all_tickets_button.setFont(text_font2)
        all_tickets_button.setFixedWidth(1250)
        all_tickets_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        all_tickets_button.enterEvent = main_window.on_enter_event
        all_tickets_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Кількість квитків, проданих кожним касиром"
        tickets_by_cashier_button = QPushButton()
        tickets_by_cashier_button.setIcon(QIcon('../resources/icons/ticket_icon.svg'))
        tickets_by_cashier_button.setText("Кількість квитків за касиром")
        tickets_by_cashier_button.setIconSize(tickets_by_cashier_button.sizeHint() * 3)
        tickets_by_cashier_button.setStyleSheet(button_style)
        tickets_by_cashier_button.setFont(text_font2)
        tickets_by_cashier_button.setFixedWidth(1250)
        tickets_by_cashier_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        tickets_by_cashier_button.enterEvent = main_window.on_enter_event
        tickets_by_cashier_button.leaveEvent = main_window.on_leave_event

        # Додавання картинки адміна
        admin_picture_label = QLabel()
        admin_image = QImage("../resources/icons/admin_picture.png")
        admin_picture_pixmap = QPixmap(admin_image)
        admin_picture_label.setPixmap(admin_picture_pixmap)
        admin_picture_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Додавання усіх елементів до розмітки статистики
        statistics_layout.addWidget(stat_widget)
        statistics_layout.addWidget(months_tickets_button)
        statistics_layout.addWidget(all_tickets_button)
        statistics_layout.addWidget(tickets_by_cashier_button)
        statistics_layout.addWidget(admin_picture_label)
        statistics_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        statistics_layout.setSpacing(30)

        statistics_widget = QWidget()
        statistics_widget.setLayout(statistics_layout)

        # Додавання розміток до головної розмітки
        admin_layout.addWidget(menu_widget)
        admin_layout.addWidget(statistics_widget)

        # Встановлення головної розмітки
        self.setLayout(admin_layout)

    # Обробка події при натисканні кнопки "Налаштування профілю"
    def open_profile_settings(self):
        self.main_window.show_profile_settings_widget(employee=self.employee)

    # Функція перегляду таблиці
    def view_table(self, title_name, table_name, model_class, add_edit_class, table_width,
                   table_max_height=None, is_add_button=True):
        dialog = TableDialog(title_name, table_name, model_class, add_edit_class, table_width,
                             table_max_height=table_max_height, is_add_button=is_add_button)
        dialog.exec()

    # Обробка події при натисканні кнопки "Вийти із облікового запису"
    def exit_profile(self):
        dialog = ConfirmDialog("Ви впевнені, що хочете вийти?")
        if dialog.exec() == QDialog.Accepted:
            self.main_window.show_login_widget()
