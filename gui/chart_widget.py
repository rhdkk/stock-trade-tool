"""
Chart widget for displaying stock price and indicators
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from config import COLORS

class ChartWidget(QWidget):
    """Chart for price and indicators"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        self.layout = QVBoxLayout()
        
        # Create plot
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Price', units='USD')
        self.plot_widget.setLabel('bottom', 'Date')
        self.plot_widget.setTitle('Stock Price with EMAs')
        
        # Style
        self.plot_widget.setBackground('#1e1e1e')
        self.plot_widget.getAxis('left').setPen(pg.mkPen('#666666'))
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen('#666666'))
        
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
    
    def plot_data(self, df):
        """Plot price data with EMAs"""
        if df is None or df.empty:
            return
        
        self.plot_widget.clear()
        
        # X-axis: dates as numbers
        x = list(range(len(df)))
        
        # Price
        price = df['close'].values
        self.plot_widget.plot(x, price, pen=pg.mkPen('#ffffff', width=2), 
                             name='Close Price')
        
        # EMAs
        if 'ema_9' in df.columns:
            ema_9 = df['ema_9'].values
            self.plot_widget.plot(x, ema_9, pen=pg.mkPen('#00ff00', width=1.5),
                                 name='EMA 9')
        
        if 'ema_21' in df.columns:
            ema_21 = df['ema_21'].values
            self.plot_widget.plot(x, ema_21, pen=pg.mkPen('#ffff00', width=1.5),
                                 name='EMA 21')
        
        if 'ema_55' in df.columns:
            ema_55 = df['ema_55'].values
            self.plot_widget.plot(x, ema_55, pen=pg.mkPen('#ff6600', width=1.5),
                                 name='EMA 55')
        
        # Legend
        self.plot_widget.addLegend()