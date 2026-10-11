"""
Stock Screener Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import pandas as pd

from screener import StockScreener
from config import MARKETS
from utils import format_price, get_signal_color

class ScreenerWorker(QThread):
    """Worker thread for screener"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    
    def __init__(self, market):
        super().__init__()
        self.market = market
        self.screener = StockScreener()
    
    def run(self):
        """Run screener"""
        self.progress.emit(f"Screening {self.market}...")
        
        results = self.screener.screen_market(self.market)
        
        self.progress.emit("Screening completed!")
        self.finished.emit(results)

class ScreenerWindow(QMainWindow):
    """Stock screener window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Screener - Swing Trade Opportunities")
        self.setGeometry(100, 100, 1200, 700)
        
        self.initUI()
        self.apply_stylesheet()
    
    def initUI(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        
        # ===== CONTROLS =====
        control_layout = QHBoxLayout()
        
        market_label = QLabel("Market:")
        market_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.market_combo = QComboBox()
        self.market_combo.addItems(list(MARKETS.keys()))
        self.market_combo.setMaximumWidth(150)
        
        scan_btn = QPushButton("Scan Market")
        scan_btn.clicked.connect(self.scan_market)
        scan_btn.setMaximumWidth(150)
        
        control_layout.addWidget(market_label)
        control_layout.addWidget(self.market_combo)
        control_layout.addWidget(scan_btn)
        control_layout.addStretch()
        
        main_layout.addLayout(control_layout)
        
        # ===== PROGRESS =====
        self.progress_label = QLabel("Ready to scan")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(20)
        
        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_bar)
        
        # ===== RESULTS TABLE =====
        results_label = QLabel("Swing Trade Opportunities (RSI < 45):")
        results_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Ticker", "Signal", "Confidence %", "Price", "RSI", "Action"
        ])
        self.results_table.setColumnWidth(0, 100)
        self.results_table.setColumnWidth(1, 100)
        
        main_layout.addWidget(results_label)
        main_layout.addWidget(self.results_table)
        
        main_widget.setLayout(main_layout)
        
        # Worker
        self.worker = None
    
    def scan_market(self):
        """Scan market"""
        market = self.market_combo.currentText()
        
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(0)  # Indeterminate
        self.progress_label.setText(f"Scanning {market}...")
        
        self.worker = ScreenerWorker(market)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
    
    def on_progress(self, message):
        """Progress update"""
        self.progress_label.setText(message)
    
    def on_finished(self, results):
        """Screening finished"""
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        
        if results is None or results.empty:
            self.progress_label.setText("No swing trade opportunities found")
            self.results_table.setRowCount(0)
            return
        
        # Display results
        self.results_table.setRowCount(len(results))
        
        for row, (idx, row_data) in enumerate(results.iterrows()):
            # Ticker
            ticker_item = QTableWidgetItem(row_data['Ticker'])
            self.results_table.setItem(row, 0, ticker_item)
            
            # Signal
            signal_item = QTableWidgetItem(row_data['Signal'])
            signal_item.setBackground(QColor(get_signal_color(row_data['Signal'])))
            self.results_table.setItem(row, 1, signal_item)
            
            # Confidence
            conf_item = QTableWidgetItem(f"{row_data['Confidence']:.1f}%")
            self.results_table.setItem(row, 2, conf_item)
            
            # Price
            price_item = QTableWidgetItem(f"${row_data['Price']:.2f}")
            self.results_table.setItem(row, 3, price_item)
            
            # RSI
            rsi_item = QTableWidgetItem(f"{row_data['RSI']:.0f}")
            self.results_table.setItem(row, 4, rsi_item)
            
            # Action
            action_item = QTableWidgetItem("📊 View")
            self.results_table.setItem(row, 5, action_item)
        
        self.progress_label.setText(f"Found {len(results)} swing trade opportunities!")
    
    def apply_stylesheet(self):
        """Apply stylesheet"""
        from gui.styles import get_stylesheet
        self.setStyleSheet(get_stylesheet('dark'))