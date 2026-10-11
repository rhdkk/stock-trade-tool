"""
Market Screener Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtGui import QFont
from screener import StockScreener
from config import MARKETS


class ScreenerWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Market Screener")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()
    
    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        
        # Controls
        control_layout = QHBoxLayout()
        market_label = QLabel("Market:")
        market_font = QFont("Arial", 11)
        market_font.setBold(True)
        market_label.setFont(market_font)
        
        self.market_combo = QComboBox()
        self.market_combo.addItems(list(MARKETS.keys()))
        self.market_combo.setMaximumWidth(150)
        
        scan_btn = QPushButton("Scan Market")
        scan_btn.clicked.connect(self.scan_market)
        
        control_layout.addWidget(market_label)
        control_layout.addWidget(self.market_combo)
        control_layout.addWidget(scan_btn)
        control_layout.addStretch()
        main_layout.addLayout(control_layout)
        
        # Status
        self.status_label = QLabel("Ready to scan")
        main_layout.addWidget(self.status_label)
        
        # Results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Ticker", "Signal", "Confidence %", "Price", "RSI"])
        main_layout.addWidget(self.results_table)
        
        main_widget.setLayout(main_layout)
    
    def scan_market(self):
        market = self.market_combo.currentText()
        self.status_label.setText(f"Scanning {market}...")
        
        screener = StockScreener()
        results = screener.screen_market(market)
        
        if results is None or results.empty:
            self.status_label.setText("No opportunities found")
            self.results_table.setRowCount(0)
            return
        
        self.results_table.setRowCount(len(results))
        for row, (idx, row_data) in enumerate(results.iterrows()):
            self.results_table.setItem(row, 0, QTableWidgetItem(row_data['Ticker']))
            self.results_table.setItem(row, 1, QTableWidgetItem(row_data['Signal']))
            self.results_table.setItem(row, 2, QTableWidgetItem(f"{row_data['Confidence']:.1f}%"))
            self.results_table.setItem(row, 3, QTableWidgetItem(f"${row_data['Price']:.2f}"))
            self.results_table.setItem(row, 4, QTableWidgetItem(f"{row_data['RSI']:.0f}"))
        
        self.status_label.setText(f"Found {len(results)} opportunities!")