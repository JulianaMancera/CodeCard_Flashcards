import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from ui import LandingPage, MainContent
from data import load_data, save_data

class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 CodeCard Flashcard App")
        
        # Create splash screen
        splash_pix = QPixmap(800, 600)
        splash_pix.fill(Qt.white)
        splash = QSplashScreen(splash_pix)
        splash.show()
        splash.showMessage("Loading CodeCard Flashcard App...", Qt.AlignCenter | Qt.AlignBottom, Qt.black)
        QApplication.processEvents()
        
        # Set initial window size to 80% of screen size
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        self.center_window()
        
        # Load data
        self.data = load_data()
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create pages
        self.landing_page = LandingPage(self)
        self.main_content = MainContent(self, self.data)
        
        # Add pages to stack
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.addWidget(self.main_content)
        
        # Start with landing page
        self.stacked_widget.setCurrentWidget(self.landing_page)
        
        # Apply global styles
        self.apply_global_styles()
        
        # Set up auto-save timer
        self.setup_auto_save()
        
        # Close splash screen after initialization
        QTimer.singleShot(1000, splash.close)
        
    def center_window(self):
        """Center the window on the screen."""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def apply_global_styles(self):
        """Apply modern global stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f4f8, stop:0.5 #d1d9e6, stop:1 #f0f4f8);
            }
            QPushButton {
                font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                padding: 12px 24px;
                min-height: 40px;
                color: white;
                border: none;
            }
            QPushButton:hover {
                filter: brightness(1.1);
                transform: scale(1.02);
            }
            QPushButton:focus {
                outline: 2px solid #2563eb;
                outline-offset: 2px;
            }
            QLineEdit, QTextEdit {
                font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                background: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #2563eb;
                background: #f8fafc;
            }
            QScrollBar:vertical {
                background: #f0f4f8;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #2563eb;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QMessageBox, QDialog {
                background: #ffffff;
                border: 1px solid #d1d9e6;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: #2563eb;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background: #1d4ed8;
            }
        """)
    
    def setup_auto_save(self):
        """Set up automatic data saving every 30 seconds."""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_data)
        self.auto_save_timer.start(30000)
    
    def show_main(self):
        """Switch to main content page with animation."""
        self.stacked_widget.setCurrentWidget(self.main_content)
        self.main_content.update_stats()
    
    def show_landing(self):
        """Switch to landing page with animation."""
        self.stacked_widget.setCurrentWidget(self.landing_page)
    
    def save_data(self):
        """Save application data."""
        try:
            save_data(self.data)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def closeEvent(self, event):
        """Handle application close event."""
        try:
            self.save_data()
            if hasattr(self, 'auto_save_timer'):
                self.auto_save_timer.stop()
            event.accept()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            event.accept()
    
    def keyPressEvent(self, event):
        """Handle global key press events."""
        if event.key() == Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        elif event.key() == Qt.Key_Escape and self.isMaximized():
            self.showNormal()
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_data()
        elif event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)

def setup_application():
    """Set up the QApplication with modern settings."""
    app = QApplication(sys.argv)
    app.setApplicationName("CodeCard Flashcard App")
    app.setApplicationVersion("2.1")
    app.setOrganizationName("CodeCard Learning")
    app.setOrganizationDomain("codecard.learning")
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    font = QFont("Inter", 11)
    font.setHintingPreference(QFont.PreferDefaultHinting)
    app.setFont(font)
    return app

if __name__ == "__main__":
    app = setup_application()
    window = FlashcardApp()
    window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)