"""
Time Then Price Tab - ICT Algorithmic Macro Times Analysis
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QScrollArea, QGroupBox, QFrame, QTableWidget,
                            QTableWidgetItem, QHeaderView, QSplitter)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QDateTime
from PyQt6.QtGui import QColor, QFont
from database.db_manager import DatabaseManager
import datetime

class TimeThenPriceTab(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.init_ui()
        self.setup_countdown_timer()
        
    def init_ui(self):
        """Initialize the Time Then Price interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("⏰ TIME THEN PRICE - Algorithmic Macro Times")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #fbbf24;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Current time display
        self.current_time_label = QLabel()
        self.current_time_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #10b981;
            background-color: #1e293b;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid #10b981;
        """)
        header_layout.addWidget(self.current_time_label)
        
        layout.addLayout(header_layout)
        
        # Key Principles Section
        principles = self.create_key_principles()
        layout.addWidget(principles)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Weekly timeline view
        timeline_panel = self.create_timeline_panel()
        splitter.addWidget(timeline_panel)
        
        # Right side: Countdown timer and macro reference
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([800, 400])
        layout.addWidget(splitter)
        
    def create_key_principles(self):
        """Create key principles section"""
        group = QGroupBox("🎯 KEY PRINCIPLES - TIME THEN PRICE")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #fbbf24;
                background-color: #422006;
                border: 2px solid #fbbf24;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        principles_text = QLabel(
            "• TIME THEN PRICE: Wait for the algorithmic time window BEFORE expecting price movement\n"
            "• The 20-minute macro (:50 to :10) occurs EVERY HOUR - this is algorithmic execution\n"
            "• Killzones (London Open, NY AM, NY PM) have the highest probability when combined with proper setup\n"
            "• Do NOT trade randomly - wait for these specific time windows\n"
            "• Combine time analysis with FVG, Order Blocks, and liquidity for maximum edge\n"
            "• The algorithm operates on schedule - learn it, respect it, profit from it"
        )
        principles_text.setWordWrap(True)
        principles_text.setStyleSheet("""
            color: #fbbf24;
            font-size: 13px;
            line-height: 1.8;
            padding: 10px;
        """)
        layout.addWidget(principles_text)
        
        group.setLayout(layout)
        return group
    
    def create_timeline_panel(self):
        """Create the weekly timeline view with 7 stacked days"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Weekly Macro Timeline (EST)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scroll area for timelines
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        # Days of the week
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        for day in days:
            day_timeline = self.create_day_timeline(day)
            content_layout.addWidget(day_timeline)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return panel
    
    def create_day_timeline(self, day_name):
        """Create a timeline for a single day"""
        group = QGroupBox(day_name)
        
        # Style based on trading day or weekend
        is_trading_day = day_name not in ["Saturday", "Sunday"]
        
        if is_trading_day:
            group.setStyleSheet("""
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
        else:
            group.setStyleSheet("""
                QGroupBox {
                    font-size: 15px;
                    font-weight: bold;
                    border: 2px solid #64748b;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 15px;
                    background-color: #1e293b;
                }
                QGroupBox::title {
                    color: #94a3b8;
                }
            """)
        
        layout = QHBoxLayout()
        
        # Create 24 hour blocks (simplified visualization)
        hour_layout = QHBoxLayout()
        hour_layout.setSpacing(1)
        
        for hour in range(24):
            hour_block = self.create_hour_block(hour, day_name)
            hour_layout.addWidget(hour_block)
        
        layout.addLayout(hour_layout)
        
        group.setLayout(layout)
        return group
    
    def create_hour_block(self, hour, day_name):
        """Create a visual block for one hour with macro indication"""
        block = QFrame()
        block.setFixedWidth(30)
        block.setFixedHeight(60)
        
        # Determine if this hour has a macro
        macro_info = self.get_macro_for_hour(hour, day_name)
        
        if macro_info:
            color = macro_info['color']
            tooltip = f"{hour:02d}:00 - {macro_info['name']}\n{macro_info['type']}"
        else:
            color = "#334155"
            tooltip = f"{hour:02d}:00"
        
        block.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid #475569;
                border-radius: 3px;
            }}
            QFrame:hover {{
                border: 2px solid #fbbf24;
            }}
        """)
        
        block.setToolTip(tooltip)
        
        # Add hour label
        block_layout = QVBoxLayout(block)
        block_layout.setContentsMargins(2, 2, 2, 2)
        
        hour_label = QLabel(f"{hour:02d}")
        hour_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hour_label.setStyleSheet("color: #e2e8f0; font-size: 10px; font-weight: bold;")
        block_layout.addWidget(hour_label)
        
        return block
    
    def get_macro_for_hour(self, hour, day_name):
        """Determine if a specific hour has a macro event"""
        is_trading_day = day_name not in ["Saturday", "Sunday"]
        
        # Sunday evening market open
        if day_name == "Sunday" and hour == 18:
            return {
                'name': 'Market Open',
                'type': 'Weekly Open',
                'color': '#10b981'
            }
        
        # Friday afternoon market close
        if day_name == "Friday" and hour == 17:
            return {
                'name': 'Market Close',
                'type': 'Weekly Close',
                'color': '#6b7280'
            }
        
        if not is_trading_day:
            return None
        
        # London Killzone (2:00-5:00 AM)
        if 2 <= hour < 5:
            return {
                'name': 'London Killzone',
                'type': 'Major Killzone',
                'color': '#dc2626'
            }
        
        # NY AM Killzone (8:30-11:00 AM)
        if 8 <= hour < 11:
            return {
                'name': 'NY AM Killzone',
                'type': 'Major Killzone',
                'color': '#dc2626'
            }
        
        # NY Lunch (11:00 AM-2:00 PM)
        if 11 <= hour < 14:
            return {
                'name': 'Lunch Macro',
                'type': 'Consolidation Period',
                'color': '#3b82f6'
            }
        
        # NY PM Killzone (1:00-4:00 PM)
        if 13 <= hour < 16:
            return {
                'name': 'NY PM Killzone',
                'type': 'Major Killzone',
                'color': '#dc2626'
            }
        
        # Asian Session (midnight-5:00 AM)
        if 0 <= hour < 5:
            return {
                'name': 'Asian Session',
                'type': 'Range Formation',
                'color': '#8b5cf6'
            }
        
        # Regular trading hour
        return {
            'name': f'{hour:02d}:50-{(hour+1)%24:02d}:10',
            'type': '20min Macro',
            'color': '#fbbf24'
        }
    
    def create_right_panel(self):
        """Create right panel with countdown and reference"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Countdown timer section
        countdown_group = self.create_countdown_section()
        layout.addWidget(countdown_group)
        
        # Macro reference table
        reference_group = self.create_macro_reference()
        layout.addWidget(reference_group)
        
        return panel
    
    def create_countdown_section(self):
        """Create countdown timer for next 5 macros"""
        group = QGroupBox("⏱️ Next 5 Macros")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #10b981;
                border: 2px solid #10b981;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
                background-color: #1e293b;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Countdown table
        self.countdown_table = QTableWidget()
        self.countdown_table.setColumnCount(3)
        self.countdown_table.setHorizontalHeaderLabels(["Macro Name", "Time (EST)", "Countdown"])
        self.countdown_table.setRowCount(5)
        
        self.countdown_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.countdown_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.countdown_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.countdown_table.setMaximumHeight(200)
        
        layout.addWidget(self.countdown_table)
        
        group.setLayout(layout)
        return group
    
    def create_macro_reference(self):
        """Create detailed macro reference table"""
        group = QGroupBox("📋 Macro Reference Guide")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #a78bfa;
                border: 2px solid #a78bfa;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
                background-color: #1e293b;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Scroll area for table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Reference table
        self.macro_table = QTableWidget()
        self.macro_table.setColumnCount(6)
        self.macro_table.setHorizontalHeaderLabels([
            "Time (EST)", "Type", "Macro Name", "Expected Behavior", "Volatility (1-10)", "Notes"
        ])
        
        # Macro data
        macro_data = [
            # [Time, Type, Name, Expected, Volatility, Notes]
            ["Every :50-:10", "Hourly", "20-Minute Macro", "Expansion/Reversal", "5-7", 
             "Happens EVERY hour - algorithmic execution window"],
            
            ["00:00-05:00", "Session", "Asian Range", "Consolidation/Range", "3-4", 
             "Lower volatility - sets up liquidity for London"],
            
            ["02:00-05:00", "Killzone", "London Open", "Strong directional", "8-9", 
             "Major move potential - institutions active"],
            
            ["02:33", "Specific", "London Macro", "Liquidity sweep", "8", 
             "Common sweep of Asian highs/lows"],
            
            ["03:00", "Specific", "London Hour 2", "Continuation", "7-8", 
             "Often confirms London direction"],
            
            ["08:30", "News", "NY Data Release", "High volatility", "9-10", 
             "Economic data - extreme moves possible"],
            
            ["08:50-09:10", "Macro", "NY Open Macro", "Primary trend move", "9", 
             "Critical 20-minute window - best setups"],
            
            ["09:30", "Open", "NYSE Open", "Volume surge", "8-9", 
             "Stock market open - additional volatility"],
            
            ["10:00-11:00", "Setup", "Silver Bullet", "Clean directional", "7-8", 
             "High probability moves - minimal drawdown"],
            
            ["11:00-14:00", "Period", "Lunch Consolidation", "Choppy/ranging", "4-5", 
             "Lower probability - avoid or scalp only"],
            
            ["13:00-16:00", "Killzone", "NY PM Session", "Secondary move", "7-8", 
             "Second major opportunity of the day"],
            
            ["14:00-15:00", "Window", "PM Power Hour", "Strong moves", "7-8", 
             "Often strongest hour of PM session"],
            
            ["15:00-17:00", "Close", "End of Day", "Settlement/reversal", "5-6", 
             "Profit taking and positioning"],
            
            ["16:00", "Close", "4H Candle Close", "Algorithm reference", "6-7", 
             "Major price delivery level - watch for runs"],
        ]
        
        self.macro_table.setRowCount(len(macro_data))
        
        for row, data in enumerate(macro_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                
                # Center align volatility
                if col == 4:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
                # Color code by type
                if "Killzone" in data[1]:
                    item.setBackground(QColor("#dc262622"))
                    item.setForeground(QColor("#fca5a5"))
                elif "Macro" in data[1] or "Hourly" in data[1]:
                    item.setBackground(QColor("#fbbf2422"))
                    item.setForeground(QColor("#fbbf24"))
                elif "Setup" in data[1]:
                    item.setBackground(QColor("#10b98122"))
                    item.setForeground(QColor("#86efac"))
                else:
                    item.setForeground(QColor("#e2e8f0"))
                
                self.macro_table.setItem(row, col, item)
        
        self.macro_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.macro_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        scroll.setWidget(self.macro_table)
        layout.addWidget(scroll)
        
        group.setLayout(layout)
        return group
    
    def setup_countdown_timer(self):
        """Setup timer to update countdown every second"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_countdown()
    
    def update_countdown(self):
        """Update countdown timer and current time"""
        now = QDateTime.currentDateTime()
        
        # Update current time display
        self.current_time_label.setText(
            f"Current Time (EST): {now.toString('dddd, MMMM d, yyyy  hh:mm:ss AP')}"
        )
        
        # Get next 5 macros
        next_macros = self.get_next_macros(now, 5)
        
        # Update countdown table
        for row, macro in enumerate(next_macros):
            # Macro name
            name_item = QTableWidgetItem(macro['name'])
            name_item.setForeground(QColor(macro['color']))
            self.countdown_table.setItem(row, 0, name_item)
            
            # Time
            time_item = QTableWidgetItem(macro['time'].toString('hh:mm AP'))
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.countdown_table.setItem(row, 1, time_item)
            
            # Countdown
            seconds_until = now.secsTo(macro['time'])
            countdown_text = self.format_countdown(seconds_until)
            countdown_item = QTableWidgetItem(countdown_text)
            countdown_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            countdown_item.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
            
            # Color based on urgency
            if seconds_until < 300:  # Less than 5 minutes
                countdown_item.setForeground(QColor("#dc2626"))
            elif seconds_until < 900:  # Less than 15 minutes
                countdown_item.setForeground(QColor("#fbbf24"))
            else:
                countdown_item.setForeground(QColor("#10b981"))
            
            self.countdown_table.setItem(row, 2, countdown_item)
    
    def get_next_macros(self, current_time, count):
        """Get the next N macro times"""
        macros = []
        
        # Define all recurring macros (in minutes from midnight)
        hourly_macros = []
        for hour in range(24):
            # Each hour has a :50 minute macro (lasts until :10 of next hour)
            hourly_macros.append({
                'hour': hour,
                'minute': 50,
                'name': f'{hour:02d}:50 Macro',
                'type': 'hourly',
                'color': '#fbbf24'
            })
        
        # Specific important macros
        special_macros = [
            {'hour': 2, 'minute': 0, 'name': 'London Open', 'type': 'killzone', 'color': '#dc2626'},
            {'hour': 2, 'minute': 33, 'name': 'London 2:33', 'type': 'specific', 'color': '#dc2626'},
            {'hour': 3, 'minute': 0, 'name': 'London Hour 2', 'type': 'killzone', 'color': '#dc2626'},
            {'hour': 8, 'minute': 30, 'name': 'NY Data', 'type': 'news', 'color': '#ef4444'},
            {'hour': 8, 'minute': 50, 'name': 'NY Open Macro', 'type': 'killzone', 'color': '#dc2626'},
            {'hour': 9, 'minute': 30, 'name': 'NYSE Open', 'type': 'open', 'color': '#dc2626'},
            {'hour': 10, 'minute': 0, 'name': 'Silver Bullet Start', 'type': 'setup', 'color': '#10b981'},
            {'hour': 14, 'minute': 0, 'name': 'PM Power Hour', 'type': 'killzone', 'color': '#dc2626'},
            {'hour': 16, 'minute': 0, 'name': '4H Close', 'type': 'close', 'color': '#3b82f6'},
        ]
        
        all_macros = hourly_macros + special_macros
        
        # Get current day and calculate next occurrences
        for macro in all_macros:
            macro_time = QDateTime(current_time.date(), QTime(macro['hour'], macro['minute']))
            
            # If this time has passed today, move to tomorrow
            if macro_time <= current_time:
                macro_time = macro_time.addDays(1)
            
            macros.append({
                'name': macro['name'],
                'time': macro_time,
                'color': macro['color']
            })
        
        # Sort by time and return the next N
        macros.sort(key=lambda x: x['time'])
        return macros[:count]
    
    def format_countdown(self, seconds):
        """Format seconds into countdown string"""
        if seconds < 0:
            return "ACTIVE NOW"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"