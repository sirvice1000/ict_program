"""
Trade Journal Tab - Log and manage trades
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                            QComboBox, QDoubleSpinBox, QTextEdit, QGroupBox,
                            QSplitter, QHeaderView, QMessageBox, QDateEdit,
                            QScrollArea, QFileDialog)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from database.db_manager import DatabaseManager

class JournalTab(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.current_trade_id = None
        self.init_ui()
        self.load_trades()
        
    def init_ui(self):
        """Initialize the journal interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top panel - Trade list
        top_panel = self.create_list_panel()
        splitter.addWidget(top_panel)
        
        # Bottom panel - Trade details
        bottom_panel = self.create_detail_panel()
        splitter.addWidget(bottom_panel)
        
        splitter.setSizes([400, 500])
        layout.addWidget(splitter)
        
    def create_list_panel(self):
        """Create trade list panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Header with buttons
        header_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ New Trade")
        add_btn.clicked.connect(self.add_new_trade)
        header_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_trade)
        delete_btn.setStyleSheet("background-color: #dc2626;")
        header_layout.addWidget(delete_btn)
        
        header_layout.addStretch()
        
        # Filter
        header_layout.addWidget(QLabel("Filter:"))
        self.outcome_filter = QComboBox()
        self.outcome_filter.addItems(["All", "Pending", "Win", "Loss", "Break Even"])
        self.outcome_filter.currentTextChanged.connect(self.filter_trades)
        header_layout.addWidget(self.outcome_filter)
        
        layout.addLayout(header_layout)
        
        # Trade table
        self.trade_table = QTableWidget()
        self.trade_table.setColumnCount(10)
        self.trade_table.setHorizontalHeaderLabels([
            "Date", "Pair", "Direction", "Entry", "Exit", "P&L", "P&L %", 
            "Outcome", "Setup", "Concepts"
        ])
        
        header = self.trade_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)
        
        self.trade_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.trade_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.trade_table.cellClicked.connect(self.on_trade_selected)
        
        layout.addWidget(self.trade_table)
        
        return panel
    
    def create_detail_panel(self):
        """Create trade detail panel"""
        panel = QWidget()
        main_layout = QVBoxLayout(panel)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        
        # Basic Info
        basic_group = QGroupBox("Trade Information")
        basic_layout = QVBoxLayout()
        
        # Row 1: Date, Pair, Timeframe
        row1 = QHBoxLayout()
        
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(self.date_input)
        row1.addLayout(date_layout)
        
        pair_layout = QVBoxLayout()
        pair_layout.addWidget(QLabel("Pair"))
        self.pair_input = QLineEdit()
        self.pair_input.setPlaceholderText("e.g., EURUSD")
        pair_layout.addWidget(self.pair_input)
        row1.addLayout(pair_layout)
        
        tf_layout = QVBoxLayout()
        tf_layout.addWidget(QLabel("Timeframe"))
        self.timeframe_input = QComboBox()
        self.timeframe_input.addItems(["1m", "5m", "15m", "30m", "1h", "4h", "D", "W"])
        tf_layout.addWidget(self.timeframe_input)
        row1.addLayout(tf_layout)
        
        dir_layout = QVBoxLayout()
        dir_layout.addWidget(QLabel("Direction"))
        self.direction_input = QComboBox()
        self.direction_input.addItems(["Long", "Short"])
        dir_layout.addWidget(self.direction_input)
        row1.addLayout(dir_layout)
        
        basic_layout.addLayout(row1)
        
        # Row 2: Prices
        row2 = QHBoxLayout()
        
        entry_layout = QVBoxLayout()
        entry_layout.addWidget(QLabel("Entry Price"))
        self.entry_input = QDoubleSpinBox()
        self.entry_input.setDecimals(5)
        self.entry_input.setMaximum(999999.99999)
        entry_layout.addWidget(self.entry_input)
        row2.addLayout(entry_layout)
        
        sl_layout = QVBoxLayout()
        sl_layout.addWidget(QLabel("Stop Loss"))
        self.sl_input = QDoubleSpinBox()
        self.sl_input.setDecimals(5)
        self.sl_input.setMaximum(999999.99999)
        sl_layout.addWidget(self.sl_input)
        row2.addLayout(sl_layout)
        
        tp_layout = QVBoxLayout()
        tp_layout.addWidget(QLabel("Take Profit"))
        self.tp_input = QDoubleSpinBox()
        self.tp_input.setDecimals(5)
        self.tp_input.setMaximum(999999.99999)
        tp_layout.addWidget(self.tp_input)
        row2.addLayout(tp_layout)
        
        exit_layout = QVBoxLayout()
        exit_layout.addWidget(QLabel("Exit Price"))
        self.exit_input = QDoubleSpinBox()
        self.exit_input.setDecimals(5)
        self.exit_input.setMaximum(999999.99999)
        exit_layout.addWidget(self.exit_input)
        row2.addLayout(exit_layout)
        
        qty_layout = QVBoxLayout()
        qty_layout.addWidget(QLabel("Quantity"))
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setDecimals(2)
        self.quantity_input.setMaximum(999999.99)
        self.quantity_input.setValue(1.0)
        qty_layout.addWidget(self.quantity_input)
        row2.addLayout(qty_layout)
        
        basic_layout.addLayout(row2)
        
        # Row 3: Outcome and Setup
        row3 = QHBoxLayout()
        
        outcome_layout = QVBoxLayout()
        outcome_layout.addWidget(QLabel("Outcome"))
        self.outcome_input = QComboBox()
        self.outcome_input.addItems(["Pending", "Win", "Loss", "Break Even"])
        outcome_layout.addWidget(self.outcome_input)
        row3.addLayout(outcome_layout, 1)
        
        setup_layout = QVBoxLayout()
        setup_layout.addWidget(QLabel("Setup Type"))
        self.setup_input = QLineEdit()
        self.setup_input.setPlaceholderText("e.g., FVG + OB Confluence")
        setup_layout.addWidget(self.setup_input)
        row3.addLayout(setup_layout, 2)
        
        basic_layout.addLayout(row3)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Concepts Used
        concepts_group = QGroupBox("ICT Concepts Used (one per line)")
        concepts_layout = QVBoxLayout()
        self.concepts_input = QTextEdit()
        self.concepts_input.setMaximumHeight(100)
        self.concepts_input.setPlaceholderText("Fair Value Gap\nOrder Block\nLiquidity Sweep")
        concepts_layout.addWidget(self.concepts_input)
        concepts_group.setLayout(concepts_layout)
        layout.addWidget(concepts_group)
        
        # Notes
        notes_group = QGroupBox("Trade Notes & Analysis")
        notes_layout = QVBoxLayout()
        self.trade_notes_input = QTextEdit()
        self.trade_notes_input.setMinimumHeight(150)
        self.trade_notes_input.setPlaceholderText(
            "What did you see?\nWhy did you enter?\nWhat was the confluence?\nHow did it play out?"
        )
        notes_layout.addWidget(self.trade_notes_input)
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Screenshot
        screenshot_group = QGroupBox("Chart Screenshot")
        screenshot_layout = QHBoxLayout()
        self.screenshot_path = QLineEdit()
        self.screenshot_path.setPlaceholderText("No screenshot selected")
        self.screenshot_path.setReadOnly(True)
        screenshot_layout.addWidget(self.screenshot_path)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_screenshot)
        screenshot_layout.addWidget(browse_btn)
        
        screenshot_group.setLayout(screenshot_layout)
        layout.addWidget(screenshot_group)
        
        # Save button
        save_btn = QPushButton("💾 Save Trade")
        save_btn.setMinimumHeight(45)
        save_btn.clicked.connect(self.save_trade)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        layout.addWidget(save_btn)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        return panel
    
    def load_trades(self):
        """Load all trades into table"""
        self.trade_table.setRowCount(0)
        trades = self.db.get_all_trades()
        
        for trade in trades:
            row = self.trade_table.rowCount()
            self.trade_table.insertRow(row)
            
            self.trade_table.setItem(row, 0, QTableWidgetItem(trade['date']))
            self.trade_table.setItem(row, 1, QTableWidgetItem(trade['pair']))
            self.trade_table.setItem(row, 2, QTableWidgetItem(trade['direction'].upper()))
            self.trade_table.setItem(row, 3, QTableWidgetItem(
                f"{trade['entry_price']:.5f}" if trade['entry_price'] else "-"
            ))
            self.trade_table.setItem(row, 4, QTableWidgetItem(
                f"{trade['exit_price']:.5f}" if trade['exit_price'] else "-"
            ))
            
            # P&L
            pnl_item = QTableWidgetItem(
                f"${trade['pnl']:.2f}" if trade['pnl'] else "-"
            )
            if trade['pnl']:
                pnl_item.setForeground(QColor("#10b981" if trade['pnl'] > 0 else "#dc2626"))
            self.trade_table.setItem(row, 5, pnl_item)
            
            # P&L %
            pnl_pct_item = QTableWidgetItem(
                f"{trade['pnl_percent']:.2f}%" if trade['pnl_percent'] else "-"
            )
            if trade['pnl_percent']:
                pnl_pct_item.setForeground(QColor("#10b981" if trade['pnl_percent'] > 0 else "#dc2626"))
            self.trade_table.setItem(row, 6, pnl_pct_item)
            
            # Outcome
            outcome_item = QTableWidgetItem(trade['outcome'].title())
            if trade['outcome'] == 'win':
                outcome_item.setForeground(QColor("#10b981"))
            elif trade['outcome'] == 'loss':
                outcome_item.setForeground(QColor("#dc2626"))
            elif trade['outcome'] == 'pending':
                outcome_item.setForeground(QColor("#f59e0b"))
            self.trade_table.setItem(row, 7, outcome_item)
            
            self.trade_table.setItem(row, 8, QTableWidgetItem(trade.get('setup_type', '')))
            self.trade_table.setItem(row, 9, QTableWidgetItem(
                ', '.join(trade.get('concepts_used', []))
            ))
            
            # Store trade ID
            self.trade_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, trade['id'])
    
    def filter_trades(self):
        """Filter trades by outcome"""
        outcome_filter = self.outcome_filter.currentText().lower()
        
        for row in range(self.trade_table.rowCount()):
            outcome_item = self.trade_table.item(row, 7)
            if outcome_filter == "all":
                self.trade_table.setRowHidden(row, False)
            else:
                outcome = outcome_item.text().lower()
                self.trade_table.setRowHidden(row, outcome != outcome_filter)
    
    def on_trade_selected(self, row, col):
        """Load selected trade details"""
        trade_id = self.trade_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.current_trade_id = trade_id
        trade = self.db.get_trade_by_id(trade_id)
        
        if trade:
            self.date_input.setDate(QDate.fromString(trade['date'], "yyyy-MM-dd"))
            self.pair_input.setText(trade['pair'])
            self.timeframe_input.setCurrentText(trade['timeframe'])
            self.direction_input.setCurrentText(trade['direction'].title())
            
            self.entry_input.setValue(trade['entry_price'] or 0)
            self.sl_input.setValue(trade['stop_loss'] or 0)
            self.tp_input.setValue(trade['take_profit'] or 0)
            self.exit_input.setValue(trade['exit_price'] or 0)
            self.quantity_input.setValue(trade['quantity'] or 1)
            
            self.outcome_input.setCurrentText(trade['outcome'].title())
            self.setup_input.setText(trade.get('setup_type', ''))
            self.trade_notes_input.setText(trade.get('notes', ''))
            self.screenshot_path.setText(trade.get('screenshot_path', ''))
            
            self.concepts_input.setText('\n'.join(trade.get('concepts_used', [])))
    
    def add_new_trade(self):
        """Clear form for new trade"""
        self.current_trade_id = None
        self.date_input.setDate(QDate.currentDate())
        self.pair_input.clear()
        self.timeframe_input.setCurrentIndex(0)
        self.direction_input.setCurrentIndex(0)
        self.entry_input.setValue(0)
        self.sl_input.setValue(0)
        self.tp_input.setValue(0)
        self.exit_input.setValue(0)
        self.quantity_input.setValue(1.0)
        self.outcome_input.setCurrentIndex(0)
        self.setup_input.clear()
        self.trade_notes_input.clear()
        self.screenshot_path.clear()
        self.concepts_input.clear()
        self.pair_input.setFocus()
    
    def select_screenshot(self):
        """Select screenshot file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Chart Screenshot",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if filename:
            self.screenshot_path.setText(filename)
    
    def save_trade(self):
        """Save current trade"""
        pair = self.pair_input.text().strip()
        if not pair:
            QMessageBox.warning(self, "Error", "Please enter a currency pair")
            return
        
        date = self.date_input.date().toString("yyyy-MM-dd")
        timeframe = self.timeframe_input.currentText()
        direction = self.direction_input.currentText().lower()
        entry = self.entry_input.value() if self.entry_input.value() > 0 else None
        sl = self.sl_input.value() if self.sl_input.value() > 0 else None
        tp = self.tp_input.value() if self.tp_input.value() > 0 else None
        exit_p = self.exit_input.value() if self.exit_input.value() > 0 else None
        qty = self.quantity_input.value()
        outcome = self.outcome_input.currentText().lower()
        setup = self.setup_input.text()
        notes = self.trade_notes_input.toPlainText()
        screenshot = self.screenshot_path.text()
        
        concepts = [c.strip() for c in self.concepts_input.toPlainText().split('\n') if c.strip()]
        
        if self.current_trade_id:
            # Update existing
            self.db.update_trade(
                self.current_trade_id,
                date=date,
                pair=pair,
                timeframe=timeframe,
                direction=direction,
                entry_price=entry,
                stop_loss=sl,
                take_profit=tp,
                exit_price=exit_p,
                quantity=qty,
                outcome=outcome,
                setup_type=setup,
                notes=notes,
                screenshot_path=screenshot,
                concepts_used=concepts
            )
            QMessageBox.information(self, "Success", "Trade updated successfully!")
        else:
            # Add new
            self.db.add_trade(
                date=date,
                pair=pair,
                timeframe=timeframe,
                direction=direction,
                entry_price=entry,
                stop_loss=sl,
                take_profit=tp,
                exit_price=exit_p,
                quantity=qty,
                outcome=outcome,
                setup_type=setup,
                notes=notes,
                screenshot_path=screenshot,
                concepts_used=concepts
            )
            QMessageBox.information(self, "Success", "Trade added successfully!")
        
        self.load_trades()
    
    def delete_trade(self):
        """Delete selected trade"""
        if not self.current_trade_id:
            QMessageBox.warning(self, "Error", "Please select a trade to delete")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this trade?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_trade(self.current_trade_id)
            self.add_new_trade()
            self.load_trades()
            QMessageBox.information(self, "Success", "Trade deleted successfully!")