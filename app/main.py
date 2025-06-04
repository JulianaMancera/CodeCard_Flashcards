import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui import LandingPage, MainContent
from data import load_data, save_data

class FlashcardApp(QMainWindow):
    """Main application window with landing page and main content."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Quiz App")
        self.setFixedSize(600, 500)
        self.data = load_data()

        # Stacked widget for landing and main pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Landing page
        self.landing_page = LandingPage(self)
        self.stacked_widget.addWidget(self.landing_page)

        # Main content
        self.main_content = MainContent(self, self.data)
        self.stacked_widget.addWidget(self.main_content)

        # Global stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #e6f3fa; }
            QPushButton:hover { background-color: #4682b4; }
            QTableWidget { gridline-color: #b0c4de; }
        """)

    def show_main(self):
        self.stacked_widget.setCurrentWidget(self.main_content)

    def save_data(self):
        save_data(self.data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec_())