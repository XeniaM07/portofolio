import os
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread
from components.header import Header

LOCATION_YEAR_MAP = {
    "Arles": "1888–1889",
    "Paris": "1886–1888",
    "Saint Remy": "1889–1890",
    "Auvers sur Oise": "1890",
    "Nuenen": "1883–1885",
    "Unknown location": None
}

def infer_year_and_location(image_path):
    parts = image_path.split(os.sep)
    if "vanGogh" in parts:
        location = parts[-2]
        return location, LOCATION_YEAR_MAP.get(location)
    return None, None

def get_author(image_path):
    return "van_gogh" if "vanGogh" in image_path else "other"

def get_title(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]

def setup_main_layout_with_header(self):
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setContentsMargins(0, 0, 0, 0)
    self.main_layout.setSpacing(0)

    self.header = Header()
    self.header.logo_clicked.connect(self.logo_clicked.emit)
    self.main_layout.addWidget(self.header)

def create_back_layout(self, label_text="Back"):
    layout = QHBoxLayout()
    layout.setContentsMargins(20, 10, 20, 10)
    layout.setSpacing(5)

    self.back_button = QPushButton("◀")
    self.back_button.setCursor(Qt.PointingHandCursor)
    self.back_button.setFixedSize(30, 30)
    self.back_button.setStyleSheet("color: white; background: transparent; border: none; font-size: 24px;")

    self.back_label = QLabel(label_text)
    self.back_label.setStyleSheet("color: white;")
    self.back_label.setFont(QFont("Segoe UI", 12))
    self.back_label.setAlignment(Qt.AlignVCenter)

    layout.addWidget(self.back_button)
    layout.addWidget(self.back_label)
    layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

    return layout

def run_worker_in_thread(worker, on_finished, on_error):
    thread = QThread()
    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    worker.finished.connect(on_finished)
    worker.error.connect(on_error)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    thread.start()
    return thread
