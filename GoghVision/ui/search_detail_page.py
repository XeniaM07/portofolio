import threading
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QSpacerItem,
    QFileDialog, QScrollArea
)
from PySide6.QtGui import QPalette, QColor, QFont, QPixmap

from components.header import Header
from painting_info_api import get_painting_summary
from utils.helpers import create_back_layout

class SearchDetailsPage(QWidget):
    logo_clicked = Signal()
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_view = None
        self.main_layout = None
        self.header = None
        self.back_button = None
        self.back_label = None
        self.image_label = None
        self.pixmap = QPixmap()
        self.save_button = None
        self.details_widget = None
        self.details_layout = None
        self.name_label = None
        self.year_label = None
        self.location_label = None
        self.info_label = None
        self.info_scroll = None
        self.btn_colors = None
        self.btn_heatmap = None
        self.visuals_container = None
        self.visuals_layout = None
        self.dominant_colors_label = None
        self.heatmap_label = None
        self.save_diagram_button = None
        self._initial_size_set = False

        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header = Header(self)
        self.header.logo_clicked.connect(self.logo_clicked.emit)
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.header)

        self.main_layout.addLayout(create_back_layout(self, "Back to search page"))
        self.back_button.clicked.connect(self.back_clicked.emit)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(30)

        image_layout = QVBoxLayout()
        image_layout.setSpacing(10)

        self.image_label = QLabel()
        self.image_label.setStyleSheet("background-color: #1a1a1a; border: 1px solid white;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(250, 250)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.save_button = QPushButton("Save the painting")
        self.save_button.setStyleSheet("background-color: #3366cc; color: white; padding: 8px 16px; border: none; border-radius: 5px;")
        self.save_button.setFont(QFont("Segoe UI", 11))
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.save_button.clicked.connect(self.save_painting_image)

        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.save_button)
        content_layout.addLayout(image_layout, 1)

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        self.details_layout.setSpacing(6)

        self.name_label = QLabel("Name: ")
        self.year_label = QLabel("Year: ")
        self.location_label = QLabel("Location: ")

        for lbl in (self.name_label, self.year_label, self.location_label):
            lbl.setStyleSheet("color: white;")
            lbl.setFont(QFont("Segoe UI", 12))
            lbl.setWordWrap(True)
            self.details_layout.addWidget(lbl)

        self.info_label = QLabel("Loading painting info...")
        self.info_label.setStyleSheet("color: white;")
        self.info_label.setFont(QFont("Segoe UI", 12))
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignTop)

        self.info_scroll = QScrollArea()
        self.info_scroll.setWidgetResizable(True)
        self.info_scroll.setFixedHeight(120)
        self.info_scroll.setStyleSheet("border: none; background: transparent;")
        self.info_scroll.setWidget(self.info_label)

        self.details_layout.addWidget(self.info_scroll)

        self.btn_colors = QPushButton("Dominant Colors")
        self.btn_heatmap = QPushButton("Heatmap")

        for btn in (self.btn_colors, self.btn_heatmap):
            btn.setStyleSheet("background-color: #3366cc; color: white; padding: 8px 16px; border: none; border-radius: 5px;")
            btn.setFont(QFont("Segoe UI", 11))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.details_layout.addWidget(btn)

        self.visuals_container = QWidget()
        self.visuals_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.visuals_container.setFixedHeight(240)

        self.visuals_layout = QVBoxLayout(self.visuals_container)
        self.visuals_layout.setContentsMargins(0, 0, 0, 0)
        self.visuals_layout.setSpacing(10)

        self.dominant_colors_label = QLabel()
        self.heatmap_label = QLabel()

        for lbl in [self.dominant_colors_label, self.heatmap_label]:
            lbl.setStyleSheet("background-color: #111111; border: 1px solid white;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            lbl.setVisible(False)

        self.visuals_layout.addWidget(self.dominant_colors_label, alignment=Qt.AlignCenter)
        self.visuals_layout.addWidget(self.heatmap_label, alignment=Qt.AlignCenter)
        self.details_layout.addWidget(self.visuals_container)

        self.save_diagram_button = QPushButton("Save Diagram")
        self.save_diagram_button.setStyleSheet("background-color: #3366cc; color: white; padding: 6px 12px; border: none; border-radius: 5px;")
        self.save_diagram_button.setFont(QFont("Segoe UI", 10))
        self.save_diagram_button.setCursor(Qt.PointingHandCursor)
        self.save_diagram_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.save_diagram_button.clicked.connect(self.save_visible_diagram)
        self.details_layout.addWidget(self.save_diagram_button, alignment=Qt.AlignCenter)

        content_layout.addWidget(self.details_widget, 1)
        self.main_layout.addLayout(content_layout)

        self.btn_colors.clicked.connect(self.toggle_dominant_colors)
        self.btn_heatmap.clicked.connect(self.toggle_heatmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self._initial_size_set:
            self.setMinimumSize(self.width(), self.height())
            self._initial_size_set = True

        if not self.pixmap.isNull():
            self.image_label.setPixmap(self.pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

        label_size = int(self.visuals_container.height() * 0.9)
        for lbl in [self.dominant_colors_label, self.heatmap_label]:
            lbl.setFixedSize(label_size, label_size)
            if not lbl.pixmap().isNull():
                lbl.setPixmap(lbl.pixmap().scaled(
                    label_size, label_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))

    def toggle_dominant_colors(self):
        self.dominant_colors_label.setVisible(not self.dominant_colors_label.isVisible())
        self.heatmap_label.setVisible(False)

    def toggle_heatmap(self):
        self.heatmap_label.setVisible(not self.heatmap_label.isVisible())
        self.dominant_colors_label.setVisible(False)

    def save_visible_diagram(self):
        target_label = self.dominant_colors_label if self.dominant_colors_label.isVisible() else self.heatmap_label
        if target_label and not target_label.pixmap().isNull():
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)")
            if file_path:
                target_label.pixmap().save(file_path)

    def set_painting_data(self, data: dict):
        self.pixmap = QPixmap(data["image_path"])
        self.image_label.setPixmap(self.pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

        self.name_label.setText(f"Name: {data['title']}")
        self.year_label.setText(f"Year: {data['year'] or 'Unknown'}")
        self.location_label.setText(f"Location: {data['location'] or 'Unknown'}")
        self.info_label.setText("Loading info from Wikipedia...")

        self.dominant_colors_label.setPixmap(QPixmap(data["dominant_colors_path"]).scaled(
            self.dominant_colors_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.heatmap_label.setPixmap(QPixmap(data["heatmap_path"]).scaled(
            self.heatmap_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

        self.dominant_colors_label.setVisible(False)
        self.heatmap_label.setVisible(False)

        self.fetch_info_threaded(data["title"], data["author"])

    def fetch_info_threaded(self, title, artist):
        def worker():
            summary = get_painting_summary(title, artist)
            self.info_label.setText(summary)

        threading.Thread(target=worker, daemon=True).start()

    def save_painting_image(self):
        if not self.pixmap or self.pixmap.isNull():
            return

        title = self.name_label.text().replace("Name: ", "").strip()
        safe_title = "".join(c if c.isalnum() or c in " _-." else "_" for c in title)

        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Painting")
        if folder:
            save_path = f"{folder}/{safe_title}.png"
            self.pixmap.save(save_path)
