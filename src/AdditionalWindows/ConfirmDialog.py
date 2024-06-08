from PySide6.QtWidgets import QPushButton, QVBoxLayout, QDialog, QLabel, QHBoxLayout
from PySide6.QtGui import QFont, QPixmap, QCursor
from PySide6.QtCore import Qt


class ConfirmDialog(QDialog):
    def __init__(self, question, parent=None):
        super().__init__(parent)
        # Приховання назви вікна (верхньої панелі)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Встановлення фону в світло-голубий колір
        self.setStyleSheet("""background-color: qradialgradient(
                    spread: reflect, cx: 0.231, cy: 0.738364, radius: 0.343, 
                    fx: 0.267894, fy: 0.625, 
                    stop: 0.40113 rgba(0, 61, 173, 255), 
                    stop: 0.983051 rgba(58, 16, 145, 255), 
                    stop: 1 rgba(140, 255, 225, 255)
                    );
                    border: 1px solid white;
        """)

        # Встановлення розмірів вікна
        self.resize(1000, 300)

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
        text_font2 = QFont()
        text_font2.setFamily("appetite")
        text_font2.setPointSize(52)

        # Створення курсора-стрілочки
        arrow_pixmap = QPixmap("../resources/icons/custom_cursor.png")
        self.arrow_cursor = QCursor(arrow_pixmap)

        # Створення курсору для натискання
        click_cursor_pixmap = QPixmap("../resources/icons/click_cursor.png")
        self.click_cursor = QCursor(click_cursor_pixmap)

        # Встановлення курсора-стрілочки на початку
        self.setCursor(self.arrow_cursor)

        # Додати текстове повідомлення
        message_label = QLabel(question)
        message_label.setStyleSheet(text_style)
        message_label.setFont(text_font2)

        # Додати кнопки "Так" і "Ні"
        # Кнопка "Так"
        yes_button = QPushButton("Так")
        yes_button.setStyleSheet(button_style)
        yes_button.setFont(text_font2)

        # Підключення обробників подій для зміни курсора
        yes_button.enterEvent = self.on_enter_event
        yes_button.leaveEvent = self.on_leave_event

        # Кнопка "Ні"
        no_button = QPushButton("Ні")
        no_button.setStyleSheet(button_style)
        no_button.setFont(text_font2)

        # Підключення обробників подій для зміни курсора
        no_button.enterEvent = self.on_enter_event
        no_button.leaveEvent = self.on_leave_event

        # Підключення команд кнопок
        yes_button.clicked.connect(self.accept)
        no_button.clicked.connect(self.reject)

        # Розмістити кнопки горизонтально
        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Головний лейаут для діалогу
        layout = QVBoxLayout()
        layout.addWidget(message_label)
        layout.addLayout(button_layout)
        layout.setSpacing(30)

        self.setLayout(layout)

    # Функції зміни курсора
    def on_enter_event(self, event):
        self.setCursor(self.click_cursor)
        event.accept()

    def on_leave_event(self, event):
        self.setCursor(self.arrow_cursor)
        event.accept()
