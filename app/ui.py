from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, 
                             QTextEdit, QMessageBox, QInputDialog, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import random
import time

class AnimatedButton(QPushButton):
    """Custom animated button with hover effects."""
    def __init__(self, text, color_scheme="blue"):
        super().__init__(text)
        self.color_schemes = {
            "blue": {"normal": "#3498db", "hover": "#2980b9", "pressed": "#1f5f99"},
            "green": {"normal": "#2ecc71", "hover": "#27ae60", "pressed": "#1e8449"},
            "red": {"normal": "#e74c3c", "hover": "#c0392b", "pressed": "#a93226"},
            "orange": {"normal": "#f39c12", "hover": "#e67e22", "pressed": "#d35400"},
            "purple": {"normal": "#9b59b6", "hover": "#8e44ad", "pressed": "#7d3c98"},
            "teal": {"normal": "#1abc9c", "hover": "#16a085", "pressed": "#138d75"}
        }
        self.scheme = self.color_schemes.get(color_scheme, self.color_schemes["blue"])
        self.setup_style()
        self.setup_animation()

    def setup_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.scheme['normal']}, stop:1 {self.scheme['hover']});
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.scheme['hover']}, stop:1 {self.scheme['pressed']});
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: {self.scheme['pressed']};
                transform: translateY(0px);
            }}
        """)

    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self.animate_scale(1.05)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_scale(1.0)
        super().leaveEvent(event)

    def animate_scale(self, scale):
        rect = self.geometry()
        new_width = int(rect.width() * scale)
        new_height = int(rect.height() * scale)
        new_x = rect.x() - (new_width - rect.width()) // 2
        new_y = rect.y() - (new_height - rect.height()) // 2
        
        self.animation.setStartValue(rect)
        self.animation.setEndValue(QRect(new_x, new_y, new_width, new_height))
        self.animation.start()

class FadeInWidget(QWidget):
    """Widget with fade-in animation."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        
    def fade_in(self):
        self.fade_animation.start()

class AdminLoginDialog(QDialog):
    """Admin login dialog with modern styling."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Access")
        self.setFixedSize(400, 250)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Administrator Login")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter admin password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border: 2px solid #3498db;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                margin: 10px 20px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
                background: #f8f9fa;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = AnimatedButton("Login", "blue")
        self.login_button.clicked.connect(self.check_password)
        
        self.cancel_button = AnimatedButton("Cancel", "red")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                border-radius: 15px;
            }
        """)
        
        self.password_input.returnPressed.connect(self.check_password)
        
    def check_password(self):
        if self.password_input.text() == "admin123":  # Simple password
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Incorrect password!")
            self.password_input.clear()

