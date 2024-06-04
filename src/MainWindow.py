from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QPixmap, QCursor, QFontDatabase


# Настройки вікна програми
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Встановлення розмірів вікна
        self.setGeometry(0, 0, 2560, 1440)
        self.showFullScreen()

        # Встановлення назви вікна
        self.setWindowTitle("City Electric Transport Manager")

        # Встановлення іконки вікна
        icon = QIcon("../resources/icons/main_window_icon.svg")
        self.setWindowIcon(icon)

        # Встановлення градієнтного фону через стилі
        self.setStyleSheet("""
            QMainWindow {
                background-color: qradialgradient(
                    spread: reflect, cx: 0.231, cy: 0.738364, radius: 0.343, 
                    fx: 0.267894, fy: 0.625, 
                    stop: 0.40113 rgba(0, 61, 173, 255), 
                    stop: 0.983051 rgba(58, 16, 145, 255), 
                    stop: 1 rgba(140, 255, 225, 255)
                );
            }
        """)

        # Додавання шрифтів
        QFontDatabase.addApplicationFont("../resources/fonts/larisa-script.ttf")
        QFontDatabase.addApplicationFont("../resources/fonts/appetite-italic.ttf")

        # Створення курсора-стрілочки
        arrow_pixmap = QPixmap("../resources/icons/custom_cursor.png")
        self.arrow_cursor = QCursor(arrow_pixmap)

        # Створення курсору для натискання
        click_cursor_pixmap = QPixmap("../resources/icons/click_cursor.png")
        self.click_cursor = QCursor(click_cursor_pixmap)

        # Створення курсору для текстових полів
        text_cursor_pixmap = QPixmap("../resources/icons/text_cursor.png")
        self.text_cursor = QCursor(text_cursor_pixmap)

        # Встановлення курсора-стрілочки на початку
        self.setCursor(self.arrow_cursor)

        # Створення початкового віджета логіну
        self.show_login_widget()

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

    def show_login_widget(self):
        from LoginWidget import LoginWidget
        self.setCentralWidget(LoginWidget(self))

    def show_admin_widget(self):
        from AdminWidget import AdminWidget
        self.setCentralWidget(AdminWidget())

    def show_dispatcher_widget(self):
        from DispatcherWidget import DispatcherWidget
        self.setCentralWidget(DispatcherWidget())

    def show_driver_widget(self):
        from DriverWidget import DriverWidget
        self.setCentralWidget(DriverWidget())

    # Функція переходу до функціонала Касира
    def show_cashier_widget(self, employee):
        from CashierWidget import CashierWidget
        self.setCentralWidget(CashierWidget(self, employee))
