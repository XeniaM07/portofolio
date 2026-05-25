from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap

from components.header import Header


class HomePage(QWidget):
    logo_clicked = Signal()
    search_clicked = Signal()
    analyze_clicked = Signal()
    quiz_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = None
        self.header = None
        self.content_layout = None
        self.left_widget = None
        self.left_layout = None
        self.title_label = None
        self.subtitle_label = None
        self.paragraph_label = None
        self.right_widget = None
        self.right_layout = None
        self.image_label = None
        self.pixmap = None
        self.question_label = None
        self.buttons_container = None
        self.buttons_layout = None
        self.first_row_layout = None
        self.search_button = None
        self.analyze_button = None
        self.second_row_layout = None
        self.quiz_button = None

        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_header()
        self.setup_content()

    def setup_header(self):
        self.header = Header(self)
        self.header.logo_clicked.connect(self.logo_clicked.emit)
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.header)

    def setup_content(self):
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(30)
        self.main_layout.addLayout(self.content_layout)

        self.setup_left_section()
        self.setup_right_section()

    def setup_left_section(self):
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setSpacing(10)

        self.title_label = QLabel("Vincent van Gogh")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; background: transparent;")

        self.subtitle_label = QLabel("(1853–1890)")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("color: white; background: transparent;")

        self.paragraph_label = QLabel(
            "He was a visionary post-impressionist painter, renowned for his emotionally charged brushwork, vibrant color palettes, and deeply expressive style. "
            "Though underappreciated during his lifetime, he is now celebrated as one of the most influential figures in Western art.\n\n"
            "GoghVision is an intelligent application that analyzes and classifies artworks using advanced image processing and machine learning. "
            "Designed to recognize Van Gogh's unique artistic signature, the app identifies whether a painting is his, and if so, reveals contextual details such as the painting's likely period or location of origin."
        )
        self.paragraph_label.setAlignment(Qt.AlignJustify)
        self.paragraph_label.setWordWrap(True)
        self.paragraph_label.setStyleSheet("color: white; background: transparent;")
        self.paragraph_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.left_layout.addWidget(self.title_label)
        self.left_layout.addWidget(self.subtitle_label)
        self.left_layout.addWidget(self.paragraph_label)

        self.content_layout.addWidget(self.left_widget, 3)

    def setup_right_section(self):
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(15)

        self.setup_image()
        self.setup_question_label()
        self.setup_buttons()

        self.content_layout.addWidget(self.right_widget, 2)

    def setup_image(self):
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("border: 1px solid white;")
        self.pixmap = QPixmap("assets/home.jpg")
        self.right_layout.addWidget(self.image_label)

    def setup_question_label(self):
        self.question_label = QLabel("What's next?")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("color: white; background: transparent;")
        self.question_label.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(self.question_label)

    def setup_buttons(self):
        self.buttons_container = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_container)
        self.buttons_layout.setSpacing(10)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_first_button_row()
        self.setup_second_button_row()
        self.apply_button_styles()

        self.right_layout.addWidget(self.buttons_container)

    def setup_first_button_row(self):
        self.first_row_layout = QHBoxLayout()
        self.search_button = QPushButton("Search a painting")
        self.search_button.clicked.connect(self.search_clicked.emit)

        self.analyze_button = QPushButton("Analyze a painting")
        self.analyze_button.clicked.connect(self.analyze_clicked.emit)

        self.first_row_layout.addWidget(self.search_button)
        self.first_row_layout.addWidget(self.analyze_button)
        self.buttons_layout.addLayout(self.first_row_layout)

    def setup_second_button_row(self):
        self.second_row_layout = QHBoxLayout()
        self.quiz_button = QPushButton("Take quiz")
        self.quiz_button.clicked.connect(self.quiz_clicked.emit)

        self.second_row_layout.addStretch(1)
        self.second_row_layout.addWidget(self.quiz_button, 2)
        self.second_row_layout.addStretch(1)
        self.buttons_layout.addLayout(self.second_row_layout)

    def apply_button_styles(self):
        button_style = """
            QPushButton {
                background-color: #3366cc;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5588ee;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #2255bb;
            }
        """

        for btn in (self.search_button, self.analyze_button, self.quiz_button):
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.width()
        height = self.height()

        self.update_fonts(width)
        self.update_button_sizes(width, height)
        self.update_image_size()
        self.update_spacing(height)

    def update_fonts(self, width):
        title_font_size = max(15, min(34, int(width * 0.026)))
        subtitle_font_size = max(13, min(22, int(width * 0.016)))
        paragraph_font_size = max(12, min(18, int(width * 0.016)))

        self.title_label.setFont(QFont("Times New Roman", title_font_size, QFont.Weight.Bold))
        self.subtitle_label.setFont(QFont("Times New Roman", subtitle_font_size))
        self.paragraph_label.setFont(QFont("Segoe UI", paragraph_font_size))

    def update_button_sizes(self, width, height):
        min_btn_width = 140
        max_btn_width = 200
        btn_width = max(min_btn_width, min(max_btn_width, int(width * 0.12)))

        min_btn_height = 35
        max_btn_height = 50
        btn_height = max(min_btn_height, min(max_btn_height, int(height * 0.06)))

        btn_font_size = max(10, min(14, int(width * 0.011)))

        for btn in (self.search_button, self.analyze_button, self.quiz_button):
            btn.setMinimumSize(btn_width, btn_height)
            btn.setMaximumHeight(btn_height)

            if btn in (self.search_button, self.analyze_button):
                btn.setMaximumWidth(16777215)
            else:
                btn.setMaximumWidth(btn_width)

            font = QFont("Segoe UI", btn_font_size, QFont.Weight.Bold)
            btn.setFont(font)

    def update_image_size(self):
        if not self.pixmap.isNull():
            available_width = int(self.right_widget.width() * 0.9)
            available_height = int(self.right_widget.height() * 0.5)

            max_width = max(200, min(400, available_width))
            max_height = max(150, min(300, available_height))

            scaled_pixmap = self.pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def update_spacing(self, height):
        new_spacing = max(10, min(20, int(height * 0.02)))
        self.buttons_layout.setSpacing(new_spacing)

    def on_button_clicked(self):
        sender = self.sender()
        if sender == self.search_button:
            print("Search a painting button clicked")
        elif sender == self.analyze_button:
            print("Analyze a painting button clicked")
        elif sender == self.quiz_button:
            print("Take quiz button clicked")