from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy
)
from PySide6.QtGui import QPalette, QColor, QPixmap, Qt, QFont
from PySide6.QtCore import Signal

from components.header import Header


class AnalyzeUploadPage(QWidget):
    logo_clicked = Signal()
    image_selected = Signal(QPixmap)
    analyze_requested = Signal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.header = None
        self.image_label = None
        self.button_layout = None
        self.upload_button = None
        self.upload_another_button = None

        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        self.header = Header(self)
        self.header.logo_clicked.connect(self.logo_clicked.emit)
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.header)

        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid white; background-color: #1a1a1a; color: white;")
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setFont(QFont("Segoe UI", 14))
        main_layout.addWidget(self.image_label, alignment=Qt.AlignHCenter)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(20)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Upload an image to analyze")
        self.upload_button.setStyleSheet("background-color: #3366cc; color: white; padding: 10px; border-radius: 5px;")
        self.upload_button.setCursor(Qt.PointingHandCursor)
        self.upload_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.upload_button)

        self.upload_another_button = QPushButton("Upload Another")
        self.upload_another_button.setStyleSheet("background-color: #5599ee; color: white; padding: 10px; border-radius: 5px;")
        self.upload_another_button.setCursor(Qt.PointingHandCursor)
        self.upload_another_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.upload_another_button.setVisible(False)
        self.upload_another_button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.upload_another_button)

        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image to analyze",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
                self.image_label.setText("")
                self.image_selected.emit(pixmap)

                self.upload_another_button.setVisible(True)
                self.upload_button.setText("Analyze")
                self.upload_button.clicked.disconnect()
                self.upload_button.clicked.connect(lambda: self.analyze_requested.emit(pixmap))

                self.resizeEvent(None)
            else:
                self.image_label.setText("Failed to load image")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        available_width = self.width()
        available_height = self.height()
        side = min(available_width, available_height) * 0.5
        side = max(200, min(500, int(side)))

        self.image_label.setFixedSize(side, side)

        if self.image_label.pixmap():
            scaled_pixmap = self.image_label.pixmap().scaled(
                side, side,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

        font_size = max(12, int(side * 0.06))
        self.image_label.setFont(QFont("Segoe UI", font_size))

        for btn in [self.upload_button, self.upload_another_button]:
            btn.setFont(QFont("Segoe UI", max(10, int(side * 0.05))))
            btn.setMinimumHeight(int(side * 0.15))
            btn.setMaximumHeight(int(side * 0.2))

    def showEvent(self, event):
        super().showEvent(event)
        self.reset_upload_form()

    def reset_upload_form(self):
        self.image_label.clear()
        self.image_label.setText("No image selected")
        self.upload_another_button.setVisible(False)

        self.upload_button.setText("Upload an image to analyze")
        try:
            self.upload_button.clicked.disconnect()
        except TypeError:
            pass

        self.upload_button.clicked.connect(self.open_file_dialog)