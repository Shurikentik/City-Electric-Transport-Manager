from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.styles import *


# Вікно додавання/зміни пільги
class AddEditBenefitDialog(QDialog):
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
        title_label = QLabel(f"{"Змінити" if self.instance else "Додати нову"} пільгу")
        title_label.setStyleSheet(text_style)
        title_label.setFont(text_font7)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Надпис "Введіть назву пільги"
        input_type_label = QLabel("Введіть назву пільги")
        input_type_label.setStyleSheet(text_style)
        input_type_label.setFont(text_font5)
        input_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_type_label)

        # Рядок "Назва пільги"
        # Іконка пільги
        pay_icon_pixmap = QPixmap("../resources/icons/pay_icon.svg").scaled(100, 100)
        pay_icon_label = QLabel()
        pay_icon_label.setPixmap(pay_icon_pixmap)

        # Текстове поле для назви пільги
        type_line_edit = QLineEdit()
        if self.instance:
            type_line_edit.setText(self.instance.benefit_name)
        type_line_edit.setPlaceholderText("Назва пільги")
        type_line_edit.setStyleSheet(text_line_style)
        type_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        type_line_edit.setCursor(self.text_cursor)
        type_line_edit.enterEvent = self.on_line_edit_enter
        type_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з назвою пільги
        benefit_layout = QHBoxLayout()
        benefit_layout.addWidget(pay_icon_label)
        benefit_layout.addWidget(type_line_edit)
        benefit_layout.setSpacing(20)
        benefit_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(benefit_layout)

        # Надпис "Введіть модифікатор знижки"
        input_discount_label = QLabel("Введіть модифікатор знижки")
        input_discount_label.setStyleSheet(text_style)
        input_discount_label.setFont(text_font5)
        input_discount_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(input_discount_label)

        # Рядок "Модифікатор знижки"
        # Іконка проценту
        percent_icon_pixmap = QPixmap("../resources/icons/percent_icon.svg").scaled(100, 100)
        percent_icon_label = QLabel()
        percent_icon_label.setPixmap(percent_icon_pixmap)

        # Текстове поле для модифікатору знижки
        discount_line_edit = QLineEdit()
        if self.instance:
            discount_line_edit.setText(str(self.instance.discount_modifier))
        discount_line_edit.setPlaceholderText("Модифікатор знижки")
        discount_line_edit.setStyleSheet(text_line_style)
        discount_line_edit.setFont(text_font4)

        # Підключення обробників подій для зміни курсора
        discount_line_edit.setCursor(self.text_cursor)
        discount_line_edit.enterEvent = self.on_line_edit_enter
        discount_line_edit.leaveEvent = self.on_line_edit_leave

        # Об'єднання рядку з модифікатором знижки
        discount_layout = QHBoxLayout()
        discount_layout.addWidget(percent_icon_label)
        discount_layout.addWidget(discount_line_edit)
        discount_layout.setSpacing(20)
        discount_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(discount_layout)

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
        def save_benefit():
            benefit_name = type_line_edit.text().strip()
            # Перевірка на заповненість поля з назвою пільги
            if not benefit_name or benefit_name == "Назва пільги":
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", "Ви не вказали назву пільги")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return
            # Перевірка формату вказання знижки
            try:
                discount_modifier = float(discount_line_edit.text().strip())
            except ValueError:
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                      "Модифікатор знижки вказано у неправильному форматі")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return
            # Перевірка, чи знижка знаходиться у межах від 0 до 1
            if not (discount_modifier > 0 and discount_modifier <= 1):
                msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                      "Модифікатор знижки має бути у межах від 0.00 до 1.00")
                msg_box.setStyleSheet(message_box_style)
                msg_box.exec()
                return

            # Додавання нового об'єкта
            if not self.instance:
                # Перевірка унікальності назви
                existing_benefits = [benefit.benefit_name for benefit in self.model_class.get_all()]
                if benefit_name in existing_benefits:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Пільга з такою назвою вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    new_benefit = self.model_class(benefit_name=benefit_name, discount_modifier=discount_modifier)
                    new_benefit.save()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Пільгу успішно додано")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

            # Зміна існуючого об'єкта
            else:
                if benefit_name == self.instance.benefit_name and discount_modifier == self.instance.discount_modifier:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Ви не внесли жодних змін")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                # Перевірка унікальності назви
                existing_benefits = [benefit.benefit_name for benefit in self.model_class.get_all() if
                                     benefit.benefit_id != self.instance.benefit_id]
                if benefit_name in existing_benefits:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка",
                                          "Пільга з такою назвою вже існує")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    return
                try:
                    self.instance.benefit_name = benefit_name
                    self.instance.discount_modifier = discount_modifier
                    self.instance.update()
                    msg_box = QMessageBox(QMessageBox.Icon.Information, "Успіх", "Пільгу успішно змінено")
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()
                    self.close()
                except Exception as e:
                    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Помилка", str(e))
                    msg_box.setStyleSheet(message_box_style)
                    msg_box.exec()

        # Підключення кнопки до команди
        add_edit_button.clicked.connect(save_benefit)

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
