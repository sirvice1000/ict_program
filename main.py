"""
ICT Trading Knowledge & Journal Platform
Main Application Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    # Initialize database
    db = DatabaseManager()
    db.initialize_database()
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application metadata
    app.setApplicationName("ICT Trading Platform")
    app.setOrganizationName("TraderTools")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()