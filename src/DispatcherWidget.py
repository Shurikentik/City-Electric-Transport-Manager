from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt
from src.styles import *
from AdditionalWindows.ConfirmDialog import ConfirmDialog
from AdditionalWindows.TableDialog import TableDialog
from AdditionalWindows.QueryResultDialog import QueryResultDialog
from models.Transport import Transport
from AddEditDialogs.AddEditTransportDialog import AddEditTransportDialog


# Вікно для диспетчерів
class DispatcherWidget(QWidget):
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

        # Кнопка "Транспортні засоби"
        transport_table_button = QPushButton()
        transport_table_button.setIcon(QIcon('../resources/icons/trolleybus_icon.svg'))
        transport_table_button.setText("Транспортні засоби")
        transport_table_button.setIconSize(transport_table_button.sizeHint() * 3)
        transport_table_button.setStyleSheet(button_style)
        transport_table_button.setFont(text_font2)
        transport_table_button.setFixedWidth(1250)
        transport_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        transport_table_button.clicked.connect(
            lambda: self.view_table("Транспортні засоби", "transport",
                                    Transport, AddEditTransportDialog, 2090)
        )
        menu_layout.addWidget(transport_table_button)

        # Підключення обробників подій для зміни курсора
        transport_table_button.enterEvent = self.main_window.on_enter_event
        transport_table_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Маршрути"
        route_table_button = QPushButton()
        route_table_button.setIcon(QIcon('../resources/icons/route_icon.svg'))
        route_table_button.setText("Маршрути")
        route_table_button.setIconSize(route_table_button.sizeHint() * 3)
        route_table_button.setStyleSheet(button_style)
        route_table_button.setFont(text_font2)
        route_table_button.setFixedWidth(1250)
        route_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        menu_layout.addWidget(route_table_button)

        # Підключення обробників подій для зміни курсора
        route_table_button.enterEvent = self.main_window.on_enter_event
        route_table_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Розклади руху"
        schedule_table_button = QPushButton()
        schedule_table_button.setIcon(QIcon('../resources/icons/time_icon.svg'))
        schedule_table_button.setText("Розклади руху")
        schedule_table_button.setIconSize(schedule_table_button.sizeHint() * 3)
        schedule_table_button.setStyleSheet(button_style)
        schedule_table_button.setFont(text_font2)
        schedule_table_button.setFixedWidth(1250)
        schedule_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        menu_layout.addWidget(schedule_table_button)

        # Підключення обробників подій для зміни курсора
        schedule_table_button.enterEvent = self.main_window.on_enter_event
        schedule_table_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Ремонтні операції"
        repair_table_button = QPushButton()
        repair_table_button.setIcon(QIcon('../resources/icons/wrench_icon.svg'))
        repair_table_button.setText("Ремонтні операції")
        repair_table_button.setIconSize(repair_table_button.sizeHint() * 3)
        repair_table_button.setStyleSheet(button_style)
        repair_table_button.setFont(text_font2)
        repair_table_button.setFixedWidth(1250)
        repair_table_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        menu_layout.addWidget(repair_table_button)

        # Підключення обробників подій для зміни курсора
        repair_table_button.enterEvent = self.main_window.on_enter_event
        repair_table_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Вивести транспорт на маршрут"
        assign_transport_button = QPushButton()
        assign_transport_button.setIcon(QIcon('../resources/icons/vector_icon.svg'))
        assign_transport_button.setText("Вивести транспорт на маршрут")
        assign_transport_button.setIconSize(assign_transport_button.sizeHint() * 3)
        assign_transport_button.setStyleSheet(button_style)
        assign_transport_button.setFont(text_font2)
        assign_transport_button.setFixedWidth(1250)
        assign_transport_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        menu_layout.addWidget(assign_transport_button)

        # Підключення обробників подій для зміни курсора
        assign_transport_button.enterEvent = self.main_window.on_enter_event
        assign_transport_button.leaveEvent = self.main_window.on_leave_event

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
        menu_layout.setSpacing(30)
        layout.addLayout(menu_layout)

        # Ініціалізація розмітки статистики
        statistics_layout = QVBoxLayout()

        # Рядок "Розділ статистики"
        # Іконка "Статистика"
        statistics_icon_pixmap = QPixmap("../resources/icons/route_icon.svg").scaled(100, 100)
        statistics_icon_label = QLabel()
        statistics_icon_label.setPixmap(statistics_icon_pixmap)

        # Надпис "Статистика руху"
        statistics_label = QLabel("Статистика руху")
        statistics_label.setStyleSheet(text_style)
        statistics_label.setFont(text_font7)
        statistics_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Збираємо три елементи в один рядок
        stat_title_layout = QHBoxLayout()
        stat_title_layout.addWidget(statistics_icon_label)
        stat_title_layout.addWidget(statistics_label)
        stat_title_layout.setSpacing(30)
        stat_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        statistics_layout.addLayout(stat_title_layout)

        # Кнопка "Список розкладів за часом"
        schedule_by_time_button = QPushButton()
        schedule_by_time_button.setIcon(QIcon('../resources/icons/time_icon.svg'))
        schedule_by_time_button.setText("Список розкладів за часом")
        schedule_by_time_button.setIconSize(schedule_by_time_button.sizeHint() * 2.2)
        schedule_by_time_button.setStyleSheet(button_style)
        schedule_by_time_button.setFont(text_font5)
        schedule_by_time_button.setFixedWidth(1250)
        schedule_by_time_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(schedule_by_time_button)

        # Підключення обробників подій для зміни курсора
        schedule_by_time_button.enterEvent = self.main_window.on_enter_event
        schedule_by_time_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Центральні маршрути"
        central_routes_button = QPushButton()
        central_routes_button.setIcon(QIcon('../resources/icons/route_icon.svg'))
        central_routes_button.setText("Центральні маршрути")
        central_routes_button.setIconSize(central_routes_button.sizeHint() * 2.2)
        central_routes_button.setStyleSheet(button_style)
        central_routes_button.setFont(text_font5)
        central_routes_button.setFixedWidth(1250)
        central_routes_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(central_routes_button)

        # Підключення обробників подій для зміни курсора
        central_routes_button.enterEvent = self.main_window.on_enter_event
        central_routes_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Доступні транспорти"
        available_transports_button = QPushButton()
        available_transports_button.setIcon(QIcon('../resources/icons/trolleybus_icon.svg'))
        available_transports_button.setText("Доступні транспорти")
        available_transports_button.setIconSize(available_transports_button.sizeHint() * 2.2)
        available_transports_button.setStyleSheet(button_style)
        available_transports_button.setFont(text_font5)
        available_transports_button.setFixedWidth(1250)
        available_transports_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(available_transports_button)

        # Підключення обробників подій для зміни курсора
        available_transports_button.enterEvent = self.main_window.on_enter_event
        available_transports_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Журнал виходу на маршрут"
        journal_button = QPushButton()
        journal_button.setIcon(QIcon('../resources/icons/journal_icon.svg'))
        journal_button.setText("Журнал виходу на маршрут")
        journal_button.setIconSize(journal_button.sizeHint() * 2.2)
        journal_button.setStyleSheet(button_style)
        journal_button.setFont(text_font5)
        journal_button.setFixedWidth(1250)
        journal_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(journal_button)

        # Підключення обробників подій для зміни курсора
        journal_button.enterEvent = self.main_window.on_enter_event
        journal_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Транспорти в ремонті"
        transports_in_repair_button = QPushButton()
        transports_in_repair_button.setIcon(QIcon('../resources/icons/wrench_icon.svg'))
        transports_in_repair_button.setText("Транспорти в ремонті")
        transports_in_repair_button.setIconSize(transports_in_repair_button.sizeHint() * 2.2)
        transports_in_repair_button.setStyleSheet(button_style)
        transports_in_repair_button.setFont(text_font5)
        transports_in_repair_button.setFixedWidth(1250)
        transports_in_repair_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(transports_in_repair_button)

        # Підключення обробників подій для зміни курсора
        transports_in_repair_button.enterEvent = self.main_window.on_enter_event
        transports_in_repair_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Транспорти не в ремонті"
        transports_not_in_repair_button = QPushButton()
        transports_not_in_repair_button.setIcon(QIcon('../resources/icons/wrench_icon.svg'))
        transports_not_in_repair_button.setText("Транспорти не в ремонті")
        transports_not_in_repair_button.setIconSize(transports_not_in_repair_button.sizeHint() * 2.2)
        transports_not_in_repair_button.setStyleSheet(button_style)
        transports_not_in_repair_button.setFont(text_font5)
        transports_not_in_repair_button.setFixedWidth(1250)
        transports_not_in_repair_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(transports_not_in_repair_button)

        # Підключення обробників подій для зміни курсора
        transports_not_in_repair_button.enterEvent = self.main_window.on_enter_event
        transports_not_in_repair_button.leaveEvent = self.main_window.on_leave_event

        # Кнопка "Статистика стану транспортів"
        repair_statistics_button = QPushButton()
        repair_statistics_button.setIcon(QIcon('../resources/icons/wrench_icon.svg'))
        repair_statistics_button.setText("Статистика стану транспортів")
        repair_statistics_button.setIconSize(repair_statistics_button.sizeHint() * 2.2)
        repair_statistics_button.setStyleSheet(button_style)
        repair_statistics_button.setFont(text_font5)
        repair_statistics_button.setFixedWidth(1250)
        repair_statistics_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        statistics_layout.addWidget(repair_statistics_button)

        # Підключення обробників подій для зміни курсора
        repair_statistics_button.enterEvent = self.main_window.on_enter_event
        repair_statistics_button.leaveEvent = self.main_window.on_leave_event

        # Додавання картинки диспетчера
        dispatcher_picture_label = QLabel()
        dispatcher_image = QImage("../resources/icons/dispatcher_picture.png")
        dispatcher_picture_pixmap = QPixmap(dispatcher_image)
        dispatcher_picture_label.setPixmap(dispatcher_picture_pixmap)
        dispatcher_picture_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        statistics_layout.addWidget(dispatcher_picture_label)

        # Додавання розмітки статистики до головної розмітки
        statistics_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        statistics_layout.setSpacing(20)
        layout.addLayout(statistics_layout)
        self.setLayout(layout)

    # Обробка події при натисканні кнопки "Налаштування профілю"
    def open_profile_settings(self):
        self.main_window.show_profile_settings_widget(employee=self.employee)

    # Функція перегляду таблиці
    def view_table(self, title_name, table_name, model_class, add_edit_class, table_width,
                   table_max_height=None, is_add_button=True, is_edit_button=True):
        dialog = TableDialog(title_name, table_name, model_class, add_edit_class, table_width,
                             table_max_height=table_max_height, is_add_button=is_add_button,
                             is_edit_button=is_edit_button)
        dialog.exec()

    # Функція перегляду результату запиту
    def view_query_result(self, title_name, query_function, table_width, table_max_height=None):
        dialog = QueryResultDialog(title_label=title_name, query_function=query_function, table_width=table_width,
                                   table_max_height=table_max_height)
        dialog.exec()

    # Обробка події при натисканні кнопки "Вийти із облікового запису"
    def exit_profile(self):
        dialog = ConfirmDialog("Ви впевнені, що хочете вийти?")
        if dialog.exec() == QDialog.Accepted:
            self.main_window.show_login_widget()
