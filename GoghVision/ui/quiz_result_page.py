from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout
from PySide6.QtGui import QFont, QPixmap, QColor, QPalette
from PySide6.QtCore import Qt, Signal
from components.header import Header
import os
from utils.helpers import setup_main_layout_with_header

class QuizResultPage(QWidget):
    logo_clicked = Signal()
    back_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.header = None
        self.main_layout = None
        self.scroll_layout = None
        self.title_label = None
        self.image_label = None
        self.description_label = None
        self.back_btn = None

        setup_main_layout_with_header(self)
        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent;")

        container = QWidget()
        container.setAutoFillBackground(True)
        palette = container.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        container.setPalette(palette)

        self.scroll_layout = QVBoxLayout(container)
        self.scroll_layout.setContentsMargins(60, 40, 60, 40)
        self.scroll_layout.setSpacing(25)

        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        self.title_label = QLabel("You are most like:")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.scroll_layout.addWidget(self.title_label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(self.image_label)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: white;")
        self.description_label.setFont(QFont("Segoe UI", 13))
        self.description_label.setAlignment(Qt.AlignJustify)
        self.scroll_layout.addWidget(self.description_label)

        self.scroll_layout.addSpacing(10)

        self.back_btn = QPushButton("Take the quiz again")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3366cc;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5588ee;
            }
        """)
        self.back_btn.setFixedSize(220, 45)
        self.back_btn.clicked.connect(self.back_clicked.emit)

        btn_container = QHBoxLayout()
        btn_container.addStretch(1)
        btn_container.addWidget(self.back_btn)
        btn_container.addStretch(1)
        self.scroll_layout.addLayout(btn_container)

    def display_result(self, result_data):
        painting_id = result_data["painting"]
        painting_title = painting_id.replace('_', ' ').title()

        self.title_label.setText(f"You are most like: {painting_title}")
        self.description_label.setText(result_data["description"])

        image_path = f"assets/{painting_id}.png"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
