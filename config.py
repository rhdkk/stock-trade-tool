"""
Configuration for Stock Technical Analyzer Web App
"""

# EMA Settings (Swing Trading Optimized)
EMA_FAST = 9
EMA_MID = 21
EMA_SLOW = 55

# MACD Settings
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands
BB_PERIOD = 20
BB_STD = 2

# RSI
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Stochastic
STOCH_PERIOD = 14
STOCH_K_PERIOD = 3
STOCH_D_PERIOD = 3

# Screening
MIN_VOLUME = 500000
MIN_PRICE = 5
MAX_PRICE = 500

# Stock Markets
MARKETS = {
    'US': [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NVDA', 'AMD', 'NFLX', 'PYPL'
    ],
    'IDX': [
        'BBCA.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK',
        'INDY.JK', 'UNVR.JK'
    ],
    'UK': [
        'FTSE:ULVR', 'FTSE:HSBA', 'FTSE:SHEL'
    ],
}

# Swing Trade Config
SWING_TRADE_CONFIG = {
    'entry_rsi_level': 35,
    'stop_loss_percent': 2.5,
    'target_profit_percent': 5,
    'max_hold_days': 14,
}