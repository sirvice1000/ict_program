"""
Database Manager - Handles all SQLite operations
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "trading_data.db"):
        self.db_path = db_path
        self.conn = None
        
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def initialize_database(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Concepts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                date_added TEXT NOT NULL,
                summary TEXT,
                definition TEXT,
                how_to_identify TEXT,
                trading_rules TEXT,
                examples TEXT,
                personal_notes TEXT
            )
        """)
        
        # Key points table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id INTEGER NOT NULL,
                point TEXT NOT NULL,
                FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
            )
        """)
        
        # Related concepts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS related_concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id INTEGER NOT NULL,
                related_name TEXT NOT NULL,
                FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
            )
        """)
        
        # Resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id INTEGER NOT NULL,
                resource TEXT NOT NULL,
                FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
            )
        """)
        
        # Trades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                pair TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                exit_price REAL,
                quantity REAL,
                pnl REAL,
                pnl_percent REAL,
                outcome TEXT,
                setup_type TEXT,
                notes TEXT,
                screenshot_path TEXT,
                date_closed TEXT
            )
        """)
        
        # Trade concepts junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER NOT NULL,
                concept_name TEXT NOT NULL,
                FOREIGN KEY (trade_id) REFERENCES trades(id) ON DELETE CASCADE
            )
        """)
        
        # Market data table (NEW)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                daily_high REAL,
                daily_low REAL,
                UNIQUE(date, symbol)
            )
        """)
        
        # Concept notes table (NEW)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concept_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id TEXT NOT NULL UNIQUE,
                notes TEXT,
                last_updated TEXT
            )
        """)
        
        conn.commit()
        
    # ==================== CONCEPT OPERATIONS ====================
    
    def add_concept(self, title: str, category: str, summary: str = "",
                   definition: str = "", how_to_identify: str = "",
                   trading_rules: str = "", examples: str = "",
                   personal_notes: str = "", key_points: List[str] = None,
                   related_concepts: List[str] = None,
                   resources: List[str] = None) -> int:
        """Add a new concept and return its ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        date_added = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT INTO concepts (title, category, date_added, summary, definition,
                                how_to_identify, trading_rules, examples, personal_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, category, date_added, summary, definition, how_to_identify,
              trading_rules, examples, personal_notes))
        
        concept_id = cursor.lastrowid
        
        # Add key points
        if key_points:
            for point in key_points:
                if point.strip():
                    cursor.execute("INSERT INTO key_points (concept_id, point) VALUES (?, ?)",
                                 (concept_id, point.strip()))
        
        # Add related concepts
        if related_concepts:
            for related in related_concepts:
                if related.strip():
                    cursor.execute("INSERT INTO related_concepts (concept_id, related_name) VALUES (?, ?)",
                                 (concept_id, related.strip()))
        
        # Add resources
        if resources:
            for resource in resources:
                if resource.strip():
                    cursor.execute("INSERT INTO resources (concept_id, resource) VALUES (?, ?)",
                                 (concept_id, resource.strip()))
        
        conn.commit()
        return concept_id
    
    def get_all_concepts(self) -> List[Dict]:
        """Get all concepts with their related data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM concepts ORDER BY date_added DESC")
        concepts = [dict(row) for row in cursor.fetchall()]
        
        for concept in concepts:
            concept_id = concept['id']
            
            cursor.execute("SELECT point FROM key_points WHERE concept_id = ?", (concept_id,))
            concept['key_points'] = [row['point'] for row in cursor.fetchall()]
            
            cursor.execute("SELECT related_name FROM related_concepts WHERE concept_id = ?", (concept_id,))
            concept['related_concepts'] = [row['related_name'] for row in cursor.fetchall()]
            
            cursor.execute("SELECT resource FROM resources WHERE concept_id = ?", (concept_id,))
            concept['resources'] = [row['resource'] for row in cursor.fetchall()]
        
        return concepts
    
    def get_concept_by_id(self, concept_id: int) -> Optional[Dict]:
        """Get a single concept with all related data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM concepts WHERE id = ?", (concept_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        concept = dict(row)
        
        cursor.execute("SELECT point FROM key_points WHERE concept_id = ?", (concept_id,))
        concept['key_points'] = [row['point'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT related_name FROM related_concepts WHERE concept_id = ?", (concept_id,))
        concept['related_concepts'] = [row['related_name'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT resource FROM resources WHERE concept_id = ?", (concept_id,))
        concept['resources'] = [row['resource'] for row in cursor.fetchall()]
        
        return concept
    
    def update_concept(self, concept_id: int, **kwargs):
        """Update a concept and its related data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        key_points = kwargs.pop('key_points', None)
        related_concepts = kwargs.pop('related_concepts', None)
        resources = kwargs.pop('resources', None)
        
        if kwargs:
            fields = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            values = list(kwargs.values()) + [concept_id]
            cursor.execute(f"UPDATE concepts SET {fields} WHERE id = ?", values)
        
        if key_points is not None:
            cursor.execute("DELETE FROM key_points WHERE concept_id = ?", (concept_id,))
            for point in key_points:
                if point.strip():
                    cursor.execute("INSERT INTO key_points (concept_id, point) VALUES (?, ?)",
                                 (concept_id, point.strip()))
        
        if related_concepts is not None:
            cursor.execute("DELETE FROM related_concepts WHERE concept_id = ?", (concept_id,))
            for related in related_concepts:
                if related.strip():
                    cursor.execute("INSERT INTO related_concepts (concept_id, related_name) VALUES (?, ?)",
                                 (concept_id, related.strip()))
        
        if resources is not None:
            cursor.execute("DELETE FROM resources WHERE concept_id = ?", (concept_id,))
            for resource in resources:
                if resource.strip():
                    cursor.execute("INSERT INTO resources (concept_id, resource) VALUES (?, ?)",
                                 (concept_id, resource.strip()))
        
        conn.commit()
    
    def delete_concept(self, concept_id: int):
        """Delete a concept and all related data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM concepts WHERE id = ?", (concept_id,))
        conn.commit()
    
    def search_concepts(self, query: str) -> List[Dict]:
        """Search concepts by title, category, or summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM concepts 
            WHERE title LIKE ? OR category LIKE ? OR summary LIKE ?
            ORDER BY date_added DESC
        """, (search_pattern, search_pattern, search_pattern))
        
        concepts = [dict(row) for row in cursor.fetchall()]
        
        for concept in concepts:
            concept_id = concept['id']
            
            cursor.execute("SELECT point FROM key_points WHERE concept_id = ?", (concept_id,))
            concept['key_points'] = [row['point'] for row in cursor.fetchall()]
            
            cursor.execute("SELECT related_name FROM related_concepts WHERE concept_id = ?", (concept_id,))
            concept['related_concepts'] = [row['related_name'] for row in cursor.fetchall()]
            
            cursor.execute("SELECT resource FROM resources WHERE concept_id = ?", (concept_id,))
            concept['resources'] = [row['resource'] for row in cursor.fetchall()]
        
        return concepts
    
    def get_concepts_by_category(self, category: str) -> List[Dict]:
        """Get all concepts in a specific category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM concepts WHERE category = ? ORDER BY date_added DESC", (category,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM concepts ORDER BY category")
        return [row['category'] for row in cursor.fetchall()]
    
    # ==================== TRADE OPERATIONS ====================
    
    def add_trade(self, date: str, pair: str, timeframe: str, direction: str,
                 entry_price: float = None, stop_loss: float = None,
                 take_profit: float = None, exit_price: float = None,
                 quantity: float = None, outcome: str = "pending",
                 setup_type: str = "", notes: str = "",
                 screenshot_path: str = "", concepts_used: List[str] = None) -> int:
        """Add a new trade and return its ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        pnl = None
        pnl_percent = None
        if exit_price and entry_price and quantity:
            if direction.lower() == 'long':
                pnl = (exit_price - entry_price) * quantity
            else:
                pnl = (entry_price - exit_price) * quantity
            pnl_percent = (pnl / (entry_price * quantity)) * 100 if entry_price else 0
        
        date_closed = datetime.now().strftime("%Y-%m-%d") if outcome != "pending" else None
        
        cursor.execute("""
            INSERT INTO trades (date, pair, timeframe, direction, entry_price, stop_loss,
                              take_profit, exit_price, quantity, pnl, pnl_percent, outcome,
                              setup_type, notes, screenshot_path, date_closed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, pair, timeframe, direction, entry_price, stop_loss, take_profit,
              exit_price, quantity, pnl, pnl_percent, outcome, setup_type, notes,
              screenshot_path, date_closed))
        
        trade_id = cursor.lastrowid
        
        if concepts_used:
            for concept in concepts_used:
                if concept.strip():
                    cursor.execute("INSERT INTO trade_concepts (trade_id, concept_name) VALUES (?, ?)",
                                 (trade_id, concept.strip()))
        
        conn.commit()
        return trade_id
    
    def get_all_trades(self) -> List[Dict]:
        """Get all trades with concepts used"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM trades ORDER BY date DESC")
        trades = [dict(row) for row in cursor.fetchall()]
        
        for trade in trades:
            trade_id = trade['id']
            cursor.execute("SELECT concept_name FROM trade_concepts WHERE trade_id = ?", (trade_id,))
            trade['concepts_used'] = [row['concept_name'] for row in cursor.fetchall()]
        
        return trades
    
    def get_trade_by_id(self, trade_id: int) -> Optional[Dict]:
        """Get a single trade with all data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        trade = dict(row)
        
        cursor.execute("SELECT concept_name FROM trade_concepts WHERE trade_id = ?", (trade_id,))
        trade['concepts_used'] = [row['concept_name'] for row in cursor.fetchall()]
        
        return trade
    
    def update_trade(self, trade_id: int, **kwargs):
        """Update a trade"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        concepts_used = kwargs.pop('concepts_used', None)
        
        if 'exit_price' in kwargs or 'entry_price' in kwargs or 'quantity' in kwargs:
            trade = self.get_trade_by_id(trade_id)
            entry = kwargs.get('entry_price', trade['entry_price'])
            exit_p = kwargs.get('exit_price', trade['exit_price'])
            qty = kwargs.get('quantity', trade['quantity'])
            direction = kwargs.get('direction', trade['direction'])
            
            if exit_p and entry and qty:
                if direction.lower() == 'long':
                    pnl = (exit_p - entry) * qty
                else:
                    pnl = (entry - exit_p) * qty
                kwargs['pnl'] = pnl
                kwargs['pnl_percent'] = (pnl / (entry * qty)) * 100 if entry else 0
        
        if 'outcome' in kwargs and kwargs['outcome'] != 'pending':
            if not kwargs.get('date_closed'):
                kwargs['date_closed'] = datetime.now().strftime("%Y-%m-%d")
        
        if kwargs:
            fields = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            values = list(kwargs.values()) + [trade_id]
            cursor.execute(f"UPDATE trades SET {fields} WHERE id = ?", values)
        
        if concepts_used is not None:
            cursor.execute("DELETE FROM trade_concepts WHERE trade_id = ?", (trade_id,))
            for concept in concepts_used:
                if concept.strip():
                    cursor.execute("INSERT INTO trade_concepts (trade_id, concept_name) VALUES (?, ?)",
                                 (trade_id, concept.strip()))
        
        conn.commit()
    
    def delete_trade(self, trade_id: int):
        """Delete a trade"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
        conn.commit()
    
    def get_trade_statistics(self) -> Dict:
        """Calculate trade statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM trades")
        stats['total_trades'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM trades WHERE outcome = 'win'")
        stats['wins'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM trades WHERE outcome = 'loss'")
        stats['losses'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM trades WHERE outcome = 'pending'")
        stats['pending'] = cursor.fetchone()['count']
        
        closed_trades = stats['wins'] + stats['losses']
        stats['win_rate'] = (stats['wins'] / closed_trades * 100) if closed_trades > 0 else 0
        
        cursor.execute("SELECT SUM(pnl) as total FROM trades WHERE pnl IS NOT NULL")
        result = cursor.fetchone()
        stats['total_pnl'] = result['total'] if result['total'] else 0
        
        cursor.execute("SELECT AVG(pnl) as avg FROM trades WHERE pnl IS NOT NULL")
        result = cursor.fetchone()
        stats['avg_pnl'] = result['avg'] if result['avg'] else 0
        
        cursor.execute("SELECT MAX(pnl) as max FROM trades WHERE pnl IS NOT NULL")
        result = cursor.fetchone()
        stats['best_trade'] = result['max'] if result['max'] else 0
        
        cursor.execute("SELECT MIN(pnl) as min FROM trades WHERE pnl IS NOT NULL")
        result = cursor.fetchone()
        stats['worst_trade'] = result['min'] if result['min'] else 0
        
        return stats
    
    # ==================== MARKET DATA OPERATIONS (NEW) ====================
    
    def save_market_data(self, date: str, symbol: str, daily_high: float = None, daily_low: float = None):
        """Save or update market data for a symbol on a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO market_data (date, symbol, daily_high, daily_low)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date, symbol) DO UPDATE SET
                daily_high = excluded.daily_high,
                daily_low = excluded.daily_low
        """, (date, symbol, daily_high, daily_low))
        
        conn.commit()
    
    def get_market_data(self, date: str, symbol: str) -> Optional[Dict]:
        """Get market data for a symbol on a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM market_data WHERE date = ? AND symbol = ?
        """, (date, symbol))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_market_data_range(self, symbol: str, start_date: str, end_date: str) -> List[Dict]:
        """Get market data for a symbol over a date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM market_data 
            WHERE symbol = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        """, (symbol, start_date, end_date))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== CONCEPT NOTES OPERATIONS (NEW) ====================
    
    def save_concept_notes(self, concept_id: str, notes: str):
        """Save or update personal notes for a concept"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO concept_notes (concept_id, notes, last_updated)
            VALUES (?, ?, ?)
            ON CONFLICT(concept_id) DO UPDATE SET
                notes = excluded.notes,
                last_updated = excluded.last_updated
        """, (concept_id, notes, last_updated))
        
        conn.commit()
    
    def get_concept_notes(self, concept_id: str) -> Optional[str]:
        """Get personal notes for a concept"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT notes FROM concept_notes WHERE concept_id = ?
        """, (concept_id,))
        
        row = cursor.fetchone()
        return row['notes'] if row else None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None