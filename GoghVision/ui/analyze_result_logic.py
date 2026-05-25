from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, Signal
import os

from ui.analyze_result_layout import AnalyzeResultLayoutMixin


def update_visual_pixmap(label):
    if not label or not hasattr(label, 'pixmap'):
        return

    pix = label.pixmap()
    if pix and not pix.isNull():
        current_size = label.size()
        if current_size.width() > 0 and current_size.height() > 0:
            scaled = pix.scaled(
                current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            label.setPixmap(scaled)


class AnalyzeResultPage(QWidget, AnalyzeResultLayoutMixin):
    save_diagram_clicked = Signal()
    save_dominant_colors_clicked = Signal()
    save_heatmap_clicked = Signal()
    save_similar_painting_clicked = Signal(int)
    feedback_response = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap()
        self.is_van_gogh = None
        self.current_view = None
        self.selected_similar_painting = 0
        self.feedback_timer = None
        self.min_image_size = 150
        self.max_image_size = 400

        self.init_ui()
        self.connect_signals()

    def connect_signals(self):
        self.buttons["Dominant Colors"].clicked.connect(self.toggle_dominant_colors)
        self.buttons["Heatmap"].clicked.connect(self.toggle_heatmap)
        self.buttons["Diagram of Classification"].clicked.connect(self.toggle_diagram)
        self.buttons["Similar Paintings"].clicked.connect(self.toggle_similar_paintings)
        self.save_button.clicked.connect(self.handle_save_clicked)

    def set_image(self, pixmap):
        self.original_pixmap = pixmap
        self.update_image_display()

    def update_image_display(self):
        if not self.original_pixmap.isNull():
            current_size = self.image_label.size()
            if current_size.width() > 0 and current_size.height() > 0:
                scaled = self.original_pixmap.scaled(
                    current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)

    def set_classification_result(self, is_van_gogh, year=None, location=None):
        self.is_van_gogh = is_van_gogh
        self.label_yes_no.setText("Yes" if is_van_gogh else "No")
        self.label_year.setText(f"Date(year/s): {year or 'Unknown'}")
        self.label_location.setText(f"Location: {location or 'Unknown'}")

        self.label_year.setVisible(is_van_gogh)
        self.label_location.setVisible(is_van_gogh)

        self.details_widget.updateGeometry()

    def toggle_view(self, view_key):
        all_labels = {
            "dominant_colors": self.dominant_colors_label,
            "heatmap": self.heatmap_label,
            "diagram": self.diagram_label
        }

        for key, label in all_labels.items():
            label.setVisible(key == view_key)

        if view_key in all_labels:
            update_visual_pixmap(all_labels[view_key])

        if view_key == "similar_paintings":
            for lbl in self.similar_paintings_labels:
                lbl.setVisible(True)
            self.select_similar_painting(0)
        else:
            for lbl in self.similar_paintings_labels:
                lbl.setVisible(False)

        self.current_view = view_key
        self.update_button_states()
        self.update_save_button_text()

    def update_button_states(self):
        states = {
            "Dominant Colors": "dominant_colors",
            "Heatmap": "heatmap",
            "Diagram of Classification": "diagram",
            "Similar Paintings": "similar_paintings"
        }
        for name, key in states.items():
            self.buttons[name].setEnabled(self.current_view != key)

    def toggle_dominant_colors(self):
        self.toggle_view("dominant_colors" if self.current_view != "dominant_colors" else None)

    def toggle_heatmap(self):
        self.toggle_view("heatmap" if self.current_view != "heatmap" else None)

    def toggle_diagram(self):
        self.toggle_view("diagram" if self.current_view != "diagram" else None)

    def toggle_similar_paintings(self):
        self.toggle_view("similar_paintings" if self.current_view != "similar_paintings" else None)

    def set_similar_paintings(self, paintings):
        visible_count = min(len(paintings), 5)

        for i in range(visible_count):
            painting = paintings[i]
            label = self.similar_paintings_labels[i]
            path = painting.get("image_path", "")

            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    current_size = label.size()
                    if current_size.width() > 0:
                        scaled_pixmap = pixmap.scaled(
                            current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        label.setPixmap(scaled_pixmap)
                label.setToolTip(painting.get("title", f"Painting {i + 1}"))
            else:
                label.setText("Missing")
                label.setPixmap(QPixmap())
                label.setToolTip("File not found")

            label.mousePressEvent = lambda event, index=i: self.select_similar_painting(index)

        for j in range(visible_count, len(self.similar_paintings_labels)):
            self.similar_paintings_labels[j].setVisible(False)

    def select_similar_painting(self, index):
        self.selected_similar_painting = index
        for i, lbl in enumerate(self.similar_paintings_labels):
            if lbl.isVisible():
                lbl.setStyleSheet("""
                    background-color: #2a2a2a;
                    border: 3px solid #3366cc;
                    border-radius: 8px;
                """ if i == index else """
                    background-color: #2a2a2a;
                    border: 2px solid #666666;
                    border-radius: 8px;
                """)

    def handle_save_clicked(self):
        match self.current_view:
            case "dominant_colors":
                self.save_dominant_colors_clicked.emit()
            case "heatmap":
                self.save_heatmap_clicked.emit()
            case "diagram":
                self.save_diagram_clicked.emit()
            case "similar_paintings":
                self.save_similar_painting_clicked.emit(self.selected_similar_painting)

    def update_save_button_text(self):
        names = {
            "dominant_colors": "Save Dominant Colors",
            "heatmap": "Save Heatmap",
            "diagram": "Save Diagram",
            "similar_paintings": "Save Similar Painting"
        }
        self.save_button.setText(names.get(self.current_view, "Save"))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, 'image_label'):
            self.update_image_display()

        if hasattr(self, 'current_view') and self.current_view:
            all_labels = {
                "dominant_colors": getattr(self, 'dominant_colors_label', None),
                "heatmap": getattr(self, 'heatmap_label', None),
                "diagram": getattr(self, 'diagram_label', None)
            }

            active_label = all_labels.get(self.current_view)
            if active_label and active_label.isVisible():
                update_visual_pixmap(active_label)

        if hasattr(self, 'similar_paintings_labels'):
            for label in self.similar_paintings_labels:
                if label.isVisible() and label.pixmap() and not label.pixmap().isNull():
                    current_size = label.size()
                    if current_size.width() > 0:
                        original_pixmap = label.pixmap()
                        scaled = original_pixmap.scaled(
                            current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        label.setPixmap(scaled)

    def showEvent(self, event):
        super().showEvent(event)
        self.reset_view()

        if hasattr(self, 'image_label'):
            self.update_image_display()

        if self.feedback_timer:
            self.feedback_timer.stop()
        self.feedback_timer = QTimer(self)
        self.feedback_timer.setSingleShot(True)
        self.feedback_timer.timeout.connect(self.show_feedback_popup)
        self.feedback_timer.start(5000)

    def show_feedback_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Feedback")
        msg.setText("Help us to improve. Was that a right classification?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec()
        self.feedback_response.emit(result == QMessageBox.Yes)

    def reset_view(self):
        self.current_view = None
        self.update_button_states()
        self.update_save_button_text()

        for label in [self.dominant_colors_label, self.heatmap_label, self.diagram_label]:
            label.setVisible(False)

        for lbl in self.similar_paintings_labels:
            lbl.setVisible(False)
