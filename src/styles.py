from PySide6.QtGui import QFont, QPixmap, QCursor
# Стилі
window_background_style = """
            QMainWindow {
                background-color: qradialgradient(
                    spread: reflect, cx: 0.231, cy: 0.738364, radius: 0.343, 
                    fx: 0.267894, fy: 0.625, 
                    stop: 0.40113 rgba(0, 61, 173, 255), 
                    stop: 0.983051 rgba(58, 16, 145, 255), 
                    stop: 1 rgba(140, 255, 225, 255)
                );
            }
        """
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
                    QPushButton:hover { background-color: rgba(255, 255, 255, 30); }
                    QPushButton:pressed { background-color: rgba(255, 255, 255, 100); }
                """
eye_button_style = """
                    QPushButton {
                        border: none;
                        background-color: transparent;
                    }     
                """
text_line_style = """
                    border-radius: 7px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: white;
                    color: white;
                    background-color: rgba(255, 255, 255, 0.25);
                """

combo_box_style = """
    QComboBox {
        border-radius: 7px;
        border-width: 1px;
        border-style: solid;
        border-color: white;
        color: white;
        background-color: rgba(255, 255, 255, 0.25);
    }
    QComboBox::item {
        text-align: center;
        background-color: rgba(255, 255, 255, 0.25);
    }
"""

# Шрифти
text_font1 = QFont()
text_font1.setFamily("appetite")
text_font1.setPointSize(100)

text_font2 = QFont()
text_font2.setFamily("appetite")
text_font2.setPointSize(52)

text_font3 = QFont()
text_font3.setFamily("Sitka Banner")
text_font3.setPointSize(100)
text_font3.setBold(True)

text_font4 = QFont()
text_font4.setFamily("Sitka Banner")
text_font4.setPointSize(50)

text_font5 = QFont()
text_font5.setFamily("appetite")
text_font5.setPointSize(38)

text_font6 = QFont()
text_font6.setFamily("Sitka Banner")
text_font6.setPointSize(35)

# Курсори
# Створення курсора-стрілочки
arrow_pixmap = QPixmap("../resources/icons/custom_cursor.png")
arrow_cursor = QCursor(arrow_pixmap)

# Створення курсору для натискання
click_cursor_pixmap = QPixmap("../resources/icons/click_cursor.png")
click_cursor = QCursor(click_cursor_pixmap)

# Створення курсору для текстових полів
text_cursor_pixmap = QPixmap("../resources/icons/text_cursor.png")
text_cursor = QCursor(text_cursor_pixmap)
