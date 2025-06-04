from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, 
                             QTextEdit, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random
import time

class InstructionsDialog(QDialog):
    """Dialog for displaying instructions."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instructions")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml(
            "<h2 style='color: #2f4f4f;'>Welcome to Flashcard Quiz App!</h2>"
            "<p style='color: #333;'>This app helps you create, manage, and test your knowledge with flashcards.</p>"
            "<p style='color: #333;'><b>How to Use:</b></p>"
            "<ul style='color: #333;'>"
            "<li><b>Add Flashcard:</b> Create new flashcards with questions and answers.</li>"
            "<li><b>Edit/Delete:</b> Modify or remove existing flashcards.</li>"
            "<li><b>List Flashcards:</b> View all flashcards in a table.</li>"
            "<li><b>Start Quiz:</b> Test yourself with a random order of questions.</li>"
            "<li><b>Timed Quiz:</b> Answer questions within a time limit per question.</li>"
            "<li><b>Stats:</b> Track your correct answers and overall performance.</li>"
            "</ul>"
            "<p style='color: #333;'>Click OK to close this window.</p>"
        )
        instructions.setStyleSheet("background-color: #f5faff; border: 1px solid #b0c4de; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #e6f3fa;")

class FlashcardDialog(QDialog):
    """Dialog for adding/editing flashcards."""
    def __init__(self, parent=None, question="", answer="", edit_mode=False):
        super().__init__(parent)
        self.setWindowTitle("Edit Flashcard" if edit_mode else "Add Flashcard")
        self.setFixedSize(350, 200)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Question:", styleSheet="color: #2f4f4f; font-weight: bold;"))
        self.question_input = QLineEdit(question)
        self.question_input.setPlaceholderText("Enter question")
        self.question_input.setStyleSheet("padding: 8px; border: 1px solid #b0c4de; border-radius: 5px; background-color: #fff;")
        layout.addWidget(self.question_input)

        layout.addWidget(QLabel("Answer:", styleSheet="color: #2f4f4f; font-weight: bold;"))
        self.answer_input = QLineEdit(answer)
        self.answer_input.setPlaceholderText("Enter answer")
        self.answer_input.setStyleSheet("padding: 8px; border: 1px solid #b0c4de; border-radius: 5px; background-color: #fff;")
        layout.addWidget(self.answer_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("background-color: #dc143c; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #e6f3fa;")

    def get_data(self):
        return self.question_input.text().strip(), self.answer_input.text().strip()

class QuizDialog(QDialog):
    """Dialog for running quiz (normal or timed)."""
    def __init__(self, parent, cards, timed=False, time_limit=10):
        super().__init__(parent)
        self.setWindowTitle("Timed Quiz" if timed else "Quiz")
        self.setFixedSize(450, 250)
        self.cards = cards
        self.timed = timed
        self.time_limit = time_limit
        self.current_card = 0
        self.correct = 0
        self.start_time = time.time()

        self.layout = QVBoxLayout()
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("color: #2f4f4f; padding: 10px;")
        self.layout.addWidget(self.question_label)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter your answer")
        self.answer_input.setStyleSheet("padding: 8px; border: 1px solid #b0c4de; border-radius: 5px; background-color: #fff;")
        self.layout.addWidget(self.answer_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        self.submit_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.layout.addWidget(self.submit_button)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("color: #333; font-style: italic; padding: 5px;")
        self.layout.addWidget(self.feedback_label)

        if timed:
            self.timer_label = QLabel(f"Time left: {time_limit}s")
            self.timer_label.setStyleSheet("color: #ff4500; font-weight: bold; padding: 5px;")
            self.layout.addWidget(self.timer_label)
            self.update_timer()

        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #e6f3fa;")
        self.next_question()

    def update_timer(self):
        if not self.timed or self.current_card >= len(self.cards):
            return
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        if remaining <= 0:
            self.feedback_label.setText("Time's up! Moving to next question.")
            self.submit_button.setDisabled(True)
            QTimer.singleShot(1000, self.next_question_enable_submit)
        else:
            self.timer_label.setText(f"Time left: {remaining:.1f}s")
            self.timer_label.repaint()
            QApplication.processEvents()
            QTimer.singleShot(100, self.update_timer)

    def next_question(self):
        if self.current_card >= len(self.cards):
            self.show_results()
            return
        self.question_label.setText(f"Question: {self.cards[self.current_card]['question']}")
        self.answer_input.clear()
        self.feedback_label.clear()
        self.start_time = time.time()
        self.current_card += 1

    def check_answer(self):
        if self.current_card > len(self.cards):
            return
        user_answer = self.answer_input.text().strip().lower()
        correct_answer = self.cards[self.current_card - 1]["answer"].lower()
        if user_answer == correct_answer:
            self.feedback_label.setText("Correct!")
            self.correct += 1
        else:
            self.feedback_label.setText(f"Wrong! Correct answer: {self.cards[self.current_card - 1]['answer']}")
        self.submit_button.setDisabled(True)
        QTimer.singleShot(1000, self.next_question_enable_submit)

    def next_question_enable_submit(self):
        self.submit_button.setEnabled(True)
        self.next_question()

    def show_results(self):
        total = len(self.cards)
        QMessageBox.information(self, "Quiz Results", 
                                f"Quiz finished! Score: {self.correct}/{total} ({self.correct/total*100:.1f}%)")
        self.accept()

class LandingPage(QWidget):
    """Landing page with welcome message and navigation."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Flashcard Quiz App!")
        welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #2f4f4f; margin: 20px;")
        layout.addWidget(welcome_label)

        intro_label = QLabel("Test your knowledge with custom flashcards.\nCreate, edit, and quiz yourself in either normal or timed modes!")
        intro_label.setFont(QFont("Arial", 12))
        intro_label.setAlignment(Qt.AlignCenter)
        intro_label.setStyleSheet("color: #333; margin: 10px 20px;")
        layout.addWidget(intro_label)

        start_button = QPushButton("Start App")
        start_button.clicked.connect(self.parent.show_main)
        start_button.setStyleSheet("background-color: #4682b4; color: white; padding: 12px; border-radius: 5px; font-size: 14px; margin: 10px;")
        layout.addWidget(start_button)

        instructions_button = QPushButton("View Instructions")
        instructions_button.clicked.connect(self.show_instructions)
        instructions_button.setStyleSheet("background-color: #5f9ea0; color: white; padding: 12px; border-radius: 5px; font-size: 14px; margin: 10px;")
        layout.addWidget(instructions_button)

        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("background-color: #e6f3fa;")

    def show_instructions(self):
        dialog = InstructionsDialog(self)
        dialog.exec_()

