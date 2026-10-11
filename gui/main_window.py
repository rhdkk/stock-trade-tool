"""
Main Application Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt

from gui.analysis_window import AnalysisWindow
from gui.screener_window import ScreenerWindow
from gui.styles import get_stylesheet

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Technical Analyzer - Swing Trading Edition")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon())
        
        self.analysis_window = None
        self.screener_window = None
        
        self.initUI()
        self.apply_stylesheet()
    
    def initUI(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        
        # ===== SIDEBAR =====
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar_layout = QVBoxLayout()
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-right: 1px solid #444444;
            }
        """)
        
        # Logo/Title
        title = QLabel("Stock Analyzer")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        
        subtitle = QLabel("Swing Trading Edition")
        subtitle.setFont(QFont("Arial", 9))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888888;")
        sidebar_layout.addWidget(subtitle)
        
        sidebar_layout.addSpacing(30)
        
        # Menu Buttons
        menu_label = QLabel("Menu")
        menu_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        sidebar_layout.addWidget(menu_label)
        
        # Analysis Button
        analysis_btn = QPushButton("📊 Stock Analysis")
        analysis_btn.setMinimumHeight(40)
        analysis_btn.clicked.connect(self.show_analysis)
        sidebar_layout.addWidget(analysis_btn)
        
        # Screener Button
        screener_btn = QPushButton("🔍 Market Screener")
        screener_btn.setMinimumHeight(40)
        screener_btn.clicked.connect(self.show_screener)
        sidebar_layout.addWidget(screener_btn)
        
        sidebar_layout.addSpacing(30)
        
        # Info
        info_label = QLabel("Indicators")
        info_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        sidebar_layout.addWidget(info_label)
        
        indicators_text = QLabel(
            "EMA: 9/21/55\nMACD\nRSI\nBollinger Bands\nStochastic"
        )
        indicators_text.setFont(QFont("Arial", 9))
        indicators_text.setStyleSheet("color: #aaaaaa;")
        sidebar_layout.addWidget(indicators_text)
        
        sidebar_layout.addSpacing(20)
        
        strategy_label = QLabel("Strategy")
        strategy_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        sidebar_layout.addWidget(strategy_label)
        
        strategy_text = QLabel(
            "Swing Trade\n1-2 Week Holds\nOversold Reversals"
        )
        strategy_text.setFont(QFont("Arial", 9))
        strategy_text.setStyleSheet("color: #aaaaaa;")
        sidebar_layout.addWidget(strategy_text)
        
        sidebar_layout.addStretch()
        
        # Footer
        footer = QLabel("v1.0 - Educational Use")
        footer.setFont(QFont("Arial", 8))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #666666;")
        sidebar_layout.addWidget(footer)
        
        sidebar.setLayout(sidebar_layout)
        
        # ===== CONTENT AREA =====
        self.stacked_widget = QStackedWidget()
        
        # Create windows
        self.analysis_window = AnalysisWindow()
        self.screener_window = ScreenerWindow()
        
        self.stacked_widget.addWidget(self.analysis_window)
        self.stacked_widget.addWidget(self.screener_window)
        
        # ===== LAYOUT =====
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        main_widget.setLayout(main_layout)
    
    def show_analysis(self):
        """Show analysis window"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_screener(self):
        """Show screener window"""
        self.stacked_widget.setCurrentIndex(1)
    
    def apply_stylesheet(self):
        """Apply stylesheet"""
        self.setStyleSheet(get_stylesheet('dark'))