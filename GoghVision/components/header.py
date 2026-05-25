from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap, QFont, QCursor
from PySide6.QtCore import Qt, Signal, QSize

class Header(QWidget):
    logo_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)

        self.logo_pixmap = QPixmap("assets/logo.png")
        if self.logo_pixmap.isNull():
            print("Error: assets/logo.png not found for Header.")

        self.main_layout = QHBoxLayout(self)
        self.logo_label = QLabel()
        self.quote_label = QLabel()

        self.init_ui()
        self.setStyleSheet("background-color: transparent")

    def init_ui(self):
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        self.main_layout.setSpacing(15)

        #logo.png va fi buton pentru home_page
        self.logo_label.setScaledContents(True)
        self.logo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logo_label.mousePressEvent = self._logo_mouse_press_event

        #spatiul pentru citat
        self.quote_label = QLabel("\"Great things are not done by impulse, but by a series of small things brought together.\"")
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.quote_label.setStyleSheet("color: white; font-size: 12px;")
        font = QFont("Arial", 12)
        font.setItalic(True)
        self.quote_label.setFont(font)
        self.quote_label.setWordWrap(True)

        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addWidget(self.quote_label)
        self.main_layout.addStretch()

        self.update_logo_and_quote_size()

    def _logo_mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.logo_clicked.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_logo_and_quote_size()

    def update_logo_and_quote_size(self):
        header_height = self.height()

        logo_size = int(header_height * 0.85)

        if not self.logo_pixmap.isNull():
            scaled_logo = self.logo_pixmap.scaled(
                logo_size, logo_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)
            self.logo_label.setFixedSize(scaled_logo.size())

        font_quote = self.quote_label.font()
        font_quote.setPointSize(max(10, int(header_height * 0.25)))
        self.quote_label.setFont(font_quote)

        available_width = (
            self.width()
            - self.logo_label.width()
            - self.main_layout.spacing()
            - self.main_layout.contentsMargins().left()
            - self.main_layout.contentsMargins().right()
        )

        self.quote_label.setMaximumWidth(max(1, int(available_width * 0.75)))