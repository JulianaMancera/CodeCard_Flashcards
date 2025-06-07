from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QTextEdit, QMessageBox,
    QInputDialog, QFrame, QSpacerItem, QSizePolicy, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import random
import time
import os

class AnimatedButton(QPushButton):
    """Custom animated button with modern styling."""
    def __init__(self, text, color_scheme="blue"):
        super().__init__(text)
        self.color_schemes = {
            "blue": {"normal": "#2563eb", "hover": "#1d4ed8", "pressed": "#1e40af"},
            "green": {"normal": "#16a34a", "hover": "#15803d", "pressed": "#166534"},
            "red": {"normal": "#dc2626", "hover": "#b91c1c", "pressed": "#991b1b"},
            "orange": {"normal": "#f97316", "hover": "#ea580c", "pressed": "#c2410c"},
            "purple": {"normal": "#7c3aed", "hover": "#6d28d9", "pressed": "#5b21b6"},
            "teal": {"normal": "#14b8a6", "hover": "#0d9488", "pressed": "#0f766e"}
        }
        self.scheme = self.color_schemes.get(color_scheme, self.color_schemes["blue"])
        self.setup_style()
        self.setup_animation()

    def setup_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: {self.scheme['normal']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: {self.scheme['hover']};
            }}
            QPushButton:pressed {{
                background: {self.scheme['pressed']};
            }}
            QPushButton:focus {{
                outline: 2px solid #2563eb;
                outline-offset: 2px;
            }}
        """)

    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

    def enterEvent(self, event):
        self.animate_scale(1.03)
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
        self.fade_animation.setDuration(800)
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
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Administrator Login")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e293b; margin-bottom: 15px;")
        layout.addWidget(title)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter admin password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
        """)
        layout.addWidget(self.password_input)
        
        button_layout = QHBoxLayout()
        self.login_button = AnimatedButton("Login", "blue")
        self.login_button.clicked.connect(self.check_password)
        self.cancel_button = AnimatedButton("Cancel", "red")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.password_input.returnPressed.connect(self.check_password)
        
    def check_password(self):
        # Use environment variable for password in production
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        if self.password_input.text() == admin_password:
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Incorrect password.")
            self.password_input.clear()

