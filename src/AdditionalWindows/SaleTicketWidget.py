from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PySide6.QtGui import QIcon, QImage
from src.styles import *
from PySide6.QtCore import Qt


# Віджет для налаштування профілю
class SaleTicketWidget(QWidget):
    def __init__(self, main_window, employee):
        super().__init__()
        self.employee = employee
        self.main_window = main_window

        # Ініціалізація основного макету
        main_layout = QHBoxLayout()

        # Ініціалізація макету оформлення продажу
        sale_ticket_layout = QVBoxLayout()

        # Надпис "Оформлення продажу квитка"
        sale_ticket_label = QLabel("Оформлення продажу квитка")
        sale_ticket_label.setStyleSheet(text_style)
        sale_ticket_label.setFont(text_font5)
        sale_ticket_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Надпис "Оберіть тип електротранспорту"
        transport_type_label = QLabel("Оберіть тип електротранспорту")
        transport_type_label.setStyleSheet(text_style)
        transport_type_label.setFont(text_font5)
        transport_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок для обирання типу електротранспорту
        # Іконка транспорту
        transport_icon_pixmap = QPixmap("../resources/icons/trolleybus_icon.svg").scaled(65, 65)
        transport_icon_label = QLabel()
        transport_icon_label.setPixmap(transport_icon_pixmap)

        # Об'єднання рядку обирання типу електротранспорту
        pick_transport_type_layout = QHBoxLayout()
        pick_transport_type_layout.addWidget(transport_icon_label)
        pick_transport_type_layout.setSpacing(20)
        pick_transport_type_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        pick_transport_type_widget = QWidget()
        pick_transport_type_widget.setLayout(pick_transport_type_layout)

        # Надпис "Оберіть тип чинності квитка"
        validity_type_label = QLabel("Оберіть тип чинності квитка")
        validity_type_label.setStyleSheet(text_style)
        validity_type_label.setFont(text_font5)
        validity_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок для обирання типу чинності квитка
        # Іконка часу
        validity_icon_pixmap = QPixmap("../resources/icons/time_icon.svg").scaled(65, 65)
        validity_icon_label = QLabel()
        validity_icon_label.setPixmap(validity_icon_pixmap)

        # Об'єднання рядку обирання типу чинності квитка
        pick_validity_type_layout = QHBoxLayout()
        pick_validity_type_layout.addWidget(validity_icon_label)
        pick_validity_type_layout.setSpacing(20)
        pick_validity_type_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        pick_validity_type_widget = QWidget()
        pick_validity_type_widget.setLayout(pick_validity_type_layout)

        # Надпис "*Оберіть тип пільги (якщо є)"
        benefit_type_label = QLabel("*Оберіть тип пільги (якщо є)")
        benefit_type_label.setStyleSheet(text_style)
        benefit_type_label.setFont(text_font5)
        benefit_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок для обирання типу пільги
        # Іконка відсотка
        benefit_icon_pixmap = QPixmap("../resources/icons/percent_icon.svg").scaled(65, 65)
        benefit_icon_label = QLabel()
        benefit_icon_label.setPixmap(benefit_icon_pixmap)

        # Об'єднання рядку обирання типу пільги
        pick_benefit_type_layout = QHBoxLayout()
        pick_benefit_type_layout.addWidget(benefit_icon_label)
        pick_benefit_type_layout.setSpacing(20)
        pick_benefit_type_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        pick_benefit_type_widget = QWidget()
        pick_benefit_type_widget.setLayout(pick_benefit_type_layout)

        # Кнопка "Розрахувати вартість квитка"
        calculate_price_button = QPushButton()
        calculate_price_button.setIcon(QIcon('../resources/icons/money_icon.svg'))
        calculate_price_button.setText("Розрахувати вартість квитка")
        calculate_price_button.setIconSize(calculate_price_button.sizeHint() * 2.2)
        calculate_price_button.setStyleSheet(button_style)
        calculate_price_button.setFont(text_font5)
        calculate_price_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        calculate_price_button.enterEvent = main_window.on_enter_event
        calculate_price_button.leaveEvent = main_window.on_leave_event

        # Рядок "Ціна квитка"
        # Іконка монет
        price_icon_pixmap = QPixmap("../resources/icons/coins_icon.svg").scaled(65, 65)
        price_icon_label = QLabel()
        price_icon_label.setPixmap(price_icon_pixmap)

        # Надпис "Ціна квитка"
        price_label = QLabel(f"Ціна квитка: ... грн")
        price_label.setStyleSheet(text_style)
        price_label.setFont(text_font5)
        price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Об'єднання рядку з ціною квитка
        ticket_price_layout = QHBoxLayout()
        ticket_price_layout.addWidget(price_icon_label)
        ticket_price_layout.addWidget(price_label)
        ticket_price_layout.setSpacing(20)
        ticket_price_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ticket_price_widget = QWidget()
        ticket_price_widget.setLayout(ticket_price_layout)

        # Надпис "Вкажіть передані кошти"
        input_pay_label = QLabel("Вкажіть передані кошти")
        input_pay_label.setStyleSheet(text_style)
        input_pay_label.setFont(text_font5)
        input_pay_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Рядок "Передані кошти"
        # Іконка переданих коштів
        pay_icon_pixmap = QPixmap("../resources/icons/pay_icon.svg").scaled(65, 65)
        pay_icon_label = QLabel()
        pay_icon_label.setPixmap(pay_icon_pixmap)

        # Текстове поле для введених коштів
        input_pay_line_edit = QLineEdit()
        input_pay_line_edit.setPlaceholderText("Передані кошти")
        input_pay_line_edit.setStyleSheet(text_line_style)
        input_pay_line_edit.setFont(text_font6)

        # Підключення обробників подій для зміни курсора
        input_pay_line_edit.setCursor(main_window.text_cursor)
        input_pay_line_edit.enterEvent = main_window.on_line_edit_enter
        input_pay_line_edit.leaveEvent = main_window.on_line_edit_leave

        # Об'єднання рядку з указанням переданих коштів
        input_pay_layout = QHBoxLayout()
        input_pay_layout.addWidget(pay_icon_label)
        input_pay_layout.addWidget(input_pay_line_edit)
        input_pay_layout.setSpacing(20)
        input_pay_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        input_pay_widget = QWidget()
        input_pay_widget.setLayout(input_pay_layout)

        # Кнопка "Обчислити решту"
        calculate_rest_button = QPushButton()
        calculate_rest_button.setIcon(QIcon('../resources/icons/money_icon.svg'))
        calculate_rest_button.setText("Обчислити решту")
        calculate_rest_button.setIconSize(calculate_rest_button.sizeHint() * 2.2)
        calculate_rest_button.setStyleSheet(button_style)
        calculate_rest_button.setFont(text_font5)
        calculate_rest_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        calculate_rest_button.enterEvent = main_window.on_enter_event
        calculate_rest_button.leaveEvent = main_window.on_leave_event

        # Рядок "Решта"
        # Іконка монет
        rest_icon_pixmap = QPixmap("../resources/icons/coins_icon.svg").scaled(65, 65)
        rest_icon_label = QLabel()
        rest_icon_label.setPixmap(rest_icon_pixmap)

        # Надпис "Решта"
        rest_label = QLabel(f"Решта: ... грн")
        rest_label.setStyleSheet(text_style)
        rest_label.setFont(text_font5)
        rest_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Об'єднання рядку з рештою
        rest_layout = QHBoxLayout()
        rest_layout.addWidget(rest_icon_label)
        rest_layout.addWidget(rest_label)
        rest_layout.setSpacing(20)
        rest_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        rest_widget = QWidget()
        rest_widget.setLayout(rest_layout)

        # Кнопка "Оформити продаж квитка"
        sale_ticket_button = QPushButton()
        sale_ticket_button.setIcon(QIcon('../resources/icons/money_bag_icon.svg'))
        sale_ticket_button.setText("Оформити продаж квитка")
        sale_ticket_button.setIconSize(sale_ticket_button.sizeHint() * 2.2)
        sale_ticket_button.setStyleSheet(button_style)
        sale_ticket_button.setFont(text_font5)
        sale_ticket_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Підключення обробників подій для зміни курсора
        sale_ticket_button.enterEvent = main_window.on_enter_event
        sale_ticket_button.leaveEvent = main_window.on_leave_event

        # Кнопка "Скасувати операцію продажу"
        cancel_sale_button = QPushButton()
        cancel_sale_button.setIcon(QIcon('../resources/icons/cancel_icon.svg'))
        cancel_sale_button.setText("Скасувати операцію продажу")
        cancel_sale_button.setIconSize(cancel_sale_button.sizeHint() * 2.2)
        cancel_sale_button.setStyleSheet(button_style)
        cancel_sale_button.setFont(text_font5)
        cancel_sale_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        cancel_sale_button.clicked.connect(self.cancel_sale)

        # Підключення обробників подій для зміни курсора
        cancel_sale_button.enterEvent = main_window.on_enter_event
        cancel_sale_button.leaveEvent = main_window.on_leave_event

        # Об'єднання елементів продажу квитка
        sale_ticket_layout.addWidget(sale_ticket_label)
        sale_ticket_layout.addWidget(transport_type_label)
        sale_ticket_layout.addWidget(pick_transport_type_widget)
        sale_ticket_layout.addWidget(validity_type_label)
        sale_ticket_layout.addWidget(pick_validity_type_widget)
        sale_ticket_layout.addWidget(benefit_type_label)
        sale_ticket_layout.addWidget(pick_benefit_type_widget)
        sale_ticket_layout.addWidget(calculate_price_button)
        sale_ticket_layout.addWidget(ticket_price_widget)
        sale_ticket_layout.addWidget(input_pay_label)
        sale_ticket_layout.addWidget(input_pay_widget)
        sale_ticket_layout.addWidget(calculate_rest_button)
        sale_ticket_layout.addWidget(rest_widget)
        sale_ticket_layout.addWidget(sale_ticket_button)
        sale_ticket_layout.addWidget(cancel_sale_button)

        sale_ticket_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sale_ticket_layout.setSpacing(12)

        sale_ticket_widget = QWidget()
        sale_ticket_widget.setLayout(sale_ticket_layout)

        # Додавання картинки
        picture_label = QLabel()
        picture_image = QImage("../resources/icons/bus_ticket.png")

        # Збільшення зображення
        scaled_image = picture_image.scaled(
            int(picture_image.width() * 2.5),
            int(picture_image.height() * 2.5),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        # Встановлення зображення
        picture_pixmap = QPixmap(scaled_image)
        picture_label.setPixmap(picture_pixmap)

        # Поєднання усіх елементів до основного макету
        main_layout.addWidget(sale_ticket_widget)
        main_layout.addWidget(picture_label)
        self.setLayout(main_layout)

    # Функція обробки події натискання кнопки "Скасувати операцію продажу"
    def cancel_sale(self):
        self.main_window.show_cashier_widget(employee=self.employee)
