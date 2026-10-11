"""
SQLite database management for trade journal
"""
import sqlite3
import json
from datetime import datetime

class TradeDatabase:
    def __init__(self, db_file='database/db.sqlite3'):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Create tables if not exist"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Trades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                entry_price REAL NOT NULL,
                entry_date DATE NOT NULL,
                exit_price REAL,
                exit_date DATE,
                signal TEXT,
                confidence REAL,
                profit_loss REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_trade(self, ticker, entry_price, entry_date, signal, confidence):
        """Add new trade"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trades 
            (ticker, entry_price, entry_date, signal, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticker, entry_price, entry_date, signal, confidence))
        
        conn.commit()
        trade_id = cursor.lastrowid
        conn.close()
        
        return trade_id
    
    def close_trade(self, trade_id, exit_price, exit_date):
        """Close trade"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get entry price
        cursor.execute('SELECT entry_price FROM trades WHERE id = ?', (trade_id,))
        result = cursor.fetchone()
        
        if result:
            entry_price = result[0]
            profit_loss = exit_price - entry_price
            
            cursor.execute('''
                UPDATE trades
                SET exit_price = ?, exit_date = ?, profit_loss = ?
                WHERE id = ?
            ''', (exit_price, exit_date, profit_loss, trade_id))
            
            conn.commit()
        
        conn.close()
    
    def get_trades(self, limit=50):
        """Get all trades"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM trades ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        trades = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return trades
    
    def get_statistics(self):
        """Get trading statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT
                COUNT(*) as total_trades,
                SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as winning_trades,
                SUM(CASE WHEN profit_loss < 0 THEN 1 ELSE 0 END) as losing_trades,
                AVG(profit_loss) as avg_profit,
                SUM(profit_loss) as total_profit
            FROM trades WHERE profit_loss IS NOT NULL
        ''')
        
        result = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        stats = dict(zip(columns, result)) if result else {}
        
        conn.close()
        
        return stats