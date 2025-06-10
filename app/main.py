import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from ui import LandingPage, MainContent
from data import load_data, save_data

# Constants
WINDOW_TITLE = "🎓 CodeCard Flashcard App"
APP_CONFIG = {
    "name": "CodeCard Flashcard App",
    "version": "2.1",
    "org": "CodeCard Learning",
    "domain": "codecard.learning",
    "scale": 0.8,
    "splash_ms": 1000,
    "autosave_ms": 30000,
    "font": ("Inter", 11)
}

class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = load_data() or {}
        self.setWindowTitle(WINDOW_TITLE)
        self._setup_ui()
        self._setup_auto_save()

    def _setup_ui(self):
        """Set up UI components."""
        # Window size and position
        screen = QDesktopWidget().screenGeometry()
        self.resize(800, 600)  # Set fixed size (width: 800px, height: 600px)
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        # Splash screen
        splash = QSplashScreen(QPixmap(800, 600).fill(Qt.white))
        splash.show()
        splash.showMessage(f"Loading {APP_CONFIG['name']}...", Qt.AlignCenter | Qt.AlignBottom, Qt.black)
        QApplication.processEvents()
        QTimer.singleShot(APP_CONFIG["splash_ms"], splash.close)

        # Stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.landing_page = LandingPage(self)
        self.main_content = MainContent(self, self.data)
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.addWidget(self.main_content)

        # Basic styling
        self.setStyleSheet("""
            QMainWindow { background: #f0f4f8; }
            QPushButton {
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                border-radius: 8px;
                padding: 12px 24px;
                color: white;
                border: none;
                background: #2563eb;
            }
            QPushButton:hover { background: #1d4ed8; }
            QLineEdit, QTextEdit {
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
            }
        """)

    def _setup_auto_save(self):
        """Set up auto-save."""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_data)
        self.auto_save_timer.start(APP_CONFIG["autosave_ms"])

    def show_main(self):
        """Show main content."""
        self.stacked_widget.setCurrentWidget(self.main_content)
        self.main_content.update_stats()

    def show_landing(self):
        """Show landing page."""
        self.stacked_widget.setCurrentWidget(self.landing_page)

    def save_data(self):
        """Save data."""
        try:
            save_data(self.data)
        except Exception as e:
            print(f"Save error: {e}")

    def closeEvent(self, event):
        """Handle close event."""
        self.save_data()
        if hasattr(self, 'auto_save_timer'):
            self.auto_save_timer.stop()
        event.accept()

    def keyPressEvent(self, event):
        """Handle key presses."""
        actions = {
            Qt.Key_F11: lambda: self.showNormal() if self.isMaximized() else self.showMaximized(),
            Qt.Key_Escape: self.showNormal,
            (Qt.Key_S, Qt.ControlModifier): self.save_data,
            (Qt.Key_Q, Qt.ControlModifier): self.close
        }
        for key, action in actions.items():
            if isinstance(key, tuple):
                if event.key() == key[0] and event.modifiers() == key[1]:
                    action()
                    return
            elif event.key() == key:
                action()
                return
        super().keyPressEvent(event)

def setup_app():
    """Set up QApplication."""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_CONFIG["name"])
    app.setApplicationVersion(APP_CONFIG["version"])
    app.setOrganizationName(APP_CONFIG["org"])
    app.setOrganizationDomain(APP_CONFIG["domain"])
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setFont(QFont(*APP_CONFIG["font"]))
    return app

def main():
    """Run application."""
    try:
        app = setup_app()
        window = FlashcardApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"App error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()