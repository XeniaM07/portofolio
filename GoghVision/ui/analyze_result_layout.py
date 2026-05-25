from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSizePolicy, QScrollArea, QSpacerItem
)
from PySide6.QtGui import QFont, QColor, QPalette

from components.header import Header
from utils.helpers import create_back_layout

class AnalyzeResultLayoutMixin:
    logo_clicked = Signal()
    back_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.header = None
        self.back_button = None
        self.back_label = None
        self.image_label = None
        self.details_widget = None
        self.details_layout = None
        self.label_question = None
        self.label_yes_no = None
        self.label_year = None
        self.label_location = None
        self.buttons = {}
        self.dominant_colors_label = None
        self.heatmap_label = None
        self.diagram_label = None
        self.visuals_container = None
        self.visuals_layout = None
        self.similar_container = None
        self.similar_layout = None
        self.similar_paintings_labels = []
        self.save_button = None

    def init_ui(self):
        self.set_background_color()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_header()
        self.setup_scrollable_content()

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setup_header(self):
        self.header = Header(self)
        self.header.logo_clicked.connect(self.logo_clicked.emit)
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.header)

    def setup_scrollable_content(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #333;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #666;
                border-radius: 6px;
                min-height: 20px;
            }
        """)

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        back_layout = create_back_layout(self, "Back to upload page")
        self.main_layout.addLayout(back_layout)
        self.back_button.clicked.connect(self.back_clicked.emit)

        self.setup_main_content(content_layout)

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

    def setup_main_content(self, content_layout):
        main_content_layout = QHBoxLayout()
        main_content_layout.setSpacing(20)
        main_content_layout.setContentsMargins(10, 0, 10, 0)

        self.setup_image_section(main_content_layout)
        self.setup_details_section(main_content_layout)

        content_layout.addLayout(main_content_layout)

    def setup_image_section(self, main_content_layout):
        image_container = QWidget()
        image_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        image_container.setMaximumWidth(450)
        image_container.setMinimumWidth(200)

        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)
        self.image_label.setMinimumSize(150, 150)
        self.image_label.setMaximumHeight(500)

        image_layout.addWidget(self.image_label)
        main_content_layout.addWidget(image_container)

    def setup_details_section(self, main_content_layout):
        self.details_widget = QWidget()
        self.details_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.details_widget.setMinimumWidth(300)

        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        self.details_layout.setSpacing(10)

        self.setup_classification_info()
        self.setup_visual_buttons()
        self.setup_visual_containers()
        self.setup_similar_paintings_container()
        self.setup_save_button()

        main_content_layout.addWidget(self.details_widget)

    def setup_classification_info(self):
        self.label_question = QLabel("Is this painted by Vincent van Gogh?")
        self.label_question.setStyleSheet("color: white; font-weight: bold;")
        self.label_question.setFont(QFont("Segoe UI", 13))
        self.label_question.setWordWrap(True)

        self.label_yes_no = QLabel()
        self.label_year = QLabel()
        self.label_location = QLabel()

        label_style = "color: #ccc; padding: 2px 0px;"
        label_font = QFont("Segoe UI", 10)

        for lbl in [self.label_yes_no, self.label_year, self.label_location]:
            lbl.setStyleSheet(label_style)
            lbl.setFont(label_font)
            lbl.setWordWrap(True)

        self.details_layout.addWidget(self.label_question)
        self.details_layout.addWidget(self.label_yes_no)
        self.details_layout.addWidget(self.label_year)
        self.details_layout.addWidget(self.label_location)
        self.details_layout.addSpacing(10)

    def setup_visual_buttons(self):
        button_names = ["Dominant Colors", "Heatmap", "Diagram of Classification", "Similar Paintings"]
        self.buttons = {}

        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(8)

        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()

        button_style = """
            QPushButton {
                background-color: #2e7dff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5591ff;
            }
        """

        for i, name in enumerate(button_names):
            btn = QPushButton(name)
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Segoe UI", 9))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(35)

            if i < 2:
                row1_layout.addWidget(btn)
            else:
                row2_layout.addWidget(btn)

            self.buttons[name] = btn

        buttons_layout.addLayout(row1_layout)
        buttons_layout.addLayout(row2_layout)
        self.details_layout.addWidget(buttons_container)

    def setup_visual_containers(self):
        self.dominant_colors_label = QLabel()
        self.heatmap_label = QLabel()
        self.diagram_label = QLabel()

        visual_style = """
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
        """

        for lbl in [self.dominant_colors_label, self.heatmap_label, self.diagram_label]:
            lbl.setStyleSheet(visual_style)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lbl.setScaledContents(False)
            lbl.setVisible(False)
            lbl.setMinimumSize(200, 200)
            lbl.setMaximumHeight(300)

        self.visuals_container = QWidget()
        self.visuals_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.visuals_layout = QVBoxLayout(self.visuals_container)
        self.visuals_layout.setContentsMargins(0, 0, 0, 0)
        self.visuals_layout.setSpacing(0)

        self.visuals_layout.addWidget(self.dominant_colors_label)
        self.visuals_layout.addWidget(self.heatmap_label)
        self.visuals_layout.addWidget(self.diagram_label)

        self.details_layout.addWidget(self.visuals_container)

    def setup_similar_paintings_container(self):
        self.similar_container = QWidget()
        self.similar_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.similar_container.setMaximumHeight(140)

        self.similar_layout = QHBoxLayout(self.similar_container)
        self.similar_layout.setSpacing(8)
        self.similar_layout.setContentsMargins(0, 5, 0, 5)

        similar_style = """
            QLabel {
                background-color: #2a2a2a;
                border: 2px solid #666;
                border-radius: 8px;
                padding: 2px;
            }
            QLabel:hover {
                border-color: #888;
            }
        """

        self.similar_paintings_labels = []
        for _ in range(5):
            lbl = QLabel()
            lbl.setMinimumSize(80, 80)
            lbl.setMaximumSize(120, 120)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lbl.setStyleSheet(similar_style)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setCursor(Qt.PointingHandCursor)
            lbl.setScaledContents(False)
            lbl.setVisible(False)

            self.similar_paintings_labels.append(lbl)
            self.similar_layout.addWidget(lbl)

        self.details_layout.addWidget(self.similar_container)

    def setup_save_button(self):
        self.details_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.setFixedHeight(40)
        self.save_button.setMaximumWidth(200)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3366cc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #4477cc;
                color: #ccc;
            }
        """)
        self.save_button.setFont(QFont("Segoe UI", 11))
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        save_layout = QHBoxLayout()
        save_layout.addStretch()
        save_layout.addWidget(self.save_button)
        save_layout.addStretch()
        self.details_layout.addLayout(save_layout)