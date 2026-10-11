"""
Chart Widget
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Price', units='USD')
        self.plot_widget.setLabel('bottom', 'Date')
        self.plot_widget.setTitle('Stock Price with EMAs')
        self.plot_widget.setBackground('#1e1e1e')
        
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
    
    def plot_data(self, df):
        if df is None or df.empty:
            return
        
        self.plot_widget.clear()
        
        x = list(range(len(df)))
        price = df['close'].values
        
        self.plot_widget.plot(x, price, pen=pg.mkPen('#ffffff', width=2), name='Close')
        
        if 'ema_9' in df.columns:
            self.plot_widget.plot(x, df['ema_9'].values, pen=pg.mkPen('#00ff00', width=1.5), name='EMA 9')
        if 'ema_21' in df.columns:
            self.plot_widget.plot(x, df['ema_21'].values, pen=pg.mkPen('#ffff00', width=1.5), name='EMA 21')
        if 'ema_55' in df.columns:
            self.plot_widget.plot(x, df['ema_55'].values, pen=pg.mkPen('#ff6600', width=1.5), name='EMA 55')