class SettingsDialog(QDialog):
    """Dialog for app settings."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings")
        self.setFixedSize(400, 300)
        self.data = data
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("App Settings")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e293b; margin-bottom: 15px;")
        layout.addWidget(title)
        
        time_label = QLabel("Default Time Limit (seconds):")
        time_label.setStyleSheet("color: #1e293b; font-weight: bold;")
        layout.addWidget(time_label)
        
        self.time_input = QLineEdit(str(self.data["settings"]["default_time_limit"]))
        self.time_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        layout.addWidget(self.time_input)
        
        self.sound_checkbox = QCheckBox("Enable Sound")
        self.sound_checkbox.setChecked(self.data["settings"]["sound_enabled"])
        self.sound_checkbox.setStyleSheet("margin: 10px; color: #1e293b;")
        layout.addWidget(self.sound_checkbox)
        
        button_layout = QHBoxLayout()
        save_button = AnimatedButton("Save", "green")
        save_button.clicked.connect(self.save_settings)
        cancel_button = AnimatedButton("Cancel", "red")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_settings(self):
        try:
            time_limit = float(self.time_input.text())
            if time_limit < 1 or time_limit > 60:
                QMessageBox.warning(self, "Invalid Input", "Time limit must be between 1 and 60 seconds.")
                return
            self.data["settings"]["default_time_limit"] = time_limit
            self.data["settings"]["sound_enabled"] = self.sound_checkbox.isChecked()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for time limit.")

class AdminPanel(QDialog):
    """Modern admin panel for flashcard management."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Panel")
        self.resize(900, 650)
        self.data = data
        self.parent_app = parent
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("📚 Flashcard Management")
        header.setFont(QFont("Inter", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            color: white;
            background: #2563eb;
            padding: 15px;
            border-radius: 8px;
        """)
        layout.addWidget(header)
        
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)
        
        self.add_button = AnimatedButton("➕ Add", "green")
        self.add_button.clicked.connect(self.add_flashcard)
        self.edit_button = AnimatedButton("✏️ Edit", "orange")
        self.edit_button.clicked.connect(self.edit_flashcard)
        self.delete_button = AnimatedButton("🗑️ Delete", "red")
        self.delete_button.clicked.connect(self.delete_flashcard)
        self.refresh_button = AnimatedButton("🔄 Refresh", "purple")
        self.refresh_button.clicked.connect(self.refresh_table)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        layout.addWidget(button_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                gridline-color: #e5e7eb;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QTableWidget::item:selected {
                background: #2563eb;
                color: white;
            }
            QHeaderView::section {
                background: #2563eb;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
        
        close_button = AnimatedButton("🚪 Close", "teal")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
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
                QMessageBox.information(self, "Success", "Flashcard added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Question and answer cannot be empty.")

    def edit_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a flashcard to edit.")
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
                QMessageBox.information(self, "Success", "Flashcard updated successfully!")

    def delete_flashcard(self):
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
            
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a flashcard to delete.")
            return
            
        reply = QMessageBox.question(self, "Delete Confirmation",
                                   "Are you sure you want to delete this flashcard?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.data["flashcards"].pop(current_row)
            self.parent_app.save_data()
            self.refresh_table()
            QMessageBox.information(self, "Success", "Flashcard deleted successfully!")

class InstructionsDialog(QDialog):
    """Modern instructions dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📖 Instructions")
        self.resize(600, 500)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📚 Welcome to CodeCard!")
        title.setFont(QFont("Inter", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; background: #2563eb; padding: 15px; border-radius: 8px;")
        layout.addWidget(title)
        
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
            <div style='font-family: Inter, Arial; font-size: 14px; line-height: 1.6; color: #1e293b;'>
                <h2 style='color: #2563eb;'>🎯 Getting Started</h2>
                <ul>
                    <li><b>🎮 Start Quiz:</b> Test your knowledge with random questions</li>
                    <li><b>⏱️ Timed Quiz:</b> Challenge yourself with a time limit</li>
                    <li><b>📊 View Stats:</b> Track your progress and accuracy</li>
                    <li><b>🔧 Admin Panel:</b> Manage flashcards (ask admin for password)</li>
                </ul>
                <h2 style='color: #dc2626;'>🔐 Admin Features</h2>
                <ul>
                    <li><b>➕ Add:</b> Create new flashcards</li>
                    <li><b>✏️ Edit:</b> Update existing flashcards</li>
                    <li><b>🗑️ Delete:</b> Remove flashcards</li>
                </ul>
                <h2 style='color: #16a34a;'>💡 Tips</h2>
                <ul>
                    <li>Review regularly for better retention</li>
                    <li>Use timed quizzes to boost speed</li>
                    <li>Keep questions and answers clear and concise</li>
                </ul>
            </div>
        """)
        instructions.setStyleSheet("""
            QTextEdit {
                background: #f8fafc;
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout.addWidget(instructions)
        
        ok_button = AnimatedButton("✅ Got It!", "green")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)

class FlashcardDialog(QDialog):
    """Modern flashcard add/edit dialog."""
    def __init__(self, parent=None, question="", answer="", edit_mode=False):
        super().__init__(parent)
        self.setWindowTitle("✏️ Edit Flashcard" if edit_mode else "➕ Add Flashcard")
        self.setFixedSize(500, 350)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("✏️ Edit Flashcard" if edit_mode else "➕ Add Flashcard")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; background: #2563eb; padding: 12px; border-radius: 8px;")
        layout.addWidget(title)
        
        q_label = QLabel("📝 Question:")
        q_label.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 14px;")
        layout.addWidget(q_label)
        
        self.question_input = QLineEdit(question)
        self.question_input.setPlaceholderText("Enter question...")
        self.question_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
        """)
        layout.addWidget(self.question_input)
        
        a_label = QLabel("✅ Answer:")
        a_label.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 14px;")
        layout.addWidget(a_label)
        
        self.answer_input = QLineEdit(answer)
        self.answer_input.setPlaceholderText("Enter answer...")
        self.answer_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #16a34a;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #15803d;
                background: #f8fafc;
            }
        """)
        layout.addWidget(self.answer_input)
        
        button_layout = QHBoxLayout()
        self.ok_button = AnimatedButton("💾 Save", "green")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = AnimatedButton("❌ Cancel", "red")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
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
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: white;
                background: #2563eb;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(self.progress_label)
        
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Inter", 16, QFont.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            QLabel {
                color: #1e293b;
                background: white;
                padding: 20px;
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                min-height: 100px;
            }
        """)
        self.layout.addWidget(self.question_label)
        
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Type your answer...")
        self.answer_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #16a34a;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #15803d;
                background: #f8fafc;
            }
        """)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input)
        
        self.submit_button = AnimatedButton("🚀 Submit", "blue")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
        """)
        self.layout.addWidget(self.feedback_label)
        
        if timed:
            self.timer_label = QLabel(f"⏰ Time left: {time_limit}s")
            self.timer_label.setAlignment(Qt.AlignCenter)
            self.timer_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #dc2626;
                    padding: 10px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.layout.addWidget(self.timer_label)
            self.update_timer()
        
        self.setLayout(self.layout)
        self.next_question()

    def update_progress(self):
        self.progress_label.setText(f"📊 Question {self.current_card + 1}/{len(self.cards)} | Score: {self.correct}/{self.current_card}")

    def update_timer(self):
        if not self.timed or self.current_card >= len(self.cards):
            return
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        if remaining <= 0:
            self.feedback_label.setText("⏰ Time's up!")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #dc2626;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 6px;
                }
            """)
            self.submit_button.setDisabled(True)
            QTimer.singleShot(1500, self.next_question_enable_submit)
        else:
            self.timer_label.setText(f"⏰ Time left: {remaining:.1f}s")
            if remaining <= 5:
                self.timer_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: #b91c1c;
                        padding: 10px;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: bold;
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
            self.feedback_label.setText("✅ Correct!")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #16a34a;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 6px;
                }
            """)
            self.correct += 1
        else:
            self.feedback_label.setText(f"❌ Wrong! Answer: {self.cards[self.current_card]['answer']}")
            self.feedback_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background: #dc2626;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 6px;
                }
            """)
        self.current_card += 1
        self.submit_button.setDisabled(True)
        QTimer.singleShot(1500, self.next_question_enable_submit)

    def next_question_enable_submit(self):
        self.submit_button.setEnabled(True)
        self.next_question()

    def show_results(self):
        total = len(self.cards)
        percentage = (self.correct / total) * 100
        if percentage >= 80:
            emoji, message = "🏆", "Excellent!"
        elif percentage >= 60:
            emoji, message = "🎉", "Good job!"
        else:
            emoji, message = "📚", "Keep practicing!"
        QMessageBox.information(self, f"{emoji} Quiz Complete!",
                              f"{message}\nScore: {self.correct}/{total} ({percentage:.1f}%)")
        self.accept()

