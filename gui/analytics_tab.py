"""
Analytics Tab - Trading performance metrics and statistics
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QGroupBox, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database.db_manager import DatabaseManager

class AnalyticsTab(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        """Initialize the analytics interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📈 Trading Performance Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b82f6; padding: 10px;")
        layout.addWidget(title)
        
        # Overview Stats
        overview_group = QGroupBox("Overview Statistics")
        overview_layout = QGridLayout()
        
        self.total_trades_label = self.create_stat_label("0", "Total Trades")
        self.wins_label = self.create_stat_label("0", "Wins", "#10b981")
        self.losses_label = self.create_stat_label("0", "Losses", "#dc2626")
        self.pending_label = self.create_stat_label("0", "Pending", "#f59e0b")
        self.win_rate_label = self.create_stat_label("0%", "Win Rate", "#3b82f6")
        
        overview_layout.addWidget(self.total_trades_label, 0, 0)
        overview_layout.addWidget(self.wins_label, 0, 1)
        overview_layout.addWidget(self.losses_label, 0, 2)
        overview_layout.addWidget(self.pending_label, 0, 3)
        overview_layout.addWidget(self.win_rate_label, 0, 4)
        
        overview_group.setLayout(overview_layout)
        layout.addWidget(overview_group)
        
        # P&L Stats
        pnl_group = QGroupBox("Profit & Loss")
        pnl_layout = QGridLayout()
        
        self.total_pnl_label = self.create_stat_label("$0.00", "Total P&L")
        self.avg_pnl_label = self.create_stat_label("$0.00", "Avg P&L per Trade")
        self.best_trade_label = self.create_stat_label("$0.00", "Best Trade", "#10b981")
        self.worst_trade_label = self.create_stat_label("$0.00", "Worst Trade", "#dc2626")
        
        pnl_layout.addWidget(self.total_pnl_label, 0, 0)
        pnl_layout.addWidget(self.avg_pnl_label, 0, 1)
        pnl_layout.addWidget(self.best_trade_label, 0, 2)
        pnl_layout.addWidget(self.worst_trade_label, 0, 3)
        
        pnl_group.setLayout(pnl_layout)
        layout.addWidget(pnl_group)
        
        # Knowledge Base Stats
        kb_group = QGroupBox("Knowledge Base")
        kb_layout = QHBoxLayout()
        
        self.total_concepts_label = self.create_stat_label("0", "Total Concepts", "#8b5cf6")
        self.categories_label = self.create_stat_label("0", "Categories", "#8b5cf6")
        
        kb_layout.addWidget(self.total_concepts_label)
        kb_layout.addWidget(self.categories_label)
        kb_layout.addStretch()
        
        kb_group.setLayout(kb_layout)
        layout.addWidget(kb_group)
        
        # Additional insights
        insights_group = QGroupBox("Trading Insights")
        insights_layout = QVBoxLayout()
        
        self.insights_label = QLabel("Loading insights...")
        self.insights_label.setWordWrap(True)
        self.insights_label.setStyleSheet("padding: 15px; line-height: 1.6;")
        insights_layout.addWidget(self.insights_label)
        
        insights_group.setLayout(insights_layout)
        layout.addWidget(insights_group)
        
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
    def create_stat_label(self, value: str, description: str, color: str = "#e2e8f0"):
        """Create a styled stat label"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: #334155;
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(5)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: bold;
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 13px;
            color: #94a3b8;
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(desc_label)
        
        # Store label references for updating
        container.value_label = value_label
        container.desc_label = desc_label
        
        return container
    
    def refresh_data(self):
        """Refresh all analytics data"""
        # Get trade statistics
        stats = self.db.get_trade_statistics()
        
        # Update overview
        self.total_trades_label.value_label.setText(str(stats['total_trades']))
        self.wins_label.value_label.setText(str(stats['wins']))
        self.losses_label.value_label.setText(str(stats['losses']))
        self.pending_label.value_label.setText(str(stats['pending']))
        self.win_rate_label.value_label.setText(f"{stats['win_rate']:.1f}%")
        
        # Update P&L
        total_pnl = stats['total_pnl']
        pnl_color = "#10b981" if total_pnl >= 0 else "#dc2626"
        self.total_pnl_label.value_label.setText(f"${total_pnl:.2f}")
        self.total_pnl_label.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: bold;
            color: {pnl_color};
        """)
        
        avg_pnl = stats['avg_pnl']
        avg_color = "#10b981" if avg_pnl >= 0 else "#dc2626"
        self.avg_pnl_label.value_label.setText(f"${avg_pnl:.2f}")
        self.avg_pnl_label.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: bold;
            color: {avg_color};
        """)
        
        self.best_trade_label.value_label.setText(f"${stats['best_trade']:.2f}")
        self.worst_trade_label.value_label.setText(f"${stats['worst_trade']:.2f}")
        
        # Knowledge base stats
        concepts = self.db.get_all_concepts()
        categories = self.db.get_all_categories()
        
        self.total_concepts_label.value_label.setText(str(len(concepts)))
        self.categories_label.value_label.setText(str(len(categories)))
        
        # Generate insights
        insights = self.generate_insights(stats, len(concepts))
        self.insights_label.setText(insights)
    
    def generate_insights(self, stats: dict, concept_count: int) -> str:
        """Generate trading insights from statistics"""
        insights = []
        
        # Performance insights
        if stats['total_trades'] == 0:
            insights.append("📝 <b>Get Started:</b> You haven't logged any trades yet. Start documenting your trades to track your performance!")
        else:
            insights.append(f"📊 <b>Trade Activity:</b> You've recorded {stats['total_trades']} trades with a win rate of {stats['win_rate']:.1f}%.")
            
            if stats['win_rate'] >= 60:
                insights.append("🎯 <b>Excellent!</b> Your win rate is above 60%, which is considered very strong in trading.")
            elif stats['win_rate'] >= 50:
                insights.append("✅ <b>Good Job:</b> Your win rate is profitable. Focus on maintaining consistency and improving your average winner size.")
            elif stats['win_rate'] >= 40 and stats['total_trades'] >= 20:
                insights.append("⚠️ <b>Below Average:</b> Your win rate is below 50%. Review your losing trades to identify patterns and areas for improvement.")
            
            # P&L insights
            if stats['total_pnl'] > 0:
                insights.append(f"💰 <b>Profitability:</b> You're up ${stats['total_pnl']:.2f} overall. Keep doing what's working!")
            elif stats['total_pnl'] < 0:
                insights.append(f"📉 <b>Drawdown:</b> Currently down ${abs(stats['total_pnl']):.2f}. Review your strategy and risk management.")
            
            # Average trade
            if stats['avg_pnl'] > 0:
                insights.append(f"📈 <b>Positive Expectancy:</b> Your average trade makes ${stats['avg_pnl']:.2f}. This is a good sign of a profitable strategy.")
            
            # Risk management
            if stats['best_trade'] > 0 and stats['worst_trade'] < 0:
                ratio = abs(stats['best_trade'] / stats['worst_trade']) if stats['worst_trade'] != 0 else 0
                if ratio >= 2:
                    insights.append(f"🎯 <b>Risk/Reward:</b> Your best trade (${stats['best_trade']:.2f}) is {ratio:.1f}x larger than your worst trade. Excellent risk management!")
                elif ratio >= 1:
                    insights.append(f"⚖️ <b>Risk/Reward:</b> Your winners and losers are fairly balanced. Consider aiming for larger winners relative to your losers.")
        
        # Knowledge base insights
        if concept_count == 0:
            insights.append("📚 <b>Knowledge Base:</b> Start building your knowledge base by adding ICT concepts you're learning!")
        elif concept_count < 5:
            insights.append(f"📚 <b>Learning Progress:</b> You've documented {concept_count} concepts. Keep adding more to build a comprehensive reference!")
        else:
            insights.append(f"📚 <b>Strong Foundation:</b> You have {concept_count} concepts in your knowledge base. Great work building your education!")
        
        # Sample size warning
        if 0 < stats['total_trades'] < 20:
            insights.append("⚠️ <b>Sample Size:</b> You need at least 20-30 trades to draw meaningful conclusions about your performance.")
        
        return "<br><br>".join(insights)