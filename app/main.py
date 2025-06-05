import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
from ui import LandingPage, MainContent
from data import load_data, save_data

class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 CodeCard Flashcard App - Learning Made Fun!")
         # self.setWindowIcon(QIcon('icon.png'))
        
        # Make the app full screen or maximized
        self.showMaximized()  # Use showFullScreen() for true full screen
    
        self.center_window()
        
        # Load data
        self.data = load_data()

        # Create stacked widget for multiple pages
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
                    stop:0 #dfe6e9, stop:0.5 #b2bec3, stop:1 #dfe6e9);
            }
            
            /* Global button hover effects */
            QPushButton:hover {
                transform: scale(1.02);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            
            QPushButton:pressed {
                transform: scale(0.98);
            }
            
            /* Global font settings */
            * {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            /* Smooth scrollbars */
            QScrollBar:vertical {
                background: #ecf0f1;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #1f4e79);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
            /* Modern message boxes */
            QMessageBox {
                background: qlinear-gradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
                border-radius: 10px;
            }
            
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f4e79);
            }
            
            /* Input dialogs */
            QInputDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
                border-radius: 10px;
            }
            
            QInputDialog QLineEdit, QInputDialog QDoubleSpinBox {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 6px;
                font-size: 14px;
                background: white;
            }
            
            QInputDialog QLineEdit:focus, QInputDialog QDoubleSpinBox:focus {
                border-color: #2980b9;
                background: #f8f9fa;
            }
        """)

    def setup_auto_save(self):
        """Set up automatic data saving every 30 seconds."""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_data)
        self.auto_save_timer.start(30000)  # 30 seconds

    def show_main(self):
        """Switch to main content page."""
        self.stacked_widget.setCurrentWidget(self.main_content)
        self.main_content.update_stats()  # Refresh stats when showing main content

    def show_landing(self):
        """Switch to landing page."""
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
            # Save data before closing
            self.save_data()
            
            # Stop auto-save timer
            if hasattr(self, 'auto_save_timer'):
                self.auto_save_timer.stop()
            
            event.accept()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            event.accept()

    def keyPressEvent(self, event):
        """Handle global key press events."""
        # F11 for fullscreen toggle
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()
        
        # Escape to exit fullscreen
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()
        
        # Ctrl+S to save
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_data()
        
        # Ctrl+Q to quit
        elif event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.close()
        
        else:
            super().keyPressEvent(event)

def setup_application():
    """Set up the QApplication with modern settings."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("CodeCard Flashcard App")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("CodeCard Learning")
    app.setOrganizationDomain("codecard.learning")
    
    # Enable high DPI scaling for modern displays
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Set default font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferDefaultHinting)
    app.setFont(font)
    
    return app

if __name__ == "__main__":
    # Create and setup application
    app = setup_application()
    
    # Create and show main window
    window = FlashcardApp()
    window.show()
    
    # Handle application events and cleanup
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)