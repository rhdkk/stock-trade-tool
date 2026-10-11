"""
Stock Analysis Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import pandas as pd

from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from fundamental_analyzer import FundamentalAnalyzer
from gui.chart_widget import ChartWidget
from utils import format_price, format_percent, get_signal_color

class AnalysisWindow(QMainWindow):
    """Stock analysis window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Analysis - Swing Trading")
        self.setGeometry(100, 100, 1400, 900)
        
        self.fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.signal_gen = SignalGenerator()
        self.fund_analyzer = FundamentalAnalyzer()
        
        self.current_df = None
        self.current_ticker = None
        
        self.initUI()
        self.apply_stylesheet()
    
    def initUI(self):
        """Initialize UI"""
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        
        # ===== SEARCH BAR =====
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Stock Ticker:")
        search_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("e.g., AAPL, BBCA.JK")
        self.ticker_input.setMaximumWidth(150)
        
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.analyze_stock)
        analyze_btn.setMaximumWidth(100)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setMaximumWidth(100)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.ticker_input)
        search_layout.addWidget(analyze_btn)
        search_layout.addWidget(refresh_btn)
        search_layout.addStretch()
        
        main_layout.addLayout(search_layout)
        
        # ===== TABS =====
        tabs = QTabWidget()
        
        # Chart Tab
        self.chart_widget = ChartWidget()
        tabs.addTab(self.chart_widget, "Price Chart")
        
        # Analysis Tab
        analysis_tab = self.create_analysis_tab()
        tabs.addTab(analysis_tab, "Analysis")
        
        # Indicators Tab
        indicators_tab = self.create_indicators_tab()
        tabs.addTab(indicators_tab, "Indicators")
        
        # Fundamentals Tab
        fundamentals_tab = self.create_fundamentals_tab()
        tabs.addTab(fundamentals_tab, "Fundamentals")
        
        main_layout.addWidget(tabs)
        
        main_widget.setLayout(main_layout)
    
    def create_analysis_tab(self):
        """Create analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Signal Display
        signal_layout = QHBoxLayout()
        
        signal_label = QLabel("Signal:")
        signal_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.signal_display = QLabel("---")
        self.signal_display.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.signal_display.setMinimumHeight(40)
        
        confidence_label = QLabel("Confidence:")
        self.confidence_display = QLabel("---%")
        self.confidence_display.setFont(QFont("Arial", 12))
        
        signal_layout.addWidget(signal_label)
        signal_layout.addWidget(self.signal_display)
        signal_layout.addSpacing(50)
        signal_layout.addWidget(confidence_label)
        signal_layout.addWidget(self.confidence_display)
        signal_layout.addStretch()
        
        layout.addLayout(signal_layout)
        
        # Analysis Details
        details_label = QLabel("Analysis Details:")
        details_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(details_label)
        
        self.analysis_table = QTableWidget()
        self.analysis_table.setColumnCount(2)
        self.analysis_table.setHorizontalHeaderLabels(["Indicator", "Status"])
        self.analysis_table.setMaximumHeight(300)
        
        layout.addWidget(self.analysis_table)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_indicators_tab(self):
        """Create indicators tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.indicators_table = QTableWidget()
        self.indicators_table.setColumnCount(2)
        self.indicators_table.setHorizontalHeaderLabels(["Indicator", "Value"])
        
        layout.addWidget(self.indicators_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_fundamentals_tab(self):
        """Create fundamentals tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.fundamentals_table = QTableWidget()
        self.fundamentals_table.setColumnCount(2)
        self.fundamentals_table.setHorizontalHeaderLabels(["Metric", "Value"])
        
        layout.addWidget(self.fundamentals_table)
        
        widget.setLayout(layout)
        return widget
    
    def analyze_stock(self):
        """Analyze stock"""
        ticker = self.ticker_input.text().strip().upper()
        
        if not ticker:
            self.signal_display.setText("ERROR: Enter ticker")
            return
        
        # Fetch data
        self.current_df = self.fetcher.fetch_stock_data(ticker, period='3mo', interval='1d')
        
        if self.current_df is None or self.current_df.empty:
            self.signal_display.setText("ERROR: Data not found")
            return
        
        self.current_ticker = ticker
        
        # Add indicators
        self.current_df = self.analyzer.add_all_indicators(self.current_df)
        
        # Update chart
        self.chart_widget.plot_data(self.current_df)
        
        # Update analysis
        self.update_analysis()
        self.update_indicators()
        self.update_fundamentals()
    
    def update_analysis(self):
        """Update analysis display"""
        if self.current_df is None:
            return
        
        # Generate signal
        signal, confidence, details = self.signal_gen.analyze_signals(self.current_df)
        
        # Update signal display
        self.signal_display.setText(signal)
        self.signal_display.setStyleSheet(
            f"background-color: {get_signal_color(signal)}; "
            f"padding: 10px; border-radius: 5px; color: white;"
        )
        
        self.confidence_display.setText(f"{confidence:.1f}%")
        
        # Update analysis table
        self.analysis_table.setRowCount(len(details))
        
        for row, (indicator, status) in enumerate(details.items()):
            item1 = QTableWidgetItem(indicator)
            item2 = QTableWidgetItem(status)
            
            self.analysis_table.setItem(row, 0, item1)
            self.analysis_table.setItem(row, 1, item2)
    
    def update_indicators(self):
        """Update indicators display"""
        if self.current_df is None:
            return
        
        latest = self.current_df.iloc[-1]
        
        indicators = [
            ('Close Price', format_price(latest['close'])),
            ('EMA 9', format_price(latest['ema_9'])),
            ('EMA 21', format_price(latest['ema_21'])),
            ('EMA 55', format_price(latest['ema_55'])),
            ('RSI (14)', f"{latest['rsi']:.2f}"),
            ('MACD', f"{latest['macd']:.6f}"),
            ('MACD Signal', f"{latest['macd_signal']:.6f}"),
            ('MACD Histogram', f"{latest['macd_histogram']:.6f}"),
            ('Stoch %K', f"{latest['stoch_k']:.2f}"),
            ('Stoch %D', f"{latest['stoch_d']:.2f}"),
            ('BB Upper', format_price(latest['bb_upper'])),
            ('BB Middle', format_price(latest['bb_middle'])),
            ('BB Lower', format_price(latest['bb_lower'])),
            ('BB %B', f"{latest['bb_percent_b']:.2f}"),
        ]
        
        self.indicators_table.setRowCount(len(indicators))
        
        for row, (name, value) in enumerate(indicators):
            item1 = QTableWidgetItem(name)
            item2 = QTableWidgetItem(value)
            
            self.indicators_table.setItem(row, 0, item1)
            self.indicators_table.setItem(row, 1, item2)
    
    def update_fundamentals(self):
        """Update fundamentals display"""
        if not self.current_ticker:
            return
        
        fund_data = self.fund_analyzer.get_fundamental_overview(self.current_ticker)
        
        if not fund_data:
            return
        
        fundamentals = [
            ('Company', fund_data.get('name', 'N/A')),
            ('Sector', fund_data.get('sector', 'N/A')),
            ('Industry', fund_data.get('industry', 'N/A')),
            ('P/E Ratio', f"{fund_data.get('pe_ratio', 'N/A')}"),
            ('EPS', format_price(fund_data.get('eps', 0))),
            ('52W High', format_price(fund_data.get('52_week_high', 0))),
            ('52W Low', format_price(fund_data.get('52_week_low', 0))),
        ]
        
        self.fundamentals_table.setRowCount(len(fundamentals))
        
        for row, (name, value) in enumerate(fundamentals):
            item1 = QTableWidgetItem(name)
            item2 = QTableWidgetItem(str(value))
            
            self.fundamentals_table.setItem(row, 0, item1)
            self.fundamentals_table.setItem(row, 1, item2)
    
    def refresh_data(self):
        """Refresh current stock data"""
        if self.current_ticker:
            self.ticker_input.setText(self.current_ticker)
            self.analyze_stock()
    
    def apply_stylesheet(self):
        """Apply stylesheet"""
        from gui.styles import get_stylesheet
        self.setStyleSheet(get_stylesheet('dark'))