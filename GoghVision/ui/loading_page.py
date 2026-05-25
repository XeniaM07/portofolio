import math
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPalette, QColor, QPixmap, QPainter, QFont
from PySide6.QtCore import Qt, QTimer, Signal

class LoadingPage(QWidget):
    loading_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.animated_logo_label = None
        self.layout = None
        self.quote_label = None
        self.animation_timer = None

        self.background_logo_pixmap = QPixmap("assets/logo.png")
        self.animated_logo_pixmap = QPixmap("assets/logo.png")

        self.scale_phase = 0.0
        self.scale_factor = 1.0

        self._scaled_bg_pixmap = None
        self._bg_pixmap_pos = None

        self.set_background_color()
        self.init_ui()
        self.start_animation_timer()

        self.loading_timer = QTimer(self)
        self.loading_timer.setSingleShot(True)
        self.loading_timer.timeout.connect(self._finish_loading)
        self.loading_timer.start(3000)

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        self.animated_logo_label = QLabel(self)
        self.animated_logo_label.setScaledContents(True)
        self.animated_logo_label.setStyleSheet("background: transparent;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(0)
        self.layout.addStretch()

        self.layout.addWidget(self.animated_logo_label, alignment=Qt.AlignCenter)

        self.layout.addStretch()

        self.quote_label = QLabel(
            "“Great things are not done by impulse, but by a series of small things brought together.”\n– Vincent van Gogh –"
        )
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_label.setStyleSheet("color: white;")
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        self.quote_label.setFont(font)
        self.layout.addWidget(self.quote_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_background_logo_cache()
        self.update_animated_logo()
        self.update_quote_font_size()

    def _update_background_logo_cache(self):
        if not self.background_logo_pixmap.isNull():
            max_width = int(self.width() * 0.9)
            max_height = int(self.height() * 0.9)

            self._scaled_bg_pixmap = self.background_logo_pixmap.scaled(
                max_width,
                max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._bg_pixmap_pos = (
                (self.width() - self._scaled_bg_pixmap.width()) // 2,
                (self.height() - self._scaled_bg_pixmap.height()) // 2,
            )
        else:
            self._scaled_bg_pixmap = None
            self._bg_pixmap_pos = None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._scaled_bg_pixmap and self._bg_pixmap_pos:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.setOpacity(0.1)
            painter.drawPixmap(self._bg_pixmap_pos[0], self._bg_pixmap_pos[1], self._scaled_bg_pixmap)

    def start_animation_timer(self):
        if not hasattr(self, "animation_timer") or self.animation_timer is None:
            self.animation_timer = QTimer(self)
            self.animation_timer.timeout.connect(self.animate_pulse)
        if not self.animation_timer.isActive():
            self.animation_timer.start(50)

    def stop_animation_timer(self):
        if self.animation_timer and self.animation_timer.isActive():
            self.animation_timer.stop()

    def animate_pulse(self):
        self.scale_phase += 0.1
        amplitude = 0.1
        self.scale_factor = 1.0 + amplitude * math.sin(self.scale_phase)
        self.update_animated_logo()

    def update_animated_logo(self):
        if self.animated_logo_pixmap.isNull():
            return

        base_size = int(min(self.width(), self.height()) * 0.5)
        scaled_size = int(base_size * self.scale_factor)

        scaled_pixmap = self.animated_logo_pixmap.scaled(
            scaled_size,
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.animated_logo_label.setPixmap(scaled_pixmap)
        self.animated_logo_label.setFixedSize(scaled_pixmap.size())

    def update_quote_font_size(self):
        quote_font_size = max(12, int(self.height() * 0.025))
        font = self.quote_label.font()
        font.setPointSize(quote_font_size)
        self.quote_label.setFont(font)

    def _finish_loading(self):
        self.stop_animation_timer()
        self.loading_finished.emit()