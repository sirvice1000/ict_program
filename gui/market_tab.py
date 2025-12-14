"""
Market Analysis Tab - Circuit Breakers, CME Data, and Daily Tracking
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QGridLayout, QGroupBox,
                            QScrollArea, QDateEdit, QMessageBox, QFrame, QSplitter)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QDoubleValidator, QFont
from database.db_manager import DatabaseManager
import webbrowser

class MarketTab(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.cb_cards = {}
        self.general_cb_inputs = {}
        self.general_cb_results = {}
        self.cme_inputs = {}
        self.cme_results = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the market analysis interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📊 Market Analysis Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3b82f6;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Date selector
        date_label = QLabel("Date:")
        date_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        header_layout.addWidget(date_label)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumWidth(150)
        self.date_input.setStyleSheet("font-size: 14px; padding: 8px;")
        header_layout.addWidget(self.date_input)
        
        layout.addLayout(header_layout)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Your assets
        left_panel = self.create_your_assets_panel()
        splitter.addWidget(left_panel)
        
        # Right side: General calculator + CME data
        right_panel = self.create_tools_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 400])
        layout.addWidget(splitter)
        
    def create_your_assets_panel(self):
        """Create panel for your 9 main trading assets"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Your Trading Assets - Circuit Breakers")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)
        
        # Your assets
        assets = [
            ("GOLD", "XAUUSD", "commodity"),
            ("BITCOIN/USD", "BTCUSD", "crypto"),
            ("SOL/USD", "SOLUSD", "crypto"),
            ("ETH/USD", "ETHUSD", "crypto"),
            ("USOIL", "USOIL", "commodity"),
            ("NASDAQ", "NAS100", "index"),
            ("SP500", "SPX500", "index"),
            ("DJI", "US30", "index"),
            ("XRP/USD", "XRPUSD", "crypto")
        ]
        
        for display_name, symbol, asset_type in assets:
            card = self.create_asset_cb_card(display_name, symbol, asset_type)
            content_layout.addWidget(card)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return panel
    
    def create_tools_panel(self):
        """Create panel for general calculator and CME data"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        
        # General calculator
        general_calc = self.create_general_calculator()
        content_layout.addWidget(general_calc)
        
        # CME Data section
        cme_section = self.create_cme_section()
        content_layout.addWidget(cme_section)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return panel
    
    def create_asset_cb_card(self, display_name, symbol, asset_type):
        """Create compact circuit breaker card for one asset"""
        card = QGroupBox(display_name)
        card.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3b82f6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #1e293b;
            }
            QGroupBox::title {
                color: #60a5fa;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 15, 10, 10)
        
        # Row 1: Previous Day Data
        layout.addWidget(QLabel("H:"), 0, 0)
        high_input = QLineEdit()
        high_input.setPlaceholderText("High")
        high_input.setMaximumWidth(70)
        high_input.textChanged.connect(lambda: self.calc_cb(symbol))
        layout.addWidget(high_input, 0, 1)
        
        layout.addWidget(QLabel("L:"), 0, 2)
        low_input = QLineEdit()
        low_input.setPlaceholderText("Low")
        low_input.setMaximumWidth(70)
        low_input.textChanged.connect(lambda: self.calc_cb(symbol))
        layout.addWidget(low_input, 0, 3)
        
        layout.addWidget(QLabel("C:"), 0, 4)
        close_input = QLineEdit()
        close_input.setPlaceholderText("Close")
        close_input.setMaximumWidth(70)
        close_input.textChanged.connect(lambda: self.calc_cb(symbol))
        layout.addWidget(close_input, 0, 5)
        
        # Row 2: CME Settlement (for proper next day calculation)
        layout.addWidget(QLabel("Settlement:"), 1, 0, 1, 2)
        settlement_input = QLineEdit()
        settlement_input.setPlaceholderText("CME Settlement (optional)")
        settlement_input.textChanged.connect(lambda: self.calc_cb(symbol))
        layout.addWidget(settlement_input, 1, 2, 1, 4)
        
        # Circuit Breaker Results
        cb1_label = QLabel("CB1: —")
        cb1_label.setStyleSheet("background-color: #422006; color: #fbbf24; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(cb1_label, 2, 0, 1, 2)
        
        cb2_label = QLabel("CB2: —")
        cb2_label.setStyleSheet("background-color: #7c2d12; color: #fb923c; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(cb2_label, 2, 2, 1, 2)
        
        cb3_label = QLabel("CB3: —")
        cb3_label.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(cb3_label, 2, 4, 1, 2)
        
        # Next Day Projections
        proj_high_label = QLabel("Next High: —")
        proj_high_label.setStyleSheet("background-color: #14532d; color: #86efac; padding: 4px; border-radius: 3px; font-size: 11px; font-weight: bold;")
        layout.addWidget(proj_high_label, 3, 0, 1, 3)
        
        proj_low_label = QLabel("Next Low: —")
        proj_low_label.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 4px; border-radius: 3px; font-size: 11px; font-weight: bold;")
        layout.addWidget(proj_low_label, 3, 3, 1, 3)
        
        # Store references
        self.cb_cards[symbol] = {
            'high': high_input,
            'low': low_input,
            'close': close_input,
            'settlement': settlement_input,
            'cb1': cb1_label,
            'cb2': cb2_label,
            'cb3': cb3_label,
            'proj_high': proj_high_label,
            'proj_low': proj_low_label,
            'type': asset_type
        }
        
        card.setLayout(layout)
        return card
    
    def create_general_calculator(self):
        """Create general calculator for any asset"""
        group = QGroupBox("General Calculator (Any Asset)")
        group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; color: #a78bfa; }")
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # Asset name input
        layout.addWidget(QLabel("Asset:"), 0, 0)
        asset_input = QLineEdit()
        asset_input.setPlaceholderText("e.g., AAPL, TSLA...")
        layout.addWidget(asset_input, 0, 1, 1, 3)
        
        # Price inputs
        layout.addWidget(QLabel("High:"), 1, 0)
        high_input = QLineEdit()
        high_input.textChanged.connect(self.calc_general_cb)
        layout.addWidget(high_input, 1, 1)
        
        layout.addWidget(QLabel("Low:"), 1, 2)
        low_input = QLineEdit()
        low_input.textChanged.connect(self.calc_general_cb)
        layout.addWidget(low_input, 1, 3)
        
        layout.addWidget(QLabel("Close:"), 2, 0)
        close_input = QLineEdit()
        close_input.textChanged.connect(self.calc_general_cb)
        layout.addWidget(close_input, 2, 1, 1, 3)
        
        # Results
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #475569;")
        layout.addWidget(line, 3, 0, 1, 4)
        
        cb1_label = QLabel("CB Level 1: —")
        cb1_label.setStyleSheet("background-color: #422006; color: #fbbf24; padding: 8px; border-radius: 4px;")
        layout.addWidget(cb1_label, 4, 0, 1, 4)
        
        cb2_label = QLabel("CB Level 2: —")
        cb2_label.setStyleSheet("background-color: #7c2d12; color: #fb923c; padding: 8px; border-radius: 4px;")
        layout.addWidget(cb2_label, 5, 0, 1, 4)
        
        cb3_label = QLabel("CB Level 3: —")
        cb3_label.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 8px; border-radius: 4px;")
        layout.addWidget(cb3_label, 6, 0, 1, 4)
        
        proj_high_label = QLabel("Next Day High: —")
        proj_high_label.setStyleSheet("background-color: #14532d; color: #86efac; padding: 8px; border-radius: 4px;")
        layout.addWidget(proj_high_label, 7, 0, 1, 4)
        
        proj_low_label = QLabel("Next Day Low: —")
        proj_low_label.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 8px; border-radius: 4px;")
        layout.addWidget(proj_low_label, 8, 0, 1, 4)
        
        self.general_cb_inputs = {
            'asset': asset_input,
            'high': high_input,
            'low': low_input,
            'close': close_input
        }
        
        self.general_cb_results = {
            'cb1': cb1_label,
            'cb2': cb2_label,
            'cb3': cb3_label,
            'proj_high': proj_high_label,
            'proj_low': proj_low_label
        }
        
        group.setLayout(layout)
        return group
    
    def create_cme_section(self):
        """Create CME reference data section for indices"""
        group = QGroupBox("CME Reference Data (Indices)")
        group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; color: #fbbf24; }")
        
        layout = QVBoxLayout()
        
        # Info and button section
        info_layout = QHBoxLayout()
        
        info = QLabel(
            "Enter CME settlement/opening reference prices for indices.\n"
            "Used for calculating official circuit breaker levels."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info_layout.addWidget(info)
        
        info_layout.addStretch()
        
        # Button to open CME website
        cme_button = QPushButton("🌐 Get CME Data")
        cme_button.setStyleSheet("""
            QPushButton {
                background-color: #0891b2;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0e7490;
            }
        """)
        cme_button.clicked.connect(self.open_cme_website)
        cme_button.setToolTip("Opens CME Group website in your browser")
        info_layout.addWidget(cme_button)
        
        layout.addLayout(info_layout)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #475569; margin: 10px 0;")
        layout.addWidget(line)
        
        # Create CME input for each index
        indices = [
            ("NASDAQ (NAS100)", "NAS100"),
            ("S&P 500 (SPX500)", "SPX500"),
            ("Dow Jones (US30)", "US30")
        ]
        
        for display, symbol in indices:
            card = self.create_cme_card(display, symbol)
            layout.addWidget(card)
        
        group.setLayout(layout)
        return group
    
    def create_cme_card(self, display_name, symbol):
        """Create CME data card for an index"""
        card = QFrame()
        card.setStyleSheet("background-color: #1e293b; border: 1px solid #475569; border-radius: 6px; padding: 10px;")
        
        layout = QGridLayout(card)
        layout.setSpacing(8)
        
        # Title
        title = QLabel(display_name)
        title.setStyleSheet("font-weight: bold; font-size: 13px; color: #fbbf24;")
        layout.addWidget(title, 0, 0, 1, 4)
        
        # Inputs
        layout.addWidget(QLabel("Prior Settlement:"), 1, 0)
        settlement_input = QLineEdit()
        settlement_input.setPlaceholderText("CME Settlement")
        settlement_input.textChanged.connect(lambda: self.calc_cme(symbol))
        layout.addWidget(settlement_input, 1, 1, 1, 3)
        
        layout.addWidget(QLabel("Opening Price:"), 2, 0)
        open_input = QLineEdit()
        open_input.setPlaceholderText("Today's Open")
        open_input.textChanged.connect(lambda: self.calc_cme(symbol))
        layout.addWidget(open_input, 2, 1, 1, 3)
        
        # CME Limit Up/Down Results
        limit_up_7 = QLabel("Limit Up 7%: —")
        limit_up_7.setStyleSheet("background-color: #14532d; color: #86efac; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_up_7, 3, 0, 1, 2)
        
        limit_down_7 = QLabel("Limit Down 7%: —")
        limit_down_7.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_down_7, 3, 2, 1, 2)
        
        limit_up_13 = QLabel("Limit Up 13%: —")
        limit_up_13.setStyleSheet("background-color: #14532d; color: #86efac; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_up_13, 4, 0, 1, 2)
        
        limit_down_13 = QLabel("Limit Down 13%: —")
        limit_down_13.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_down_13, 4, 2, 1, 2)
        
        limit_up_20 = QLabel("Limit Up 20%: —")
        limit_up_20.setStyleSheet("background-color: #14532d; color: #86efac; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_up_20, 5, 0, 1, 2)
        
        limit_down_20 = QLabel("Limit Down 20%: —")
        limit_down_20.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; padding: 4px; border-radius: 3px; font-size: 11px;")
        layout.addWidget(limit_down_20, 5, 2, 1, 2)
        
        self.cme_inputs[symbol] = {
            'settlement': settlement_input,
            'open_ref': open_input
        }
        
        self.cme_results[symbol] = {
            'limit_up_7': limit_up_7,
            'limit_down_7': limit_down_7,
            'limit_up_13': limit_up_13,
            'limit_down_13': limit_down_13,
            'limit_up_20': limit_up_20,
            'limit_down_20': limit_down_20
        }
        
        return card
    
    def calc_cb(self, symbol):
        """Calculate circuit breakers for your assets with proper next day high/low"""
        card = self.cb_cards[symbol]
        
        try:
            high_text = card['high'].text().strip()
            low_text = card['low'].text().strip()
            close_text = card['close'].text().strip()
            settlement_text = card['settlement'].text().strip()
            
            if not (high_text and low_text and close_text):
                card['cb1'].setText("CB1: —")
                card['cb2'].setText("CB2: —")
                card['cb3'].setText("CB3: —")
                card['proj_high'].setText("Next High: —")
                card['proj_low'].setText("Next Low: —")
                return
            
            high = float(high_text)
            low = float(low_text)
            close = float(close_text)
            
            # Circuit breakers based on close
            cb1_up = close * 1.07
            cb1_down = close * 0.93
            cb2_up = close * 1.13
            cb2_down = close * 0.87
            cb3_up = close * 1.20
            cb3_down = close * 0.80
            
            # Next day high/low projections
            # If settlement is provided, use CME method
            # Otherwise use range-based method
            if settlement_text:
                settlement = float(settlement_text)
                # CME method: Settlement +/- range
                range_val = high - low
                proj_high = settlement + range_val
                proj_low = settlement - range_val
            else:
                # Traditional method: extend the range
                range_val = high - low
                proj_high = high + (range_val * 0.618)  # 61.8% Fibonacci extension
                proj_low = low - (range_val * 0.618)
            
            # Update labels
            card['cb1'].setText(f"CB1: ↑{cb1_up:.2f} ↓{cb1_down:.2f}")
            card['cb2'].setText(f"CB2: ↑{cb2_up:.2f} ↓{cb2_down:.2f}")
            card['cb3'].setText(f"CB3: ↑{cb3_up:.2f} ↓{cb3_down:.2f}")
            card['proj_high'].setText(f"Next High: {proj_high:.2f}")
            card['proj_low'].setText(f"Next Low: {proj_low:.2f}")
            
        except ValueError:
            card['cb1'].setText("CB1: —")
            card['cb2'].setText("CB2: —")
            card['cb3'].setText("CB3: —")
            card['proj_high'].setText("Next High: —")
            card['proj_low'].setText("Next Low: —")
    
    def calc_general_cb(self):
        """Calculate for general calculator"""
        inputs = self.general_cb_inputs
        results = self.general_cb_results
        
        try:
            high_text = inputs['high'].text().strip()
            low_text = inputs['low'].text().strip()
            close_text = inputs['close'].text().strip()
            
            if not (high_text and low_text and close_text):
                results['cb1'].setText("CB Level 1: —")
                results['cb2'].setText("CB Level 2: —")
                results['cb3'].setText("CB Level 3: —")
                results['proj_high'].setText("Next Day High: —")
                results['proj_low'].setText("Next Day Low: —")
                return
            
            high = float(high_text)
            low = float(low_text)
            close = float(close_text)
            
            cb1_up = close * 1.07
            cb1_down = close * 0.93
            cb2_up = close * 1.13
            cb2_down = close * 0.87
            cb3_up = close * 1.20
            cb3_down = close * 0.80
            
            range_val = high - low
            proj_high = high + (range_val * 0.5)
            proj_low = low - (range_val * 0.5)
            
            results['cb1'].setText(f"CB Level 1 (7%): ↑ {cb1_up:.2f}  |  ↓ {cb1_down:.2f}")
            results['cb2'].setText(f"CB Level 2 (13%): ↑ {cb2_up:.2f}  |  ↓ {cb2_down:.2f}")
            results['cb3'].setText(f"CB Level 3 (20%): ↑ {cb3_up:.2f}  |  ↓ {cb3_down:.2f}")
            results['proj_high'].setText(f"Next Day High: {proj_high:.2f}")
            results['proj_low'].setText(f"Next Day Low: {proj_low:.2f}")
            
        except ValueError:
            results['cb1'].setText("CB Level 1: —")
            results['cb2'].setText("CB Level 2: —")
            results['cb3'].setText("CB Level 3: —")
            results['proj_high'].setText("Next Day High: —")
            results['proj_low'].setText("Next Day Low: —")
    
    def calc_cme(self, symbol):
        """Calculate CME Limit Up/Limit Down levels"""
        inputs = self.cme_inputs[symbol]
        results = self.cme_results[symbol]
        
        try:
            settlement_text = inputs['settlement'].text().strip()
            
            if not settlement_text:
                results['limit_up_7'].setText("Limit Up 7%: —")
                results['limit_down_7'].setText("Limit Down 7%: —")
                results['limit_up_13'].setText("Limit Up 13%: —")
                results['limit_down_13'].setText("Limit Down 13%: —")
                results['limit_up_20'].setText("Limit Up 20%: —")
                results['limit_down_20'].setText("Limit Down 20%: —")
                return
            
            # Use prior settlement price as reference (CME standard)
            settlement = float(settlement_text)
            
            # Calculate CME Limit Up/Down levels
            # These are the official circuit breaker halt levels
            limit_up_7 = settlement * 1.07
            limit_down_7 = settlement * 0.93
            
            limit_up_13 = settlement * 1.13
            limit_down_13 = settlement * 0.87
            
            limit_up_20 = settlement * 1.20
            limit_down_20 = settlement * 0.80
            
            # Update labels with proper formatting
            results['limit_up_7'].setText(f"↑ {limit_up_7:.2f}")
            results['limit_down_7'].setText(f"↓ {limit_down_7:.2f}")
            results['limit_up_13'].setText(f"↑ {limit_up_13:.2f}")
            results['limit_down_13'].setText(f"↓ {limit_down_13:.2f}")
            results['limit_up_20'].setText(f"↑ {limit_up_20:.2f}")
            results['limit_down_20'].setText(f"↓ {limit_down_20:.2f}")
            
        except ValueError:
            results['limit_up_7'].setText("Limit Up 7%: —")
            results['limit_down_7'].setText("Limit Down 7%: —")
            results['limit_up_13'].setText("Limit Up 13%: —")
            results['limit_down_13'].setText("Limit Down 13%: —")
            results['limit_up_20'].setText("Limit Up 20%: —")
            results['limit_down_20'].setText("Limit Down 20%: —")
    
    def load_todays_data(self):
        """Load today's data - placeholder for future use"""
        pass
    
    def open_cme_website(self):
        """Open CME Group price limits page in default browser"""
        cme_url = "https://www.cmegroup.com/trading/price-limits.html#equityIndex"
        try:
            webbrowser.open(cme_url)
            QMessageBox.information(
                self,
                "Opening CME Price Limits",
                "Opening CME Group Price Limits page in your browser.\n\n"
                "Look for EQUITY INDEX section:\n"
                "• E-mini S&P 500 (ES) - Settlement Price\n"
                "• E-mini NASDAQ-100 (NQ) - Settlement Price\n"
                "• E-mini Dow (YM) - Settlement Price\n\n"
                "Also note the Limit Up/Limit Down levels shown.\n"
                "Enter the settlement price to calculate circuit breakers."
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open browser. Please visit:\n{cme_url}"
            )