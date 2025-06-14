from PyQt5.QtWidgets import (
    QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt5.QtGui import QFont

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

class FlashcardDialog(QDialog):
    """Modern flashcard add/edit dialog."""
    def __init__(self, parent=None, question="", answer="", category="", edit_mode=False, categories=None):
        super().__init__(parent)
        self.setWindowTitle("✏️ Edit Flashcard" if edit_mode else "➕ Add Flashcard")
        self.setFixedSize(500, 400)
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
        
        c_label = QLabel("📌 Category:")
        c_label.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 14px;")
        layout.addWidget(c_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(categories or ["General Knowledge", "OOP", "Data Structures", "Mathematics", "Programming"])
        self.category_combo.setCurrentText(category or "General Knowledge")
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            QComboBox:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
        """)
        layout.addWidget(self.category_combo)
        
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
        return (self.question_input.text().strip(), self.answer_input.text().strip(), self.category_combo.currentText())