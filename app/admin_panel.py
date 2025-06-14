from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QFrame, QLineEdit, QComboBox, QMessageBox, QFileDialog, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils import AnimatedButton, FlashcardDialog
import json

class AdminPanel(QDialog):
    """Modern admin panel for flashcard management with enhanced features."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Panel")
        self.resize(900, 650)
        self.data = data
        self.parent_app = parent
        self.sort_order = Qt.AscendingOrder
        self.sort_column = 1  # Default sort by question
        self.setup_ui()

    def setup_ui(self):
        """Set up the admin panel UI."""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
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

        # Search bar
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 14px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by question or answer...")
        self.search_input.setStyleSheet("""
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
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addWidget(search_frame)

        # Sort controls
        sort_frame = QFrame()
        sort_layout = QHBoxLayout(sort_frame)
        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("color: #1e293b; font-weight: bold; font-size: 14px;")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Question", "Answer", "Category"])
        self.sort_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #2563eb;
            }
        """)
        self.sort_button = AnimatedButton("↕️ Toggle Sort", "purple")
        self.sort_button.setToolTip("Toggle between ascending and descending order")
        self.sort_button.clicked.connect(self.toggle_sort)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addWidget(self.sort_button)
        sort_layout.addStretch()
        layout.addWidget(sort_frame)

        # Button frame
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)

        self.add_button = AnimatedButton("➕ Add", "green")
        self.add_button.setToolTip("Add a new flashcard")
        self.add_button.clicked.connect(self.add_flashcard)
        self.edit_button = AnimatedButton("✏️ Edit", "orange")
        self.edit_button.setToolTip("Edit selected flashcard")
        self.edit_button.clicked.connect(self.edit_flashcard)
        self.delete_button = AnimatedButton("🗑️ Delete", "red")
        self.delete_button.setToolTip("Delete selected flashcard")
        self.delete_button.clicked.connect(self.delete_flashcard)
        self.delete_selected_button = AnimatedButton("🗑️ Delete Selected", "red")
        self.delete_selected_button.setToolTip("Delete all selected flashcards")
        self.delete_selected_button.clicked.connect(self.delete_selected_flashcards)
        self.refresh_button = AnimatedButton("🔄 Refresh", "purple")
        self.refresh_button.setToolTip("Refresh the flashcard table")
        self.refresh_button.clicked.connect(self.refresh_table)
        self.export_button = AnimatedButton("📤 Export", "teal")
        self.export_button.setToolTip("Export flashcards to JSON")
        self.export_button.clicked.connect(self.export_flashcards)
        self.import_button = AnimatedButton("📥 Import", "blue")
        self.import_button.setToolTip("Import flashcards from JSON")
        self.import_button.clicked.connect(self.import_flashcards)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.delete_selected_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.import_button)
        layout.addWidget(button_frame)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Select", "#", "Question", "Answer", "Category"])
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
            QTableWidget::item:nth-child(even) {
                background: #f8fafc;
            }
            QHeaderView::section {
                background: #2563eb;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table.setColumnWidth(0, 50)  # Narrow column for checkboxes
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Ensure row selection
        layout.addWidget(self.table)

        # Close button
        close_button = AnimatedButton("🚪 Close", "teal")
        close_button.setToolTip("Close the admin panel")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        """Refresh the table with current flashcards."""
        self.table.setRowCount(len(self.data["flashcards"]))
        for i, card in enumerate(self.data["flashcards"]):
            # Checkbox column
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)
            self.table.setItem(i, 0, checkbox)
            # Other columns
            self.table.setItem(i, 1, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 2, QTableWidgetItem(card["question"]))
            self.table.setItem(i, 3, QTableWidgetItem(card["answer"]))
            self.table.setItem(i, 4, QTableWidgetItem(card["category"]))
        self.sort_table()

    def filter_table(self):
        """Filter table based on search input."""
        search_text = self.search_input.text().lower()
        filtered_cards = [
            card for card in self.data["flashcards"]
            if search_text in card["question"].lower() or search_text in card["answer"].lower() or search_text in card["category"].lower()
        ]
        self.table.setRowCount(len(filtered_cards))
        for i, card in enumerate(filtered_cards):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)
            self.table.setItem(i, 0, checkbox)
            self.table.setItem(i, 1, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 2, QTableWidgetItem(card["question"]))
            self.table.setItem(i, 3, QTableWidgetItem(card["answer"]))
            self.table.setItem(i, 4, QTableWidgetItem(card["category"]))
        self.sort_table()

    def sort_table(self):
        """Sort table based on selected column and order."""
        column_map = {"Question": 2, "Answer": 3, "Category": 4}
        column = column_map[self.sort_combo.currentText()]
        self.table.sortItems(column, self.sort_order)

    def toggle_sort(self):
        """Toggle sort order between ascending and descending."""
        self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        self.sort_table()

    def add_flashcard(self):
        """Add a new flashcard."""
        dialog = FlashcardDialog(self, categories=["General Knowledge", "OOP", "Data Structures", "Mathematics", "Programming"])
        if dialog.exec_():
            question, answer, category = dialog.get_data()
            if question and answer and category:
                self.data["flashcards"].append({"question": question, "answer": answer, "category": category})
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "Success", "Flashcard added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Question, answer, and category cannot be empty.")

    def edit_flashcard(self):
        """Edit selected flashcard."""
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a flashcard to edit.")
            return
            
        # Find original card index
        question = self.table.item(current_row, 2).text()
        answer = self.table.item(current_row, 3).text()
        category = self.table.item(current_row, 4).text()
        original_index = next((i for i, card in enumerate(self.data["flashcards"])
                             if card["question"] == question and card["answer"] == answer and card["category"] == category), None)
        if original_index is None:
            QMessageBox.warning(self, "Error", "Selected flashcard not found in data.")
            return
        card = self.data["flashcards"][original_index]
        dialog = FlashcardDialog(self, card["question"], card["answer"], category, edit_mode=True,
                                categories=["General Knowledge", "OOP", "Data Structures", "Mathematics", "Programming"])
        if dialog.exec_():
            question, answer, category = dialog.get_data()
            if question and answer and category:
                self.data["flashcards"][original_index]["question"] = question
                self.data["flashcards"][original_index]["answer"] = answer
                self.data["flashcards"][original_index]["category"] = category
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "Success", "Flashcard updated successfully!")

    def delete_flashcard(self):
        """Delete selected flashcard with confirmation."""
        if not self.data["flashcards"]:
            QMessageBox.warning(self, "Error", "No flashcards available.")
            return
            
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a flashcard to delete.")
            return
            
        question = self.table.item(current_row, 2).text()
        reply = QMessageBox.question(self, "Delete Confirmation",
                                   f"Are you sure you want to delete the flashcard:\n'{question}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Find original card index
            question = self.table.item(current_row, 2).text()
            answer = self.table.item(current_row, 3).text()
            category = self.table.item(current_row, 4).text()
            original_index = next((i for i, card in enumerate(self.data["flashcards"])
                                if card["question"] == question and card["answer"] == answer and card["category"] == category), None)
            if original_index is not None:
                self.data["flashcards"].pop(original_index)
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "Success", "Flashcard deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Selected flashcard not found in data.")

    def delete_selected_flashcards(self):
        """Delete all selected flashcards."""
        selected_indices = []
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.Checked:
                question = self.table.item(row, 2).text()
                answer = self.table.item(row, 3).text()
                category = self.table.item(row, 4).text()
                original_index = next((i for i, card in enumerate(self.data["flashcards"])
                                    if card["question"] == question and card["answer"] == answer and card["category"] == category), None)
                if original_index is not None:
                    selected_indices.append(original_index)
        
        if not selected_indices:
            QMessageBox.warning(self, "Error", "No flashcards selected.")
            return

        reply = QMessageBox.question(self, "Delete Confirmation",
                                   f"Are you sure you want to delete {len(selected_indices)} selected flashcards?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Sort indices in descending order to avoid index shifting
            selected_indices.sort(reverse=True)
            for index in selected_indices:
                self.data["flashcards"].pop(index)
            self.parent_app.save_data()
            self.refresh_table()
            QMessageBox.information(self, "Success", f"{len(selected_indices)} flashcards deleted successfully!")

    def export_flashcards(self):
        """Export flashcards to a JSON file."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Flashcards", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(self.data["flashcards"], f, indent=2)
                QMessageBox.information(self, "Success", "Flashcards exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to export flashcards: {e}")

    def import_flashcards(self):
        """Import flashcards from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Flashcards", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    imported_cards = json.load(f)
                if not isinstance(imported_cards, list):
                    raise ValueError("Invalid JSON format: Expected a list of flashcards.")
                for card in imported_cards:
                    if not (isinstance(card, dict) and "question" in card and "answer" in card and "category" in card):
                        raise ValueError("Invalid flashcard format.")
                self.data["flashcards"].extend(imported_cards)
                self.parent_app.save_data()
                self.refresh_table()
                QMessageBox.information(self, "Success", "Flashcards imported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to import flashcards: {e}")