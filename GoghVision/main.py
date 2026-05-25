from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QMessageBox, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThread, Qt, QTimer

import os
import sys
import shutil

from ui.loading_page import LoadingPage
from ui.home_page import HomePage
from ui.search_list_page import SearchListPage
from ui.search_detail_page import SearchDetailsPage
from ui.analyze_upload_page import AnalyzeUploadPage
from ui.analyze_result_logic import AnalyzeResultPage
from ui.quiz_page import QuizPage
from ui.quiz_result_page import QuizResultPage

from worker import AnalysisWorker
from core.result_saver import save_analysis_result as finalize_analysis_and_save
from test_painting import calculate_result

def cleanup_temp_folder():
    shutil.rmtree("temp", ignore_errors=True)
    os.makedirs("temp", exist_ok=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gogh Vision")
        self.setGeometry(50, 50, 800, 700)

        self.thread = None
        self.worker = None
        self.latest_analysis_result = None

        cleanup_temp_folder()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.loading_page = LoadingPage()
        self.home_page = HomePage()
        self.search_list_page = SearchListPage()
        self.search_details_page = SearchDetailsPage()
        self.analyze_upload_page = AnalyzeUploadPage()
        self.analyze_result_page = AnalyzeResultPage()
        self.quiz_page = QuizPage()
        self.quiz_result_page = QuizResultPage()

        for page in [
            self.analyze_result_page, self.loading_page, self.home_page,
            self.search_list_page, self.search_details_page, self.analyze_upload_page,
            self.quiz_page, self.quiz_result_page
        ]:
            self.stacked_widget.addWidget(page)

        self.search_list_page.set_main_window(self)

        self.loading_page.loading_finished.connect(self.show_home_page)
        self.home_page.logo_clicked.connect(self.show_home_page)
        self.home_page.search_clicked.connect(self.show_search_list)
        self.home_page.analyze_clicked.connect(self.show_analyze_upload)
        self.home_page.quiz_clicked.connect(self.show_quiz)

        self.search_list_page.logo_clicked.connect(self.show_home_page)
        self.search_list_page.painting_selected.connect(self.show_search_details)

        self.search_details_page.back_clicked.connect(self.show_search_list)
        self.search_details_page.logo_clicked.connect(self.show_home_page)

        self.analyze_upload_page.logo_clicked.connect(self.show_home_page)
        self.analyze_upload_page.analyze_requested.connect(self.start_analysis)

        self.analyze_result_page.logo_clicked.connect(self.show_home_page)
        self.analyze_result_page.back_clicked.connect(self.show_analyze_upload)
        self.analyze_result_page.feedback_response.connect(self.handle_feedback_response)
        self.analyze_result_page.save_dominant_colors_clicked.connect(self.save_dominant_colors)
        self.analyze_result_page.save_heatmap_clicked.connect(self.save_heatmap)
        self.analyze_result_page.save_diagram_clicked.connect(self.save_diagram)
        self.analyze_result_page.save_similar_painting_clicked.connect(self.save_similar_painting)

        self.quiz_page.logo_clicked.connect(self.show_home_page)
        self.quiz_page.quiz_finished.connect(self.show_quiz_result)

        self.quiz_result_page.logo_clicked.connect(self.show_home_page)
        self.quiz_result_page.back_clicked.connect(self.restart_quiz_flow)

        self.stacked_widget.setCurrentWidget(self.loading_page)
        QTimer.singleShot(100, self.loading_page.start_animation_timer)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.loading_page.stop_animation_timer()

    def show_search_list(self):
        self.stacked_widget.setCurrentWidget(self.search_list_page)
        self.loading_page.stop_animation_timer()

    def show_search_details(self, painting_data):
        self.search_details_page.set_painting_data(painting_data)
        self.stacked_widget.setCurrentWidget(self.search_details_page)
        self.loading_page.stop_animation_timer()

    def show_analyze_upload(self):
        self.stacked_widget.setCurrentWidget(self.analyze_upload_page)
        self.loading_page.stop_animation_timer()

    def show_analyze_result(self, pixmap, info=None):
        self.analyze_result_page.set_image(pixmap)
        if info:
            self.analyze_result_page.set_classification_result(
                info.get('is_van_gogh', False),
                year=info.get('year'),
                location=info.get('location')
            )
        self.stacked_widget.setCurrentWidget(self.analyze_result_page)
        self.loading_page.stop_animation_timer()

    def show_quiz(self):
        self.stacked_widget.setCurrentWidget(self.quiz_page)

    def show_quiz_result(self, answers):
        result_data = calculate_result(answers)
        self.quiz_result_page.display_result(result_data)
        self.stacked_widget.setCurrentWidget(self.quiz_result_page)

    def start_analysis(self, pixmap):
        self.stacked_widget.setCurrentWidget(self.loading_page)
        self.loading_page.start_animation_timer()

        temp_path = os.path.join("temp", "temp_upload.jpg")
        pixmap.save(temp_path)

        self.thread = QThread()
        self.worker = AnalysisWorker(temp_path)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_analysis_finished(self, result):
        self.latest_analysis_result = result
        self.populate_analysis_result(result)
        self.stacked_widget.setCurrentWidget(self.analyze_result_page)
        self.loading_page.stop_animation_timer()

    def populate_analysis_result(self, result):
        self.analyze_result_page.set_image(QPixmap(result["image_path"]))
        self.analyze_result_page.set_classification_result(
            result.get("is_van_gogh", False),
            year=result.get("year"),
            location=result.get("location")
        )

        self.analyze_result_page.dominant_colors_label.setPixmap(
            QPixmap(result["dominant_colors_path"]).scaled(
                self.analyze_result_page.dominant_colors_label.size(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        self.analyze_result_page.heatmap_label.setPixmap(
            QPixmap(result["heatmap_path"]).scaled(
                self.analyze_result_page.heatmap_label.size(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        self.analyze_result_page.diagram_label.setPixmap(
            QPixmap(result["classification_diagram_path"]).scaled(
                self.analyze_result_page.diagram_label.size(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        self.analyze_result_page.set_similar_paintings(result.get("similar_paintings", []))

    def handle_feedback_response(self, is_confirmed):
        if not self.latest_analysis_result:
            return

        if is_confirmed:
            self.latest_analysis_result["selected_similar_index"] = (
                self.analyze_result_page.selected_similar_painting
            )
            finalize_analysis_and_save(
                self.latest_analysis_result["image_path"],
                self.latest_analysis_result
            )
        else:
            for key in ["image_path", "dominant_colors_path", "heatmap_path", "classification_diagram_path"]:
                try:
                    os.remove(self.latest_analysis_result[key])
                except Exception:
                    pass

    def on_analysis_error(self, message):
        self.loading_page.stop_animation_timer()

        QMessageBox.critical(
            self,
            "Error",
            f"Something went wrong during analysis:\n{message}"
        )

        self.show_analyze_upload()

    def save_pixmap(self, pixmap, default_name, dialog_title):
        if pixmap and not pixmap.isNull():
            filename, _ = QFileDialog.getSaveFileName(self, dialog_title, default_name, "PNG Files (*.png)")
            if filename:
                pixmap.save(filename)

    def save_dominant_colors(self):
        self.save_pixmap(self.analyze_result_page.dominant_colors_label.pixmap(), "dominant_colors.png", "Save Dominant Colors")

    def save_heatmap(self):
        self.save_pixmap(self.analyze_result_page.heatmap_label.pixmap(), "heatmap.png", "Save Heatmap")

    def save_diagram(self):
        self.save_pixmap(self.analyze_result_page.diagram_label.pixmap(), "diagram.png", "Save Classification Diagram")

    def save_similar_painting(self, index):
        label = self.analyze_result_page.similar_paintings_labels[index]
        self.save_pixmap(label.pixmap(), f"similar_{index + 1}.png", f"Save Similar Painting {index + 1}")

    def show_loading_page(self):
        self.stacked_widget.setCurrentWidget(self.loading_page)
        self.loading_page.start_animation_timer()

    def show_loading_then_detail(self, painting_data):
        self.show_loading_page()
        QTimer.singleShot(300, lambda: self.show_search_details(painting_data))

    def restart_quiz_flow(self):
        self.quiz_page.restart_quiz()
        self.stacked_widget.setCurrentWidget(self.quiz_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
