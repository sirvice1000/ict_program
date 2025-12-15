"""
Knowledge Base Tab - Learn ICT concepts one at a time
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QTextEdit, QGroupBox,
                            QScrollArea, QSplitter, QFrame, QMessageBox,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QTabWidget, QGridLayout, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QColor
from database.db_manager import DatabaseManager

class KnowledgeTab(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.concept_cards = {}
        self.init_ui()
        self.load_concept_notes()
        
    def init_ui(self):
        """Initialize the knowledge base interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📚 ICT Knowledge Base")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3b82f6;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Save all button
        save_all_btn = QPushButton("💾 Save All Notes")
        save_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 24px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        save_all_btn.clicked.connect(self.save_all_notes)
        header_layout.addWidget(save_all_btn)
        
        layout.addLayout(header_layout)
        
        # Create tab widget for different sections
        self.tab_widget = QTabWidget()
        
        # Core Concepts Tab
        concepts_tab = self.create_concepts_section()
        self.tab_widget.addTab(concepts_tab, "Core Concepts")
        
        # Time & Price Tab (NEW)
        time_price_tab = self.create_time_price_section()
        self.tab_widget.addTab(time_price_tab, "⏰ Time & Price Analysis")
        
        # Additional Resources Tab
        resources_tab = self.create_resources_section()
        self.tab_widget.addTab(resources_tab, "Quick Notes")
        
        layout.addWidget(self.tab_widget)
        
    def create_concepts_section(self):
        """Create the core concepts section"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Core ICT Concepts
        left_panel = self.create_core_concepts_panel()
        splitter.addWidget(left_panel)
        
        # Right: Additional concepts (future)
        right_panel = self.create_additional_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 400])
        layout.addWidget(splitter)
        
        return widget
        
    def create_time_price_section(self):
        """Create Time & Price analysis section with algo macro times"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Title and description
        title = QLabel("⏰ ICT Algorithmic Macro Times - Weekly Overview")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #fbbf24; margin-bottom: 5px;")
        layout.addWidget(title)
        
        subtitle = QLabel(
            "TIME THEN PRICE: These are the specific times when algorithms execute, "
            "creating predictable price movements. Focus on these windows for high-probability setups."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #94a3b8; font-size: 13px; margin-bottom: 10px; padding: 10px; background-color: #1e293b; border-radius: 6px;")
        layout.addWidget(subtitle)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        # Weekly Calendar Grid
        calendar_group = self.create_weekly_calendar()
        content_layout.addWidget(calendar_group)
        
        # Macro Times Reference
        macros_group = self.create_macro_times_reference()
        content_layout.addWidget(macros_group)
        
        # Your Observations
        observations_group = self.create_observations_section()
        content_layout.addWidget(observations_group)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return widget
        
    def create_weekly_calendar(self):
        """Create weekly calendar view with macro time indicators"""
        group = QGroupBox("Weekly Macro Time Map")
        group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; color: #fbbf24; }")
        
        layout = QVBoxLayout()
        
        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel("Legend:"))
        
        legend_items = [
            ("🟢 Major Macro", "#10b981"),
            ("🟡 Standard Macro", "#fbbf24"),
            ("🔴 Killzone", "#dc2626"),
            ("🔵 EOD/EO4H", "#3b82f6")
        ]
        
        for label, color in legend_items:
            lbl = QLabel(label)
            lbl.setStyleSheet(f"background-color: {color}22; color: {color}; padding: 4px 8px; border-radius: 4px; font-size: 11px;")
            legend_layout.addWidget(lbl)
        
        legend_layout.addStretch()
        layout.addLayout(legend_layout)
        
        # Weekly table
        self.weekly_table = QTableWidget()
        self.weekly_table.setColumnCount(8)  # Time + 7 days
        self.weekly_table.setRowCount(24)  # 24 hours
        
        headers = ["Hour (EST)", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.weekly_table.setHorizontalHeaderLabels(headers)
        
        # Populate hours
        for hour in range(24):
            time_item = QTableWidgetItem(f"{hour:02d}:00")
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.weekly_table.setItem(hour, 0, time_item)
            
            # Add cells for each day
            for day in range(1, 8):
                cell = QTableWidgetItem("")
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.weekly_table.setItem(hour, day, cell)
        
        # Highlight key macro times
        self.highlight_macro_times()
        
        self.weekly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.weekly_table.verticalHeader().setVisible(False)
        self.weekly_table.setMaximumHeight(600)
        
        layout.addWidget(self.weekly_table)
        
        group.setLayout(layout)
        return group
        
    def highlight_macro_times(self):
        """Highlight algo macro times in the weekly calendar"""
        
        # Define macro times (EST) - these are the key algorithmic execution windows
        macro_times = {
            # Format: (hour, minute_start, minute_end): (color, label, description)
            
            # EVERY HOUR x:50-x:10 Macro (20 minutes)
            'hourly_macro': {
                'times': [(h, 50, 10) for h in range(24)],  # Every hour
                'color': '#fbbf2444',
                'label': '🟡',
                'desc': '20min Macro'
            },
            
            # Major Killzone Times
            'london_open': {
                'times': [(2, 0, 0), (3, 0, 0)],  # 2:00-4:00 AM EST
                'color': '#dc262644',
                'label': '🔴 London',
                'desc': 'London Open Killzone'
            },
            
            'ny_open': {
                'times': [(8, 30, 0), (9, 0, 0), (9, 30, 0), (10, 0, 0)],  # 8:30-11:00 AM EST
                'color': '#dc262644',
                'label': '🔴 NY AM',
                'desc': 'New York AM Killzone'
            },
            
            'ny_lunch': {
                'times': [(11, 0, 0), (12, 0, 0), (13, 0, 0)],  # 11:00 AM-2:00 PM EST
                'color': '#3b82f644',
                'label': '🔵 Lunch',
                'desc': 'NY Lunch Macro'
            },
            
            'ny_pm': {
                'times': [(13, 0, 0), (14, 0, 0), (15, 0, 0)],  # 1:00-4:00 PM EST
                'color': '#dc262644',
                'label': '🔴 NY PM',
                'desc': 'New York PM Killzone'
            },
            
            # End of Day/4H Macros
            'eod': {
                'times': [(15, 0, 0), (16, 0, 0)],  # 3:00-5:00 PM EST
                'color': '#3b82f644',
                'label': '🔵 EOD',
                'desc': 'End of Day Macro'
            },
        }
        
        # Days when markets are active (Mon-Fri = columns 2-6)
        active_days = [2, 3, 4, 5, 6]  # Monday to Friday
        
        # Apply hourly macros to all days
        for hour in range(24):
            for day in range(1, 8):  # All days
                cell = self.weekly_table.item(hour, day)
                if cell:
                    # Add 50-10 minute macro indicator
                    cell.setBackground(QColor(macro_times['hourly_macro']['color']))
                    cell.setText(macro_times['hourly_macro']['label'])
                    cell.setToolTip(f"{hour:02d}:50-{(hour+1)%24:02d}:10\n{macro_times['hourly_macro']['desc']}")
        
        # Apply specific killzone times (only on trading days)
        for macro_type, macro_data in macro_times.items():
            if macro_type == 'hourly_macro':
                continue  # Already applied
                
            for hour, _, _ in macro_data['times']:
                for day in active_days:
                    cell = self.weekly_table.item(hour, day)
                    if cell:
                        # Overlay killzone color (stronger)
                        cell.setBackground(QColor(macro_data['color']))
                        cell.setText(macro_data['label'])
                        cell.setToolTip(f"{hour:02d}:00\n{macro_data['desc']}")
        
        # Mark Sunday evening (18:00) as market open
        sunday_open = self.weekly_table.item(18, 1)
        if sunday_open:
            sunday_open.setBackground(QColor("#10b98144"))
            sunday_open.setText("📈 Open")
            sunday_open.setToolTip("18:00 EST - Market Week Opens")
        
        # Mark Friday afternoon (17:00) as market close
        friday_close = self.weekly_table.item(17, 6)
        if friday_close:
            friday_close.setBackground(QColor("#6b728044"))
            friday_close.setText("📉 Close")
            friday_close.setToolTip("17:00 EST - Market Week Closes")
    
    def create_macro_times_reference(self):
        """Create detailed macro times reference guide"""
        group = QGroupBox("Algorithmic Macro Times - Detailed Reference")
        group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; color: #a78bfa; }")
        
        layout = QVBoxLayout()
        
        # Create reference table
        ref_table = QTableWidget()
        ref_table.setColumnCount(5)
        ref_table.setHorizontalHeaderLabels(["Time Window (EST)", "Type", "Duration", "Expected Behavior", "Trading Notes"])
        
        macro_data = [
            # [Time, Type, Duration, Expected Behavior, Trading Notes]
            ["Every Hour\n:50 to :10", "Hourly Macro", "20 minutes", 
             "Price expansion or reversal\nLiquidity sweep possible", 
             "Watch for stops being run before the move\nHigh probability setup window"],
             
            ["00:00 - 05:00", "Asian Session", "5 hours", 
             "Range formation\nLower volatility", 
             "Look for range highs/lows as liquidity\nOften sets up London move"],
             
            ["02:00 - 05:00", "London Killzone", "3 hours", 
             "Strong directional moves\nLiquidity sweeps common", 
             "Powerful moves - major players active\nWatch 02:33 and 03:00 macros"],
             
            ["08:30 - 11:00", "NY AM Killzone", "2.5 hours", 
             "Highest volume period\nNews reaction and continuation", 
             "Primary trading window\n08:50-09:10 is critical\nWatch news at 08:30"],
             
            ["10:00 - 11:00", "Silver Bullet", "1 hour", 
             "Clean directional move\nMinimal retracements", 
             "Very high probability\nOften continues trend of day"],
             
            ["11:00 - 14:00", "Lunch Macro", "3 hours", 
             "Consolidation typical\nFalse breakouts common", 
             "Lower probability for entries\nGood for assessing bias"],
             
            ["13:00 - 16:00", "NY PM Killzone", "3 hours", 
             "Second major push\nReversals possible", 
             "14:00-15:00 often strongest\nWatch for EOD positioning"],
             
            ["15:00 - 17:00", "End of Day (EOD)", "2 hours", 
             "Settlement activities\nProfit taking", 
             "Lower timeframe reversals\nPreparing for next day"],
             
            ["16:00", "4H Candle Close", "Moment", 
             "Major algorithmic reference\nPrice delivery key level", 
             "Critical for daily bias\nWatch for stop runs before/after"],
        ]
        
        ref_table.setRowCount(len(macro_data))
        
        for row, data in enumerate(macro_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
                # Color code by type
                if "Killzone" in data[1]:
                    item.setBackground(QColor("#dc262622"))
                elif "Macro" in data[1]:
                    item.setBackground(QColor("#fbbf2422"))
                elif "Silver Bullet" in data[1]:
                    item.setBackground(QColor("#10b98122"))
                    
                ref_table.setItem(row, col, item)
        
        ref_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        ref_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        ref_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        ref_table.setMaximumHeight(400)
        
        layout.addWidget(ref_table)
        
        # Add important notes
        notes = QLabel(
            "⚠️ KEY PRINCIPLES:\n\n"
            "• TIME THEN PRICE: Wait for the right time window before expecting price movement\n"
            "• The 20-minute macro (x:50-x:10) happens EVERY hour - this is algorithmic execution\n"
            "• Killzones have the highest probability - but still need proper setup\n"
            "• Sunday 18:00 to Friday 17:00 EST is the full trading week\n"
            "• Major news events override normal macro behavior - be cautious\n"
            "• Combine time analysis with FVG, Order Blocks, and liquidity for best results"
        )
        notes.setWordWrap(True)
        notes.setStyleSheet("""
            background-color: #422006;
            color: #fbbf24;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #fbbf24;
            font-size: 12px;
            line-height: 1.6;
        """)
        layout.addWidget(notes)
        
        group.setLayout(layout)
        return group
    
    def create_observations_section(self):
        """Create section for user to track their own time-based observations"""
        group = QGroupBox("📝 Your Time & Price Observations")
        group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; color: #10b981; }")
        
        layout = QVBoxLayout()
        
        instructions = QLabel(
            "Track what you observe during specific macro times:\n"
            "• Which times work best for your trading style?\n"
            "• What patterns repeat at specific times?\n"
            "• How does your asset behave during each macro?\n"
            "• When do you see the cleanest setups?"
        )
        instructions.setStyleSheet("color: #94a3b8; font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(instructions)
        
        self.time_observations = QTextEdit()
        self.time_observations.setPlaceholderText(
            "Example observations:\n\n"
            "02:33 - London opening - GOLD often sweeps Asian highs then reverses\n"
            "08:50-09:10 - NY AM macro - Best entry window for continuing overnight trend\n"
            "10:00 Silver Bullet - Clean moves, minimal drawdown\n"
            "14:15 - Often see reversal if NY AM trend exhausted\n\n"
            "Track your wins and losses by time to find your edge..."
        )
        self.time_observations.setMinimumHeight(200)
        layout.addWidget(self.time_observations)
        
        group.setLayout(layout)
        return group
    
    def create_core_concepts_panel(self):
        """Create panel for core ICT concepts"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Core ICT Concepts")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        
        # Core concepts - starting with FVG and Order Blocks
        core_concepts = [
            ("Fair Value Gap (FVG)", "FVG", self.get_fvg_content()),
            ("Order Blocks (OB)", "OB", self.get_ob_content()),
        ]
        
        for display_name, short_name, concept_data in core_concepts:
            card = self.create_concept_card(display_name, short_name, concept_data)
            content_layout.addWidget(card)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return panel
    
    def create_resources_section(self):
        """Create panel for additional concepts and custom notes"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Quick Notes & References")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #a78bfa; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Quick notes area
        notes_group = QGroupBox("Quick Trading Notes")
        notes_layout = QVBoxLayout()
        
        self.quick_notes = QTextEdit()
        self.quick_notes.setPlaceholderText(
            "Quick notes, observations, things to remember...\n\n"
            "Example:\n"
            "- Always wait for killzone\n"
            "- Check premium/discount first\n"
            "- Look for liquidity sweeps\n"
            "- Combine time + FVG + OB for best setups"
        )
        self.quick_notes.setMinimumHeight(200)
        notes_layout.addWidget(self.quick_notes)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Coming soon concepts
        coming_soon = QGroupBox("Coming Soon")
        coming_layout = QVBoxLayout()
        
        future_concepts = [
            "Break of Structure (BOS)",
            "Market Structure Shift (MSS)",
            "Liquidity Sweeps",
            "Killzones (Detailed)",
            "Premium/Discount Arrays",
            "Optimal Trade Entry (OTE)",
            "Breaker Blocks",
            "Mitigation Blocks",
            "Silver Bullet Setups",
            "Power of 3"
        ]
        
        for concept in future_concepts:
            label = QLabel(f"• {concept}")
            label.setStyleSheet("color: #64748b; font-size: 13px; padding: 2px;")
            coming_layout.addWidget(label)
        
        coming_layout.addStretch()
        coming_soon.setLayout(coming_layout)
        layout.addWidget(coming_soon)
        
        layout.addStretch()
        
        return panel
    
    def create_additional_panel(self):
        """Create panel for additional concepts and custom notes"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Quick Notes & References")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #a78bfa; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Quick notes area
        notes_group = QGroupBox("Quick Trading Notes")
        notes_layout = QVBoxLayout()
        
        self.quick_notes = QTextEdit()
        self.quick_notes.setPlaceholderText(
            "Quick notes, observations, things to remember...\n\n"
            "Example:\n"
            "- Always wait for killzone\n"
            "- Check premium/discount first\n"
            "- Look for liquidity sweeps"
        )
        self.quick_notes.setMinimumHeight(200)
        notes_layout.addWidget(self.quick_notes)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Coming soon concepts
        coming_soon = QGroupBox("Coming Soon")
        coming_layout = QVBoxLayout()
        
        future_concepts = [
            "Break of Structure (BOS)",
            "Market Structure Shift (MSS)",
            "Liquidity Sweeps",
            "Killzones",
            "Premium/Discount Arrays",
            "Optimal Trade Entry (OTE)",
            "Breaker Blocks",
            "Mitigation Blocks"
        ]
        
        for concept in future_concepts:
            label = QLabel(f"• {concept}")
            label.setStyleSheet("color: #64748b; font-size: 13px; padding: 2px;")
            coming_layout.addWidget(label)
        
        coming_layout.addStretch()
        coming_soon.setLayout(coming_layout)
        layout.addWidget(coming_soon)
        
        layout.addStretch()
        
        return panel
    
    def create_concept_card(self, display_name, short_name, concept_data):
        """Create an expandable concept card"""
        card = QGroupBox(display_name)
        card.setStyleSheet("""
            QGroupBox {
                font-size: 15px;
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
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Summary (always visible)
        summary_label = QLabel(concept_data['summary'])
        summary_label.setWordWrap(True)
        summary_label.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: normal; padding: 5px;")
        layout.addWidget(summary_label)
        
        # Key points (always visible)
        if concept_data.get('key_points'):
            points_label = QLabel("Key Points:")
            points_label.setStyleSheet("color: #10b981; font-size: 12px; font-weight: bold; margin-top: 5px;")
            layout.addWidget(points_label)
            
            for point in concept_data['key_points'][:3]:  # Show first 3 points
                point_label = QLabel(f"• {point}")
                point_label.setWordWrap(True)
                point_label.setStyleSheet("color: #cbd5e1; font-size: 12px; font-weight: normal; padding-left: 10px;")
                layout.addWidget(point_label)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #475569; margin: 8px 0;")
        layout.addWidget(line)
        
        # Your personal notes section
        notes_label = QLabel("📝 Your Notes:")
        notes_label.setStyleSheet("color: #fbbf24; font-size: 13px; font-weight: bold;")
        layout.addWidget(notes_label)
        
        notes_area = QTextEdit()
        notes_area.setPlaceholderText(
            f"Add your personal notes about {display_name} here...\n\n"
            "What works for you? What have you observed?\n"
            "Screenshots, examples, trade results..."
        )
        notes_area.setMaximumHeight(150)
        notes_area.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        layout.addWidget(notes_area)
        
        # Store reference
        self.concept_cards[short_name] = {
            'notes': notes_area,
            'data': concept_data
        }
        
        card.setLayout(layout)
        return card
    
    def get_fvg_content(self):
        """Get Fair Value Gap content"""
        return {
            'summary': 'A three-candle price imbalance where the market moved so fast it left an unfilled gap. Price often returns to "fill" these gaps.',
            'key_points': [
                'FVGs represent footprints of institutional order flow',
                'Consequent Encroachment (50% level) is the strongest reaction point',
                'Best used during killzone times when volatility is high',
                'Combine with BOS/MSS for highest probability setups',
                'FVGs can invert (IFVG) when price breaks through completely',
                'Not every FVG is tradeable - context and confluence matter'
            ],
            'definition': """
**Bullish FVG:**
- High of Candle 1 does NOT overlap with Low of Candle 3
- Gap = area between them
- Acts as SUPPORT when price returns

**Bearish FVG:**
- Low of Candle 1 does NOT overlap with High of Candle 3
- Gap = area between them
- Acts as RESISTANCE when price returns

**Entry Methods:**
1. Aggressive: Enter at start of gap
2. Standard: Enter at 50% (Consequent Encroachment)
3. Conservative: Wait for confirmation

**Invalidation:**
- Price closes completely through it without reaction
""",
            'category': 'ICT Concepts'
        }
    
    def get_ob_content(self):
        """Get Order Blocks content"""
        return {
            'summary': 'Zones where institutional traders placed large orders, creating areas that act as support or resistance when price returns.',
            'key_points': [
                'The last opposite candle before an impulsive move is the OB',
                'Works best when aligned with higher timeframe trend',
                'OBs get weaker with multiple tests - first test is strongest',
                'Failed Order Blocks become Breaker Blocks (polarity change)',
                'Best during killzone times when institutions are active',
                'Use 50% of OB (Mean Threshold) for better entry'
            ],
            'definition': """
**Bullish Order Block:**
- Last BEARISH candle before strong bullish move
- Represents where institutions placed BUY orders
- Acts as SUPPORT when price returns

**Bearish Order Block:**
- Last BULLISH candle before strong bearish move
- Represents where institutions placed SELL orders
- Acts as RESISTANCE when price returns

**Entry Methods:**
1. Aggressive: Buy/Sell stop above/below key candles
2. Conservative: Wait for price to return to OB zone
3. High Probability: Combine with FVG + liquidity sweep

**Stop Loss:**
- Bullish OB: 10-20 pips below the low
- Bearish OB: 10-20 pips above the high

**Invalidation:**
- Price closes completely through without reaction
""",
            'category': 'ICT Concepts'
        }
    
    def save_all_notes(self):
        """Save all personal notes to database"""
        saved = 0
        
        # Save concept notes
        for concept_id, card in self.concept_cards.items():
            notes = card['notes'].toPlainText().strip()
            if notes:
                # Save to database
                self.db.save_concept_notes(concept_id, notes)
                saved += 1
        
        # Save quick notes
        quick_notes = self.quick_notes.toPlainText().strip()
        if quick_notes:
            self.db.save_concept_notes('QUICK_NOTES', quick_notes)
            saved += 1
        
        # Save time & price observations
        if hasattr(self, 'time_observations'):
            time_obs = self.time_observations.toPlainText().strip()
            if time_obs:
                self.db.save_concept_notes('TIME_PRICE_OBSERVATIONS', time_obs)
                saved += 1
        
        if saved > 0:
            QMessageBox.information(
                self,
                "Saved",
                f"Saved notes for {saved} section(s)!"
            )
        else:
            QMessageBox.information(
                self,
                "Nothing to Save",
                "No notes to save. Add some notes first!"
            )
    
    def load_concept_notes(self):
        """Load saved notes from database"""
        for concept_id, card in self.concept_cards.items():
            notes = self.db.get_concept_notes(concept_id)
            if notes:
                card['notes'].setPlainText(notes)
        
        # Load quick notes
        quick_notes = self.db.get_concept_notes('QUICK_NOTES')
        if quick_notes:
            self.quick_notes.setPlainText(quick_notes)
        
        # Load time & price observations (after UI is created)
        if hasattr(self, 'time_observations'):
            time_obs = self.db.get_concept_notes('TIME_PRICE_OBSERVATIONS')
            if time_obs:
                self.time_observations.setPlainText(time_obs)