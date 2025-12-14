"""
Main Window - Primary application interface
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QLabel, QPushButton, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from gui.knowledge_tab import KnowledgeTab
from gui.journal_tab import JournalTab
from gui.analytics_tab import AnalyticsTab
from gui.market_tab import MarketTab
from database.db_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ICT Trading Platform - Knowledge & Journal")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for main content
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Create tabs
        self.market_tab = MarketTab(self.db)
        self.knowledge_tab = KnowledgeTab(self.db)
        self.journal_tab = JournalTab(self.db)
        self.analytics_tab = AnalyticsTab(self.db)
        
        self.tabs.addTab(self.market_tab, "📊 Market Data")
        self.tabs.addTab(self.knowledge_tab, "📚 Knowledge Base")
        self.tabs.addTab(self.journal_tab, "📝 Trade Journal")
        self.tabs.addTab(self.analytics_tab, "📈 Analytics")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
    def create_header(self):
        """Create application header"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e293b, stop:1 #334155);
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Title
        title_label = QLabel("ICT Trading Platform")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #f1f5f9;
        """)
        
        subtitle_label = QLabel("Knowledge Base & Trading Journal")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #94a3b8;
        """)
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.setSpacing(2)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Version label
        version_label = QLabel("v1.1.0")
        version_label.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(version_label)
        
        return header
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        tab_names = ["Market Data", "Knowledge Base", "Trade Journal", "Analytics"]
        if index < len(tab_names):
            self.status_bar.showMessage(f"Viewing: {tab_names[index]}")
            
            # Refresh analytics when switching to it
            if index == 3:
                self.analytics_tab.refresh_data()
            # Refresh market data when switching to it
            elif index == 0:
                self.market_tab.load_todays_data()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1e293b;
            }
            QTabBar::tab {
                background-color: #334155;
                color: #94a3b8;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #1e293b;
                color: #3b82f6;
                border-bottom: 2px solid #3b82f6;
            }
            QTabBar::tab:hover {
                background-color: #475569;
                color: #e2e8f0;
            }
            QStatusBar {
                background-color: #1e293b;
                color: #94a3b8;
                border-top: 1px solid #334155;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #475569;
                color: #64748b;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #334155;
                color: #e2e8f0;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #3b82f6;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 13px;
            }
            QListWidget, QTreeWidget, QTableWidget {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 6px;
                font-size: 13px;
            }
            QListWidget::item, QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #334155;
            }
            QListWidget::item:selected, QTreeWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QListWidget::item:hover, QTreeWidget::item:hover {
                background-color: #334155;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }
            QScrollBar:horizontal {
                background-color: #1e293b;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #475569;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #94a3b8;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                color: #e2e8f0;
                selection-background-color: #3b82f6;
                border: 1px solid #475569;
            }
            QGroupBox {
                color: #e2e8f0;
                border: 1px solid #475569;
                border-radius: 6px;
                margin-top: 12px;
                font-weight: 500;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTableWidget {
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
            }
            QHeaderView::section {
                background-color: #334155;
                color: #e2e8f0;
                padding: 8px;
                border: none;
                border-right: 1px solid #475569;
                border-bottom: 1px solid #475569;
                font-weight: 600;
            }
            QDateEdit {
                background-color: #334155;
                color: #e2e8f0;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px;
            }
            QDateEdit::drop-down {
                border: none;
                padding-right: 10px;
            }
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #94a3b8;
                margin-right: 5px;
            }
        """)