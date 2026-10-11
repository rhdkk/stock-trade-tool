"""
Stock Analysis Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget
)
from PyQt6.QtGui import QFont
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from gui.chart_widget import ChartWidget
from utils import format_price, get_signal_color


class AnalysisWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Analysis")
        self.setGeometry(100, 100, 1400, 900)
        
        self.fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.signal_gen = SignalGenerator()
        self.current_df = None
        
        self.initUI()
    
    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Stock Ticker:")
        font = QFont("Arial", 11)
        font.setBold(True)
        search_label.setFont(font)
        
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("e.g., AAPL, BBCA.JK")
        self.ticker_input.setMaximumWidth(200)
        
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.analyze_stock)
        analyze_btn.setMaximumWidth(100)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.ticker_input)
        search_layout.addWidget(analyze_btn)
        search_layout.addStretch()
        main_layout.addLayout(search_layout)
        
        # Tabs
        tabs = QTabWidget()
        
        # Chart tab
        self.chart_widget = ChartWidget()
        tabs.addTab(self.chart_widget, "Price Chart")
        
        # Analysis tab
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout()
        
        signal_label = QLabel("Trading Signal:")
        signal_font = QFont("Arial", 11)
        signal_font.setBold(True)
        signal_label.setFont(signal_font)
        
        self.signal_display = QLabel("---")
        self.signal_display.setFont(QFont("Arial", 14))
        self.signal_display.setMinimumHeight(50)
        
        self.analysis_table = QTableWidget()
        self.analysis_table.setColumnCount(2)
        self.analysis_table.setHorizontalHeaderLabels(["Indicator", "Status"])
        
        analysis_layout.addWidget(signal_label)
        analysis_layout.addWidget(self.signal_display)
        analysis_layout.addWidget(QLabel("Details:"))
        analysis_layout.addWidget(self.analysis_table)
        analysis_tab.setLayout(analysis_layout)
        tabs.addTab(analysis_tab, "Analysis")
        
        # Indicators tab
        indicators_tab = QWidget()
        indicators_layout = QVBoxLayout()
        self.indicators_table = QTableWidget()
        self.indicators_table.setColumnCount(2)
        self.indicators_table.setHorizontalHeaderLabels(["Indicator", "Value"])
        indicators_layout.addWidget(self.indicators_table)
        indicators_tab.setLayout(indicators_layout)
        tabs.addTab(indicators_tab, "Indicators")
        
        main_layout.addWidget(tabs)
        main_widget.setLayout(main_layout)
    
    def analyze_stock(self):
        ticker = self.ticker_input.text().strip().upper()
        
        if not ticker:
            self.signal_display.setText("ERROR: Enter ticker")
            return
        
        self.current_df = self.fetcher.fetch_stock_data(ticker)
        if self.current_df is None:
            self.signal_display.setText("ERROR: Data not found")
            return
        
        self.current_df = self.analyzer.add_all_indicators(self.current_df)
        self.chart_widget.plot_data(self.current_df)
        self.update_analysis()
        self.update_indicators()
    
    def update_analysis(self):
        if self.current_df is None:
            return
        
        signal, confidence, details = self.signal_gen.analyze_signals(self.current_df)
        
        self.signal_display.setText(f"{signal} ({confidence:.0f}%)")
        self.signal_display.setStyleSheet(
            f"background-color: {get_signal_color(signal)}; color: white; padding: 10px; border-radius: 5px;"
        )
        
        self.analysis_table.setRowCount(len(details))
        for row, (indicator, status) in enumerate(details.items()):
            self.analysis_table.setItem(row, 0, QTableWidgetItem(indicator))
            self.analysis_table.setItem(row, 1, QTableWidgetItem(status))
    
    def update_indicators(self):
        if self.current_df is None:
            return
        
        latest = self.current_df.iloc[-1]
        indicators = [
            ('Close Price', format_price(latest['close'])),
            ('EMA 9', format_price(latest['ema_9'])),
            ('EMA 21', format_price(latest['ema_21'])),
            ('EMA 55', format_price(latest['ema_55'])),
            ('RSI', f"{latest['rsi']:.2f}"),
            ('MACD', f"{latest['macd']:.6f}"),
            ('Stoch K', f"{latest['stoch_k']:.2f}"),
            ('BB Upper', format_price(latest['bb_upper'])),
        ]
        
        self.indicators_table.setRowCount(len(indicators))
        for row, (name, value) in enumerate(indicators):
            self.indicators_table.setItem(row, 0, QTableWidgetItem(name))
            self.indicators_table.setItem(row, 1, QTableWidgetItem(value))