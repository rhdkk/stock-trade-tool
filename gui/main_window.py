"""
Main Window
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from gui.analysis_window import AnalysisWindow
from gui.screener_window import ScreenerWindow
from gui.styles import get_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Technical Analyzer - Swing Trading Edition")
        self.setGeometry(100, 100, 1400, 900)
        self.initUI()
        self.setStyleSheet(get_stylesheet('dark'))
    
    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar.setStyleSheet("QWidget { background-color: #252525; border-right: 1px solid #444444; }")
        sidebar_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Stock Analyzer")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        
        subtitle = QLabel("Swing Trading Edition")
        subtitle_font = QFont("Arial", 9)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #888888;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(subtitle)
        
        sidebar_layout.addSpacing(30)
        
        # Menu
        menu_label = QLabel("Menu")
        menu_font = QFont("Arial", 11)
        menu_font.setBold(True)
        menu_label.setFont(menu_font)
        sidebar_layout.addWidget(menu_label)
        
        analysis_btn = QPushButton("📊 Stock Analysis")
        analysis_btn.setMinimumHeight(40)
        analysis_btn.clicked.connect(self.show_analysis)
        sidebar_layout.addWidget(analysis_btn)
        
        screener_btn = QPushButton("🔍 Market Screener")
        screener_btn.setMinimumHeight(40)
        screener_btn.clicked.connect(self.show_screener)
        sidebar_layout.addWidget(screener_btn)
        
        sidebar_layout.addSpacing(30)
        
        # Info
        info_label = QLabel("Indicators")
        info_font = QFont("Arial", 11)
        info_font.setBold(True)
        info_label.setFont(info_font)
        sidebar_layout.addWidget(info_label)
        
        indicators_text = QLabel("EMA: 9/21/55\nMACD\nRSI\nBollinger Bands\nStochastic")
        indicators_text.setFont(QFont("Arial", 9))
        indicators_text.setStyleSheet("color: #aaaaaa;")
        sidebar_layout.addWidget(indicators_text)
        
        sidebar_layout.addStretch()
        
        footer = QLabel("v1.0")
        footer.setFont(QFont("Arial", 8))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #666666;")
        sidebar_layout.addWidget(footer)
        
        sidebar.setLayout(sidebar_layout)
        
        # Content
        self.stacked_widget = QStackedWidget()
        self.analysis_window = AnalysisWindow()
        self.screener_window = ScreenerWindow()
        
        self.stacked_widget.addWidget(self.analysis_window)
        self.stacked_widget.addWidget(self.screener_window)
        
        # Layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        main_widget.setLayout(main_layout)
    
    def show_analysis(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def show_screener(self):
        self.stacked_widget.setCurrentIndex(1)