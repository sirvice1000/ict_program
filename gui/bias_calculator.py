"""
Daily Bias Calculator - Comprehensive checklist for determining daily market bias
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QGroupBox, QCheckBox, QScrollArea,
                            QWidget, QTextEdit, QComboBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DailyBiasCalculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daily Bias Calculator")
        self.setMinimumSize(900, 700)
        self.checkboxes = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the bias calculator interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📊 Daily Bias Calculator")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b82f6;")
        layout.addWidget(header)
        
        subtitle = QLabel("Complete this checklist to determine your daily market bias")
        subtitle.setStyleSheet("font-size: 13px; color: #94a3b8; margin-bottom: 10px;")
        layout.addWidget(subtitle)
        
        # Scroll area for checklist
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        # Section 1: Higher Timeframe Analysis
        htf_group = self.create_htf_section()
        content_layout.addWidget(htf_group)
        
        # Section 2: Previous Day Analysis
        prev_day_group = self.create_prev_day_section()
        content_layout.addWidget(prev_day_group)
        
        # Section 3: Current Day Setup
        current_day_group = self.create_current_day_section()
        content_layout.addWidget(current_day_group)
        
        # Section 4: Market Structure
        structure_group = self.create_structure_section()
        content_layout.addWidget(structure_group)
        
        # Section 5: Liquidity Analysis
        liquidity_group = self.create_liquidity_section()
        content_layout.addWidget(liquidity_group)
        
        # Section 6: Premium/Discount
        pd_group = self.create_premium_discount_section()
        content_layout.addWidget(pd_group)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Result section
        result_layout = self.create_result_section()
        layout.addLayout(result_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        calculate_btn = QPushButton("🎯 Calculate Bias")
        calculate_btn.setMinimumHeight(45)
        calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        calculate_btn.clicked.connect(self.calculate_bias)
        button_layout.addWidget(calculate_btn)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setMinimumHeight(45)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
        """)
        reset_btn.clicked.connect(self.reset_form)
        button_layout.addWidget(reset_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(45)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def create_htf_section(self):
        """Create Higher Timeframe Analysis section"""
        group = QGroupBox("1️⃣ Higher Timeframe Analysis (Weekly/Daily)")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("htf_weekly_trend", "Weekly trend is bullish (higher highs and higher lows)"),
            ("htf_weekly_bearish", "Weekly trend is bearish (lower highs and lower lows)"),
            ("htf_daily_aligned", "Daily timeframe aligns with weekly direction"),
            ("htf_weekly_high", "Price is near weekly high (premium)"),
            ("htf_weekly_low", "Price is near weekly low (discount)"),
            ("htf_weekly_consolidation", "Weekly is in consolidation/range"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_prev_day_section(self):
        """Create Previous Day Analysis section"""
        group = QGroupBox("2️⃣ Previous Day Analysis")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("prev_bullish_close", "Previous day closed bullish (near highs)"),
            ("prev_bearish_close", "Previous day closed bearish (near lows)"),
            ("prev_left_fvg", "Previous day left Fair Value Gaps"),
            ("prev_swept_highs", "Previous day swept/took buy-side liquidity"),
            ("prev_swept_lows", "Previous day swept/took sell-side liquidity"),
            ("prev_range_expansion", "Previous day showed strong range expansion"),
            ("prev_inside_day", "Previous day was an inside day"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_current_day_section(self):
        """Create Current Day Setup section"""
        group = QGroupBox("3️⃣ Current Day Opening & Asian Session")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("current_gap_up", "Market gapped up at open"),
            ("current_gap_down", "Market gapped down at open"),
            ("current_asian_high", "Asian session formed clear high"),
            ("current_asian_low", "Asian session formed clear low"),
            ("current_asian_consolidation", "Asian session consolidated in range"),
            ("current_london_displacement", "London open showed strong displacement"),
            ("current_above_asian_high", "Price is trading above Asian high"),
            ("current_below_asian_low", "Price is trading below Asian low"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_structure_section(self):
        """Create Market Structure section"""
        group = QGroupBox("4️⃣ Market Structure")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("struct_bos_bullish", "Break of Structure (BOS) to the upside"),
            ("struct_bos_bearish", "Break of Structure (BOS) to the downside"),
            ("struct_mss_bullish", "Market Structure Shift (MSS) - bearish to bullish"),
            ("struct_mss_bearish", "Market Structure Shift (MSS) - bullish to bearish"),
            ("struct_hh_hl", "Creating higher highs and higher lows"),
            ("struct_lh_ll", "Creating lower highs and lower lows"),
            ("struct_equal_highs", "Equal highs present (liquidity pool)"),
            ("struct_equal_lows", "Equal lows present (liquidity pool)"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_liquidity_section(self):
        """Create Liquidity Analysis section"""
        group = QGroupBox("5️⃣ Liquidity Analysis")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("liq_buyside_swept", "Buy-side liquidity already swept"),
            ("liq_sellside_swept", "Sell-side liquidity already swept"),
            ("liq_buyside_remaining", "Buy-side liquidity remains above (unswept)"),
            ("liq_sellside_remaining", "Sell-side liquidity remains below (unswept)"),
            ("liq_internal_liquidity", "Internal range liquidity available"),
            ("liq_external_liquidity", "External range liquidity draw"),
            ("liq_old_highs", "Old highs acting as liquidity magnet"),
            ("liq_old_lows", "Old lows acting as liquidity magnet"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_premium_discount_section(self):
        """Create Premium/Discount section"""
        group = QGroupBox("6️⃣ Premium/Discount & Fair Value Gaps")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #60a5fa; }")
        layout = QVBoxLayout()
        
        checks = [
            ("pd_in_discount", "Price is in discount zone (below 50% of range)"),
            ("pd_in_premium", "Price is in premium zone (above 50% of range)"),
            ("pd_fvg_below", "Bullish FVG below current price (support)"),
            ("pd_fvg_above", "Bearish FVG above current price (resistance)"),
            ("pd_ob_below", "Bullish Order Block below"),
            ("pd_ob_above", "Bearish Order Block above"),
            ("pd_at_equilibrium", "Price at equilibrium (50%)"),
            ("pd_imbalance_filled", "Previous imbalances have been filled"),
        ]
        
        for key, text in checks:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-weight: normal; color: #e2e8f0; padding: 5px;")
            self.checkboxes[key] = cb
            layout.addWidget(cb)
        
        group.setLayout(layout)
        return group
    
    def create_result_section(self):
        """Create result display section"""
        layout = QVBoxLayout()
        
        # Result label
        self.result_label = QLabel("Complete the checklist and click 'Calculate Bias'")
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #94a3b8;
            padding: 15px;
            background-color: #334155;
            border-radius: 8px;
        """)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setMinimumHeight(60)
        layout.addWidget(self.result_label)
        
        # Analysis text
        self.analysis_text = QTextEdit()
        self.analysis_text.setMaximumHeight(120)
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setPlaceholderText("Detailed analysis will appear here...")
        self.analysis_text.setStyleSheet("""
            background-color: #1e293b;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 10px;
            color: #e2e8f0;
        """)
        layout.addWidget(self.analysis_text)
        
        return layout
    
    def calculate_bias(self):
        """Calculate the daily bias based on checked items"""
        bullish_score = 0
        bearish_score = 0
        neutral_score = 0
        
        # Higher Timeframe scoring
        if self.checkboxes["htf_weekly_trend"].isChecked():
            bullish_score += 3
        if self.checkboxes["htf_weekly_bearish"].isChecked():
            bearish_score += 3
        if self.checkboxes["htf_daily_aligned"].isChecked():
            # Adds to whichever direction is winning
            if bullish_score > bearish_score:
                bullish_score += 2
            elif bearish_score > bullish_score:
                bearish_score += 2
        if self.checkboxes["htf_weekly_high"].isChecked():
            bearish_score += 2  # In premium, expect retracement
        if self.checkboxes["htf_weekly_low"].isChecked():
            bullish_score += 2  # In discount, expect rally
        if self.checkboxes["htf_weekly_consolidation"].isChecked():
            neutral_score += 2
        
        # Previous Day scoring
        if self.checkboxes["prev_bullish_close"].isChecked():
            bullish_score += 2
        if self.checkboxes["prev_bearish_close"].isChecked():
            bearish_score += 2
        if self.checkboxes["prev_swept_highs"].isChecked():
            bearish_score += 1  # Often reverses after sweep
        if self.checkboxes["prev_swept_lows"].isChecked():
            bullish_score += 1  # Often reverses after sweep
        if self.checkboxes["prev_range_expansion"].isChecked():
            if bullish_score > bearish_score:
                bullish_score += 1
            elif bearish_score > bullish_score:
                bearish_score += 1
        
        # Current Day scoring
        if self.checkboxes["current_gap_up"].isChecked():
            bearish_score += 1  # Gap fills
        if self.checkboxes["current_gap_down"].isChecked():
            bullish_score += 1  # Gap fills
        if self.checkboxes["current_above_asian_high"].isChecked():
            bullish_score += 2
        if self.checkboxes["current_below_asian_low"].isChecked():
            bearish_score += 2
        if self.checkboxes["current_london_displacement"].isChecked():
            if bullish_score > bearish_score:
                bullish_score += 2
            elif bearish_score > bullish_score:
                bearish_score += 2
        
        # Market Structure scoring
        if self.checkboxes["struct_bos_bullish"].isChecked():
            bullish_score += 3
        if self.checkboxes["struct_bos_bearish"].isChecked():
            bearish_score += 3
        if self.checkboxes["struct_mss_bullish"].isChecked():
            bullish_score += 3
        if self.checkboxes["struct_mss_bearish"].isChecked():
            bearish_score += 3
        if self.checkboxes["struct_hh_hl"].isChecked():
            bullish_score += 2
        if self.checkboxes["struct_lh_ll"].isChecked():
            bearish_score += 2
        
        # Liquidity scoring
        if self.checkboxes["liq_buyside_remaining"].isChecked():
            bullish_score += 2  # Draw to liquidity
        if self.checkboxes["liq_sellside_remaining"].isChecked():
            bearish_score += 2  # Draw to liquidity
        if self.checkboxes["liq_buyside_swept"].isChecked():
            bearish_score += 1  # Often reverses
        if self.checkboxes["liq_sellside_swept"].isChecked():
            bullish_score += 1  # Often reverses
        
        # Premium/Discount scoring
        if self.checkboxes["pd_in_discount"].isChecked():
            bullish_score += 2
        if self.checkboxes["pd_in_premium"].isChecked():
            bearish_score += 2
        if self.checkboxes["pd_fvg_below"].isChecked():
            bullish_score += 1
        if self.checkboxes["pd_fvg_above"].isChecked():
            bearish_score += 1
        if self.checkboxes["pd_ob_below"].isChecked():
            bullish_score += 1
        if self.checkboxes["pd_ob_above"].isChecked():
            bearish_score += 1
        
        # Determine bias
        total_checks = bullish_score + bearish_score + neutral_score
        
        if total_checks == 0:
            self.result_label.setText("⚠️ Please complete the checklist")
            self.result_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #f59e0b;
                padding: 15px;
                background-color: #334155;
                border-radius: 8px;
            """)
            self.analysis_text.clear()
            return
        
        # Calculate percentages
        total_directional = bullish_score + bearish_score
        if total_directional > 0:
            bullish_pct = (bullish_score / total_directional) * 100
            bearish_pct = (bearish_score / total_directional) * 100
        else:
            bullish_pct = 0
            bearish_pct = 0
        
        # Determine final bias
        difference = abs(bullish_score - bearish_score)
        
        if difference <= 2:
            bias = "NEUTRAL"
            color = "#f59e0b"
            confidence = "Low Conviction"
        elif bullish_score > bearish_score:
            if difference >= 5:
                bias = "STRONG BULLISH"
                color = "#10b981"
                confidence = "High Conviction"
            else:
                bias = "BULLISH"
                color = "#10b981"
                confidence = "Moderate Conviction"
        else:
            if difference >= 5:
                bias = "STRONG BEARISH"
                color = "#dc2626"
                confidence = "High Conviction"
            else:
                bias = "BEARISH"
                color = "#dc2626"
                confidence = "Moderate Conviction"
        
        # Update result label
        self.result_label.setText(f"📊 Daily Bias: {bias} ({confidence})")
        self.result_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
            padding: 15px;
            background-color: #334155;
            border-radius: 8px;
        """)
        
        # Create detailed analysis
        analysis = f"BIAS ANALYSIS:\n\n"
        analysis += f"Bullish Score: {bullish_score} ({bullish_pct:.1f}%)\n"
        analysis += f"Bearish Score: {bearish_score} ({bearish_pct:.1f}%)\n"
        analysis += f"Conviction: {confidence}\n\n"
        
        analysis += "KEY FACTORS:\n"
        if bullish_score > bearish_score:
            analysis += "• Market showing bullish characteristics\n"
            if self.checkboxes["pd_in_discount"].isChecked():
                analysis += "• Price in discount - favorable for longs\n"
            if self.checkboxes["struct_bos_bullish"].isChecked() or self.checkboxes["struct_mss_bullish"].isChecked():
                analysis += "• Bullish structure confirmed\n"
            if self.checkboxes["liq_buyside_remaining"].isChecked():
                analysis += "• Buy-side liquidity draw present\n"
        elif bearish_score > bullish_score:
            analysis += "• Market showing bearish characteristics\n"
            if self.checkboxes["pd_in_premium"].isChecked():
                analysis += "• Price in premium - favorable for shorts\n"
            if self.checkboxes["struct_bos_bearish"].isChecked() or self.checkboxes["struct_mss_bearish"].isChecked():
                analysis += "• Bearish structure confirmed\n"
            if self.checkboxes["liq_sellside_remaining"].isChecked():
                analysis += "• Sell-side liquidity draw present\n"
        else:
            analysis += "• Mixed signals - trade with caution\n"
            analysis += "• Wait for clearer directional bias\n"
        
        self.analysis_text.setText(analysis)
    
    def reset_form(self):
        """Reset all checkboxes"""
        for cb in self.checkboxes.values():
            cb.setChecked(False)
        
        self.result_label.setText("Complete the checklist and click 'Calculate Bias'")
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #94a3b8;
            padding: 15px;
            background-color: #334155;
            border-radius: 8px;
        """)
        self.analysis_text.clear()