class AdminPanel(QDialog):
    """Modern admin panel for flashcard management."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Panel - Flashcard Management")
        self.resize(800, 600)
        self.data = data
        self.parent_app = parent
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📚 Flashcard Admin Panel")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(header)
        
        # Button panel
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        self.add_button = AnimatedButton("➕ Add Flashcard", "green")
        self.add_button.clicked.connect(self.add_flashcard)
        
        self.edit_button = AnimatedButton("✏️ Edit Flashcard", "orange")
        self.edit_button.clicked.connect(self.edit_flashcard)
        
        self.delete_button = AnimatedButton("🗑️ Delete Flashcard", "red")
        self.delete_button.clicked.connect(self.delete_flashcard)
        
        self.refresh_button = AnimatedButton("🔄 Refresh", "purple")
        self.refresh_button.clicked.connect(self.refresh_table)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        
        layout.addWidget(button_frame)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                gridline-color: #bdc3c7;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 15px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.table)
        
        # Close button
        close_button = AnimatedButton("🚪 Close Admin Panel", "teal")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
            }
        """)
        
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.data["flashcards"]))
        for i, card in enumerate(self.data["flashcards"]):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(card["question"]))
            self.table.setItem(i, 2, QTableWidgetItem(card["answer"]))

    def add_flashcard(self):
        dialog = FlashcardDialog(self)
        if dialog.exec_():
            question, answer = dialog.get_data()
            if question and answer:
                self.data["flashcards"].append({"question": question, "answer": answer})
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "✅ Success", "Flashcard added successfully!")
            else:
                QMessageBox.warning(self, "⚠️ Error", "Question and answer cannot be empty.")

    def edit_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "⚠️ Error", "No flashcards available.")
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Error", "Please select a flashcard to edit.")
            return
            
        card = self.data["flashcards"][current_row]
        dialog = FlashcardDialog(self, card["question"], card["answer"], edit_mode=True)
        if dialog.exec_():
            question, answer = dialog.get_data()
            if question and answer:
                self.data["flashcards"][current_row]["question"] = question
                self.data["flashcards"][current_row]["answer"] = answer
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "✅ Success", "Flashcard updated successfully!")

    def delete_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "⚠️ Error", "No flashcards available.")
            return
            
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Error", "Please select a flashcard to delete.")
            return
            
        reply = QMessageBox.question(self, "🗑️ Delete Confirmation", 
                                   "Are you sure you want to delete this flashcard?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.data["flashcards"].pop(current_row)
            self.parent_app.save_data()
            self.refresh_table()
            QMessageBox.information(self, "✅ Success", "Flashcard deleted successfully!")

class InstructionsDialog(QDialog):
    """Modern instructions dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📖 Instructions")
        self.resize(600, 500)
        layout = QVBoxLayout()

        # Title
        title = QLabel("📚 Welcome to CodeCard Flashcard App!")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(title)

        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
            <div style='font-family: Arial; font-size: 14px; line-height: 1.6; color: #2c3e50;'>
                <h2 style='color: #3498db;'>🎯 How to Use the App</h2>
                <ul>
                    <li><b>🎮 Start Quiz:</b> Test yourself with randomized questions</li>
                    <li><b>⏱️ Timed Quiz:</b> Answer questions within a time limit</li>
                    <li><b>📊 View Stats:</b> Track your performance and progress</li>
                    <li><b>🔧 Admin Panel:</b> Access flashcard management (password: admin123)</li>
                </ul>
                
                <h2 style='color: #e74c3c;'>🔐 Admin Features</h2>
                <ul>
                    <li><b>➕ Add Flashcards:</b> Create new question-answer pairs</li>
                    <li><b>✏️ Edit Flashcards:</b> Modify existing flashcards</li>
                    <li><b>🗑️ Delete Flashcards:</b> Remove unwanted flashcards</li>
                    <li><b>📋 Manage Collection:</b> Full control over flashcard database</li>
                </ul>
                
                <h2 style='color: #27ae60;'>💡 Tips for Success</h2>
                <ul>
                    <li>Review flashcards regularly for better retention</li>
                    <li>Use timed quizzes to improve recall speed</li>
                    <li>Create clear, concise questions and answers</li>
                    <li>Track your progress using the stats feature</li>
                </ul>
            </div>
        """)
        instructions.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
            }
        """)
        layout.addWidget(instructions)

        ok_button = AnimatedButton("✅ Got It!", "green")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
            }
        """)

