from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor, QPalette
from components.header import Header
from test_painting import QUESTIONS
from utils.helpers import setup_main_layout_with_header

class QuizPage(QWidget):
    logo_clicked = Signal()
    quiz_finished = Signal(list)

    def __init__(self):
        super().__init__()

        self.main_layout = None
        self.header = None
        self.content_layout = None
        self.progress_label = None
        self.question_label = None
        self.answers_group = None
        self.answers_buttons = []
        self.next_button = None

        self.current_question_index = 0
        self.answers = []

        self.set_background_color()
        self.init_ui()

    def set_background_color(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#000033"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        setup_main_layout_with_header(self)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(60, 40, 60, 40)
        self.content_layout.setSpacing(30)
        self.main_layout.addLayout(self.content_layout)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #ccccff;")
        self.progress_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.progress_label)

        self.question_label = QLabel("")
        self.question_label.setStyleSheet("color: white;")
        self.question_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.question_label)

        self.answers_group = QButtonGroup(self)
        self.answers_buttons = []

        for _ in range(4):
            btn = QRadioButton()
            btn.setStyleSheet("color: white;")
            btn.setFont(QFont("Segoe UI", 13))
            self.answers_group.addButton(btn)
            self.answers_buttons.append(btn)
            self.content_layout.addWidget(btn)

        self.next_button = QPushButton("Next Question")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #3366cc;
                color: white;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5588ee;
            }
        """)
        self.next_button.clicked.connect(self.next_question)
        self.content_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.load_question()

    def load_question(self):
        total = len(QUESTIONS)
        current = self.current_question_index + 1
        question_data = QUESTIONS[self.current_question_index]

        self.progress_label.setText(f"Question {current} of {total}")
        self.question_label.setText(question_data['question'])

        for i, answer in enumerate(question_data["answers"]):
            self.answers_buttons[i].setText(answer)
            self.answers_buttons[i].setVisible(True)

        for i in range(len(question_data["answers"]), 4):
            self.answers_buttons[i].setVisible(False)

        self.answers_group.setExclusive(False)
        for btn in self.answers_buttons:
            btn.setChecked(False)
        self.answers_group.setExclusive(True)

        self.next_button.setText("View Results" if current == total else "Next Question")

    def next_question(self):
        selected_btn = self.answers_group.checkedButton()
        if not selected_btn:
            return

        selected_index = self.answers_buttons.index(selected_btn)
        selected_letter = chr(ord('a') + selected_index)
        self.answers.append(selected_letter)

        self.current_question_index += 1
        if self.current_question_index >= len(QUESTIONS):
            self.quiz_finished.emit(self.answers)
        else:
            self.load_question()

    def restart_quiz(self):
        self.current_question_index = 0
        self.answers = []
        self.load_question()