class LandingPage(FadeInWidget):
    """Modern landing page with animations."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        layout.addStretch()
        
        welcome_label = QLabel("🎓 CodeCard Flashcard App")
        welcome_label.setFont(QFont("Inter", 28, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            color: white;
            background: #2563eb;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #1d4ed8;
        """)
        layout.addWidget(welcome_label)
        
        intro_label = QLabel("🚀 Master Your Knowledge\n💡 Create, Study, Excel!")
        intro_label.setFont(QFont("Inter", 14))
        intro_label.setAlignment(Qt.AlignCenter)
        intro_label.setStyleSheet("""
            color: #1e293b;
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #d1d9e6;
        """)
        layout.addWidget(intro_label)
        
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(12)
        
        start_button = AnimatedButton("🎯 Start Learning", "blue")
        start_button.clicked.connect(self.parent.show_main)
        button_layout.addWidget(start_button)
        
        instructions_button = AnimatedButton("📖 Instructions", "teal")
        instructions_button.clicked.connect(self.show_instructions)
        button_layout.addWidget(instructions_button)
        
        admin_button = AnimatedButton("🔧 Admin Panel", "purple")
        admin_button.clicked.connect(self.show_admin_login)
        button_layout.addWidget(admin_button)
        
        layout.addWidget(button_container)
        layout.addStretch()
        
        self.setLayout(layout)
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
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(12)
        
        title = QLabel("📚 Flashcard Learning Center")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            background: #2563eb;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #1d4ed8;
        """)
        header_layout.addWidget(title)
        
        self.stats_label = QLabel("")
        self.stats_label.setFont(QFont("Inter", 14, QFont.Bold))
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            color: #1e293b;
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #16a34a;
        """)
        header_layout.addWidget(self.stats_label)
        
        layout.addWidget(header_frame)
        
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(12)
        
        quiz_frame = QFrame()
        quiz_layout = QHBoxLayout(quiz_frame)
        quiz_layout.setSpacing(12)
        
        self.quiz_button = AnimatedButton("🎯 Start Quiz", "blue")
        self.quiz_button.clicked.connect(lambda: self.start_quiz(timed=False))
        quiz_layout.addWidget(self.quiz_button)
        
        self.timed_quiz_button = AnimatedButton("⏱️ Timed Challenge", "orange")
        self.timed_quiz_button.clicked.connect(lambda: self.start_quiz(timed=True))
        quiz_layout.addWidget(self.timed_quiz_button)
        
        buttons_layout.addWidget(quiz_frame)
        
        self.view_button = AnimatedButton("📋 View Flashcards", "teal")
        self.view_button.clicked.connect(self.show_flashcards)
        buttons_layout.addWidget(self.view_button)
        
        utility_frame = QFrame()
        utility_layout = QHBoxLayout(utility_frame)
        utility_layout.setSpacing(12)
        
        self.instructions_button = AnimatedButton("📖 Instructions", "purple")
        self.instructions_button.clicked.connect(self.show_instructions)
        utility_layout.addWidget(self.instructions_button)
        
        self.settings_button = AnimatedButton("⚙️ Settings", "green")
        self.settings_button.clicked.connect(self.show_settings)
        utility_layout.addWidget(self.settings_button)
        
        self.back_button = AnimatedButton("🏠 Back", "red")
        self.back_button.clicked.connect(self.parent.show_landing)
        utility_layout.addWidget(self.back_button)
        
        buttons_layout.addWidget(utility_frame)
        layout.addWidget(buttons_frame)
        
        self.table_frame = QFrame()
        self.table_frame.setVisible(False)
        table_layout = QVBoxLayout(self.table_frame)
        table_layout.setSpacing(12)
        
        table_title = QLabel("📊 Flashcard Collection")
        table_title.setFont(QFont("Inter", 16, QFont.Bold))
        table_title.setAlignment(Qt.AlignCenter)
        table_title.setStyleSheet("""
            color: white;
            background: #16a34a;
            padding: 12px;
            border-radius: 8px;
        """)
        table_layout.addWidget(table_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                gridline-color: #e5e7eb;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QTableWidget::item:selected {
                background: #2563eb;
                color: white;
            }
            QHeaderView::section {
                background: #2563eb;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        """)
        table_layout.addWidget(self.table)
        
        hide_table_button = AnimatedButton("👁️ Hide Flashcards", "red")
        hide_table_button.clicked.connect(self.hide_flashcards)
        table_layout.addWidget(hide_table_button)
        
        layout.addWidget(self.table_frame)
        layout.addStretch()
        
        self.setLayout(layout)
        self.update_stats()
        QTimer.singleShot(100, self.fade_in)

    def update_stats(self):
        stats = self.data["stats"]
        total_cards = len(self.data["flashcards"])
        if stats["total"] > 0:
            percent = (stats["correct"] / stats["total"]) * 100
            self.stats_label.setText(
                f"📊 Score: {stats['correct']}/{stats['total']} ({percent:.1f}%) | "
                f"📚 Cards: {total_cards}"
            )
        else:
            self.stats_label.setText(f"📚 Cards: {total_cards} | 🎯 Start your first quiz!")

    def show_flashcards(self):
        if not self.data["flashcards"]:
            QMessageBox.information(self, "No Flashcards",
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
            QMessageBox.warning(self, "No Flashcards",
                              "No flashcards available!\nPlease add flashcards in the Admin Panel.")
            return
        cards = self.data["flashcards"].copy()
        random.shuffle(cards)
        time_limit = self.data["settings"]["default_time_limit"] if timed else 10
        if timed:
            time_limit, ok = QInputDialog.getDouble(
                self, "Timed Quiz Setup",
                "Enter time limit per question (seconds):",
                self.data["settings"]["default_time_limit"], 1, 60, 1
            )
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
        
    def show_settings(self):
        dialog = SettingsDialog(self, self.data)
        if dialog.exec_():
            self.parent.save_data()
            self.update_stats()

    def show_admin_login(self):
        login_dialog = AdminLoginDialog(self)
        if login_dialog.exec_():
            admin_panel = AdminPanel(self.parent, self.data)
            admin_panel.exec_()
            self.update_stats()