class MainContent(QWidget):
    """Main content widget with flashcard management and quiz controls."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        layout = QVBoxLayout()

        # Buttons layout
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Flashcard")
        self.add_button.clicked.connect(self.add_flashcard)
        self.add_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Flashcard")
        self.edit_button.clicked.connect(self.edit_flashcard)
        self.edit_button.setStyleSheet("background-color: #5f9ea0; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Flashcard")
        self.delete_button.clicked.connect(self.delete_flashcard)
        self.delete_button.setStyleSheet("background-color: #dc143c; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.list_button = QPushButton("List Flashcards")
        self.list_button.clicked.connect(self.list_flashcards)
        self.list_button.setStyleSheet("background-color: #ff8c00; color: white; padding: 10px; border-radius: 5px; font-size: 14px; margin: 5px;")
        layout.addWidget(self.list_button)

        self.quiz_button = QPushButton("Start Quiz")
        self.quiz_button.clicked.connect(lambda: self.start_quiz(timed=False))
        self.quiz_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px; border-radius: 5px; font-size: 14px; margin: 5px;")
        layout.addWidget(self.quiz_button)

        self.timed_quiz_button = QPushButton("Start Timed Quiz")
        self.timed_quiz_button.clicked.connect(lambda: self.start_quiz(timed=True))
        self.timed_quiz_button.setStyleSheet("background-color: #5f9ea0; color: white; padding: 10px; border-radius: 5px; font-size: 14px; margin: 5px;")
        layout.addWidget(self.timed_quiz_button)

        self.instructions_button = QPushButton("Instructions")
        self.instructions_button.clicked.connect(self.show_instructions)
        self.instructions_button.setStyleSheet("background-color: #708090; color: white; padding: 10px; border-radius: 5px; font-size: 14px; margin: 5px;")
        layout.addWidget(self.instructions_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.parent.close)
        self.exit_button.setStyleSheet("background-color: #dc143c; color: white; padding: 10px; border-radius: 5px; font-size: 14px; margin: 5px;")
        layout.addWidget(self.exit_button)

        # Table for flashcards
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("border: 1px solid #b0c4de; background-color: #fff; margin: 10px;")
        layout.addWidget(self.table)

        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("font-weight: bold; color: #2f4f4f; margin: 10px;")
        layout.addWidget(self.stats_label)
        self.update_stats()

        self.setLayout(layout)

    def update_stats(self):
        stats = self.data["stats"]
        percent = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        self.stats_label.setText(f"Overall Stats: {stats['correct']}/{stats['total']} ({percent:.1f}%)")

    def add_flashcard(self):
        dialog = FlashcardDialog(self)
        if dialog.exec_():
            question, answer = dialog.get_data()
            if question and answer:
                self.data["flashcards"].append({"question": question, "answer": answer})
                self.parent.save_data()
                QMessageBox.information(self, "Success", "Flashcard added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Question and answer cannot be empty.")

    def edit_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
        self.list_flashcards()
        index, ok = QInputDialog.getInt(self, "Edit Flashcard", "Enter flashcard number to edit:", 1, 1, len(self.data["flashcards"]))
        if ok:
            index -= 1
            card = self.data["flashcards"][index]
            dialog = FlashcardDialog(self, card["question"], card["answer"], edit_mode=True)
            if dialog.exec_():
                question, answer = dialog.get_data()
                if question:
                    self.data["flashcards"][index]["question"] = question
                if answer:
                    self.data["flashcards"][index]["answer"] = answer
                self.parent.save_data()
                QMessageBox.information(self, "Success", "Flashcard updated successfully!")

    def delete_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
        self.list_flashcards()
        index, ok = QInputDialog.getInt(self, "Delete Flashcard", "Enter flashcard number to delete:", 1, 1, len(self.data["flashcards"]))
        if ok:
            self.data["flashcards"].pop(index - 1)
            self.parent.save_data()
            QMessageBox.information(self, "Success", "Flashcard deleted successfully!")
            self.list_flashcards()

    def list_flashcards(self):
        self.table.setRowCount(len(self.data["flashcards"]))
        for i, card in enumerate(self.data["flashcards"]):
            self.table.setItem(i, 0, QTableWidgetItem(card["question"]))
            self.table.setItem(i, 1, QTableWidgetItem(card["answer"]))

    def start_quiz(self, timed=False):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available. Add some first!")
            return
        cards = self.data["flashcards"].copy()
        random.shuffle(cards)
        time_limit = 10
        if timed:
            time_limit, ok = QInputDialog.getDouble(self, "Timed Quiz", "Enter time limit per question (seconds):", 10, 1, 60, 1)
            if not ok:
                return
        dialog = QuizDialog(self, cards, timed, time_limit)
        dialog.exec_()
        self.data["stats"]["correct"] += dialog.correct
        self.data["stats"]["total"] += len(cards)
        self.parent.save_data()
        self.update_stats()

    def show_instructions(self):
        dialog = InstructionsDialog(self)
        dialog.exec_()