class FlashcardDialog(QDialog):
    """Modern flashcard add/edit dialog."""
    def __init__(self, parent=None, question="", answer="", edit_mode=False):
        super().__init__(parent)
        self.setWindowTitle("✏️ Edit Flashcard" if edit_mode else "➕ Add Flashcard")
        self.setFixedSize(500, 350)
        layout = QVBoxLayout()

        # Title
        title = QLabel("✏️ Edit Flashcard" if edit_mode else "➕ Create New Flashcard")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                padding: 15px;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        layout.addWidget(title)

        # Question input
        q_label = QLabel("📝 Question:")
        q_label.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 14px; margin: 5px;")
        layout.addWidget(q_label)
        
        self.question_input = QLineEdit(question)
        self.question_input.setPlaceholderText("Enter your question here...")
        self.question_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border: 2px solid #3498db;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                margin: 5px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
                background: #f8f9fa;
            }
        """)
        layout.addWidget(self.question_input)

        # Answer input
        a_label = QLabel("✅ Answer:")
        a_label.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 14px; margin: 5px;")
        layout.addWidget(a_label)
        
        self.answer_input = QLineEdit(answer)
        self.answer_input.setPlaceholderText("Enter the correct answer...")
        self.answer_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border: 2px solid #27ae60;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                margin: 5px;
            }
            QLineEdit:focus {
                border-color: #229954;
                background: #f8f9fa;
            }
        """)
        layout.addWidget(self.answer_input)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.ok_button = AnimatedButton("💾 Save", "green")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = AnimatedButton("❌ Cancel", "red")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
                border-radius: 15px;
            }
        """)

    def get_data(self):
        return self.question_input.text().strip(), self.answer_input.text().strip()

class QuizDialog(QDialog):
    """Modern quiz dialog with animations."""
    def __init__(self, parent, cards, timed=False, time_limit=10):
        super().__init__(parent)
        self.setWindowTitle("⏱️ Timed Quiz" if timed else "🎯 Quiz Mode")
        self.resize(700, 500)
        self.cards = cards
        self.timed = timed
        self.time_limit = time_limit
        self.current_card = 0
        self.correct = 0
        self.start_time = time.time()

        self.layout = QVBoxLayout()
        
        # Progress indicator
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
        """)
        self.layout.addWidget(self.progress_label)

        # Question display
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background: white;
                padding: 30px;
                border: 3px solid #3498db;
                border-radius: 12px;
                margin: 15px;
                min-height: 100px;
            }
        """)
        self.layout.addWidget(self.question_label)

        # Answer input
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Type your answer here...")
        self.answer_input.setStyleSheet("""
            QLineEdit {
                padding: 20px;
                border: 3px solid #27ae60;
                border-radius: 10px;
                font-size: 16px;
                background: white;
                margin: 15px;
            }
            QLineEdit:focus {
                border-color: #229954;
                background: #f8f9fa;
            }
        """)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input)

        # Submit button
        self.submit_button = AnimatedButton("🚀 Submit Answer", "blue")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        self.layout.addWidget(self.feedback_label)

        # Timer for timed quizzes
        if timed:
            self.timer_label = QLabel(f"⏰ Time left: {time_limit}s")
            self.timer_label.setAlignment(Qt.AlignCenter)
            self.timer_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #e74c3c;
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    margin: 10px;
                }
            """)
            self.layout.addWidget(self.timer_label)
            self.update_timer()

        self.setLayout(self.layout)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
            }
        """)
        self.next_question()

    def update_progress(self):
        self.progress_label.setText(f"📊 Question {self.current_card + 1} of {len(self.cards)} | Score: {self.correct}/{self.current_card}")

    def update_timer(self):
        if not self.timed or self.current_card >= len(self.cards):
            return
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        if remaining <= 0:
            self.feedback_label.setText("⏰ Time's up! Moving to next question...")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #e74c3c;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 8px;
                    margin: 10px;
                }
            """)
            self.submit_button.setDisabled(True)
            QTimer.singleShot(2000, self.next_question_enable_submit)
        else:
            self.timer_label.setText(f"⏰ Time left: {remaining:.1f}s")
            if remaining <= 5:
                self.timer_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: #c0392b;
                        padding: 10px;
                        border-radius: 8px;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 10px;
                        animation: blink 1s infinite;
                    }
                """)
            QTimer.singleShot(100, self.update_timer)

    def next_question(self):
        if self.current_card >= len(self.cards):
            self.show_results()
            return
        
        self.update_progress()
        self.question_label.setText(f"❓ {self.cards[self.current_card]['question']}")
        self.answer_input.clear()
        self.answer_input.setFocus()
        self.feedback_label.clear()
        self.start_time = time.time()

    def check_answer(self):
        if self.current_card >= len(self.cards):
            return
            
        user_answer = self.answer_input.text().strip().lower()
        correct_answer = self.cards[self.current_card]["answer"].lower()
        
        if user_answer == correct_answer:
            self.feedback_label.setText("✅ Correct! Well done!")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #27ae60;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px;
                }
            """)
            self.correct += 1
        else:
            self.feedback_label.setText(f"❌ Wrong! Correct answer: {self.cards[self.current_card]['answer']}")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #e74c3c;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px;
                }
            """)
        
        self.current_card += 1
        self.submit_button.setDisabled(True)
        QTimer.singleShot(2000, self.next_question_enable_submit)

    def next_question_enable_submit(self):
        self.submit_button.setEnabled(True)
        self.next_question()

    def show_results(self):
        total = len(self.cards)
        percentage = (self.correct / total) * 100
        
        if percentage >= 80:
            emoji = "🏆"
            message = "Excellent work!"
        elif percentage >= 60:
            emoji = "🎉"
            message = "Good job!"
        else:
            emoji = "📚"
            message = "Keep practicing!"
            
        QMessageBox.information(self, f"{emoji} Quiz Complete!", 
                              f"{message}\n\nFinal Score: {self.correct}/{total} ({percentage:.1f}%)")
        self.accept()

class LandingPage(FadeInWidget):
    """Modern landing page with animations."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()
        
        # Spacer
        layout.addItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Main title
        welcome_label = QLabel("🎓 CodeCard Flashcard App")
        welcome_label.setFont(QFont("Arial", 32, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                padding: 30px;
                border-radius: 15px;
                margin: 20px;
                border: 3px solid #2980b9;
            }
        """)
        layout.addWidget(welcome_label)

        # Subtitle
        intro_label = QLabel("🚀 Master Your Knowledge with Interactive Flashcards\n💡 Create, Study, and Excel!")
        intro_label.setFont(QFont("Arial", 16))
        intro_label.setAlignment(Qt.AlignCenter)
        intro_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background: rgba(255, 255, 255, 0.9);
                padding: 25px;
                border-radius: 12px;
                margin: 15px 40px;
                border: 2px solid #3498db;
                line-height: 1.6;
            }
        """)
        layout.addWidget(intro_label)

        # Button container
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        
        # Start button
        start_button = AnimatedButton("🎯 Start Learning", "blue")
        start_button.clicked.connect(self.parent.show_main)
        start_button.setMinimumHeight(60)
        button_layout.addWidget(start_button)

        # Instructions button
        instructions_button = AnimatedButton("📖 View Instructions", "teal")
        instructions_button.clicked.connect(self.show_instructions)
        instructions_button.setMinimumHeight(60)
        button_layout.addWidget(instructions_button)

        # Admin button
        admin_button = AnimatedButton("🔧 Admin Panel", "purple")
        admin_button.clicked.connect(self.show_admin_login)
        admin_button.setMinimumHeight(60)
        button_layout.addWidget(admin_button)

        layout.addWidget(button_container)
        layout.addItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #74b9ff, stop:0.5 #0984e3, stop:1 #74b9ff);
            }
        """)
        
        # Start fade-in animation
        QTimer.singleShot(100, self.fade_in)

    def show_instructions(self):
        dialog = InstructionsDialog(self)
        dialog.exec_()
        
    def show_admin_login(self):
        login_dialog = AdminLoginDialog(self)
        if login_dialog.exec_():
            admin_panel = AdminPanel(self.parent, self.parent.data)
            admin_panel.exec_()

class MainContent(FadeInWidget):
    """Modern main content with large buttons and animations."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        layout = QVBoxLayout()

        # Header section
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        # Title
        title = QLabel("📚 Flashcard Learning Center")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                padding: 25px;
                border-radius: 12px;
                margin: 15px;
                border: 2px solid #2980b9;
            }
        """)
        header_layout.addWidget(title)
        
        # Stats display
        self.stats_label = QLabel("")
        self.stats_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
                border: 2px solid #27ae60;
            }
        """)
        header_layout.addWidget(self.stats_label)
        
        layout.addWidget(header_frame)

        # Main buttons section
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        
        # Quiz buttons
        quiz_frame = QFrame()
        quiz_layout = QHBoxLayout(quiz_frame)
        
        self.quiz_button = AnimatedButton("🎯 Start Quiz", "blue")
        self.quiz_button.clicked.connect(lambda: self.start_quiz(timed=False))
        self.quiz_button.setMinimumHeight(80)
        self.quiz_button.setMinimumWidth(300)
        quiz_layout.addWidget(self.quiz_button)

        self.timed_quiz_button = AnimatedButton("⏱️ Timed Challenge", "orange")
        self.timed_quiz_button.clicked.connect(lambda: self.start_quiz(timed=True))
        self.timed_quiz_button.setMinimumHeight(80)
        self.timed_quiz_button.setMinimumWidth(300)
        quiz_layout.addWidget(self.timed_quiz_button)
        
        buttons_layout.addWidget(quiz_frame)

        # View flashcards button
        self.view_button = AnimatedButton("📋 View All Flashcards", "teal")
        self.view_button.clicked.connect(self.show_flashcards)
        self.view_button.setMinimumHeight(70)
        buttons_layout.addWidget(self.view_button)

        # Utility buttons
        utility_frame = QFrame()
        utility_layout = QHBoxLayout(utility_frame)
        
        self.instructions_button = AnimatedButton("📖 Instructions", "purple")
        self.instructions_button.clicked.connect(self.show_instructions)
        self.instructions_button.setMinimumHeight(60)
        utility_layout.addWidget(self.instructions_button)

        self.admin_button = AnimatedButton("🔧 Admin Panel", "green")
        self.admin_button.clicked.connect(self.show_admin_login)
        self.admin_button.setMinimumHeight(60)
        utility_layout.addWidget(self.admin_button)

        self.back_button = AnimatedButton("🏠 Back to Home", "red")
        self.back_button.clicked.connect(self.parent.show_landing)
        self.back_button.setMinimumHeight(60)
        utility_layout.addWidget(self.back_button)
        
        buttons_layout.addWidget(utility_frame)
        layout.addWidget(buttons_frame)

        # Flashcards table (initially hidden)
        self.table_frame = QFrame()
        self.table_frame.setVisible(False)
        table_layout = QVBoxLayout(self.table_frame)
        
        table_title = QLabel("📊 Flashcard Collection")
        table_title.setFont(QFont("Arial", 18, QFont.Bold))
        table_title.setAlignment(Qt.AlignCenter)
        table_title.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #229954);
                padding: 15px;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        table_layout.addWidget(table_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 3px solid #3498db;
                border-radius: 10px;
                gridline-color: #bdc3c7;
                font-size: 14px;
                margin: 10px;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 15px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        table_layout.addWidget(self.table)
        
        hide_table_button = AnimatedButton("👁️ Hide Flashcards", "red")
        hide_table_button.clicked.connect(self.hide_flashcards)
        table_layout.addWidget(hide_table_button)
        
        layout.addWidget(self.table_frame)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dfe6e9, stop:0.5 #b2bec3, stop:1 #dfe6e9);
            }
        """)
        
        self.update_stats()
        QTimer.singleShot(100, self.fade_in)

    def update_stats(self):
        stats = self.data["stats"]
        total_cards = len(self.data["flashcards"])
        if stats["total"] > 0:
            percent = (stats["correct"] / stats["total"]) * 100
            self.stats_label.setText(
                f"📊 Performance: {stats['correct']}/{stats['total']} ({percent:.1f}%) | "
                f"📚 Total Cards: {total_cards}"
            )
        else:
            self.stats_label.setText(f"📚 Total Cards: {total_cards} | 🎯 Ready to start your first quiz!")

    def show_flashcards(self):
        if not self.data["flashcards"]:
            QMessageBox.information(self, "📚 No Flashcards", 
                                  "No flashcards available.\nUse the Admin Panel to add some!")
            return
            
        self.table.setRowCount(len(self.data["flashcards"]))
        for i, card in enumerate(self.data["flashcards"]):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(card["question"]))
            self.table.setItem(i, 2, QTableWidgetItem(card["answer"]))
        
        self.table_frame.setVisible(True)

    def hide_flashcards(self):
        self.table_frame.setVisible(False)

    def start_quiz(self, timed=False):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "⚠️ No Flashcards", 
                              "No flashcards available for quiz!\nPlease ask an admin to add some flashcards first.")
            return
            
        cards = self.data["flashcards"].copy()
        random.shuffle(cards)
        
        time_limit = 10
        if timed:
            time_limit, ok = QInputDialog.getDouble(
                self, "⏱️ Timed Quiz Setup", 
                "Enter time limit per question (seconds):", 
                10, 1, 60, 1
            )
            if not ok:
                return
                
        dialog = QuizDialog(self, cards, timed, time_limit)
        dialog.exec_()
        
        # Update stats
        self.data["stats"]["correct"] += dialog.correct
        self.data["stats"]["total"] += len(cards)
        self.parent.save_data()
        self.update_stats()

    def show_instructions(self):
        dialog = InstructionsDialog(self)
        dialog.exec_()
        
    def show_admin_login(self):
        login_dialog = AdminLoginDialog(self)
        if login_dialog.exec_():
            admin_panel = AdminPanel(self.parent, self.data)
            admin_panel.exec_()
            self.update_stats()