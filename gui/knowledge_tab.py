"""
Knowledge Base Tab - Learn ICT concepts one at a time
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QTextEdit, QGroupBox,
                            QScrollArea, QSplitter, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
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
• High of Candle 1 does NOT overlap with Low of Candle 3
• Gap = area between them
• Acts as SUPPORT when price returns

**Bearish FVG:**
• Low of Candle 1 does NOT overlap with High of Candle 3
• Gap = area between them
• Acts as RESISTANCE when price returns

**Entry Methods:**
1. Aggressive: Enter at start of gap
2. Standard: Enter at 50% (Consequent Encroachment)
3. Conservative: Wait for confirmation

**Invalidation:**
• Price closes completely through it without reaction
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
• Last BEARISH candle before strong bullish move
• Represents where institutions placed BUY orders
• Acts as SUPPORT when price returns

**Bearish Order Block:**
• Last BULLISH candle before strong bearish move
• Represents where institutions placed SELL orders
• Acts as RESISTANCE when price returns

**Entry Methods:**
1. Aggressive: Buy/Sell stop above/below key candles
2. Conservative: Wait for price to return to OB zone
3. High Probability: Combine with FVG + liquidity sweep

**Stop Loss:**
• Bullish OB: 10-20 pips below the low
• Bearish OB: 10-20 pips above the high

**Invalidation:**
• Price closes completely through without reaction
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