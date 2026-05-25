from PySide6.QtCore import QObject, Signal
from core.predictor import analyze_image as analyze_image_without_saving

class AnalysisWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            result = analyze_image_without_saving(self.image_path)
            result["image_path"] = self.image_path
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
