import os
from PySide6.QtCore import Qt, QTimer, QThread, QObject, Signal
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QLineEdit, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QFileDialog
)

from components.header import Header
from db_access import search_by_keyword_vangogh
from cbir import get_similar_vangogh_paintings
from core.feature_extractor import extract_features
from utils.helpers import run_worker_in_thread

class ImageSearchWorker(QObject):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            features = extract_features(self.image_path)
            results = get_similar_vangogh_paintings(features, top_n=10)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class SearchListPage(QWidget):
    logo_clicked = Signal()
    painting_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.header = None
        self.search_input = None
        self.search_by_image_button = None
        self.results_list = None
        self.image_search_thread = None
        self.image_worker = None

        self.main_window = None
        self._search_results_ready = False

        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.header = Header(self)
        self.header.logo_clicked.connect(self.logo_clicked.emit)
        layout.addWidget(self.header)

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(20, 10, 20, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Vincent van Gogh paintings...")
        self.search_input.setMinimumHeight(35)
        self.search_input.setStyleSheet("""
            background-color: #3366cc;
            color: white;
            border-radius: 5px;
            padding-left: 10px;
            font-size: 14px;
        """)
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_input.returnPressed.connect(self._trigger_delayed_search)

        self.search_by_image_button = QPushButton("Search by Image")
        self.search_by_image_button.setStyleSheet("""
            QPushButton {
                background-color: #5599ee;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4477dd;
            }
        """)
        self.search_by_image_button.setCursor(Qt.PointingHandCursor)
        self.search_by_image_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.search_by_image_button.clicked.connect(self.open_image_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_by_image_button)
        layout.addLayout(search_layout)

        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                color: white;
                font-size: 13px;
            }
            QListWidget::item:selected {
                background-color: #4444aa;
            }
        """)
        self.results_list.itemClicked.connect(self.on_item_selected)
        layout.addWidget(self.results_list)

    def set_main_window(self, main_window):
        self.main_window = main_window

    def _trigger_delayed_search(self):
        if self.main_window:
            self.main_window.show_loading_page()
            QTimer.singleShot(400, self.perform_search)
        else:
            self.perform_search()

    def perform_search(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            return

        self.results_list.clear()
        results = search_by_keyword_vangogh(keyword)

        for row in results:
            item = QListWidgetItem(f"{row[1]}")
            item.setData(Qt.UserRole, {
                "id": row[0],
                "title": row[1],
                "year": row[2],
                "location": row[3],
                "author": row[4],
                "image_path": row[5],
                "features": row[6],
                "dominant_colors_path": row[7],
                "heatmap_path": row[8],
                "classification_diagram_path": row[9]
            })
            if row[5]:
                pixmap = QPixmap(row[5]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item.setIcon(QIcon(pixmap))
            self.results_list.addItem(item)

        self._search_results_ready = True
        if self.main_window:
            self.main_window.show_search_list()

    def open_image_search(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select image to search", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return

        if self.main_window:
            self.main_window.show_loading_page()

        self.image_search_thread = QThread()
        self.image_worker = ImageSearchWorker(file_path)
        self.image_worker = ImageSearchWorker(file_path)
        self.image_search_thread = run_worker_in_thread(
            self.image_worker,
            self.on_image_search_finished,
            self.on_image_search_error
        )

    def on_image_search_finished(self, results):
        self.results_list.clear()
        for painting in results:
            item = QListWidgetItem(painting["title"])
            item.setData(Qt.UserRole, painting)

            if painting.get("image_path"):
                pixmap = QPixmap(painting["image_path"]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item.setIcon(QIcon(pixmap))

            self.results_list.addItem(item)

        self._search_results_ready = True
        if self.main_window:
            self.main_window.show_search_list()

    def on_image_search_error(self, message):
        print(f"Error during image search: {message}")
        if self.main_window:
            self.main_window.show_search_list()

    def on_item_selected(self, item):
        data = item.data(Qt.UserRole)
        if self.main_window:
            self.main_window.show_loading_then_detail(data)
        else:
            self.painting_selected.emit(data)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.width()
        target_width = int(width / 2.5)
        self.search_input.setMaximumWidth(target_width)
        self.search_input.setMinimumWidth(target_width)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._search_results_ready:
            self.clear_search_fields()

    def clear_search_fields(self):
        self._search_results_ready = False
        self.search_input.clear()
        self.results_list.clear()
