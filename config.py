"""
Configuration for Swing Trade Stock Analyzer
Optimized for 1-2 week swing trading
"""

# SWING TRADE OPTIMIZED EMA SETTINGS
# For 1-2 week swing trades, we use faster moving averages
EMA_FAST = 9      # Quick trend (was 5, too fast for swing)
EMA_MID = 21      # Medium trend (was 20, optimized)
EMA_SLOW = 55     # Longer reference (was 200, too slow for swing)

# MACD - Optimized for faster moves
MACD_FAST = 12    # Keep standard
MACD_SLOW = 26    # Keep standard
MACD_SIGNAL = 9   # Keep standard

# Bollinger Bands
BB_PERIOD = 20
BB_STD = 2

# RSI - Keep standard
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Stochastic - Good for swing trading entry/exit
STOCH_PERIOD = 14
STOCH_K_PERIOD = 3
STOCH_D_PERIOD = 3

# Volume - Important for swing trades
MIN_VOLUME = 500000  # Lower than day trading
MIN_PRICE = 5
MAX_PRICE = 500

# Screening Parameters - Swing Trade Focused
SWING_TRADE_LOOKBACK = '3mo'  # 3 months of data
SWING_TRADE_MIN_RSI = 25      # Recently oversold
SWING_TRADE_MAX_RSI = 45      # Not yet recovered

# Markets
MARKETS = {
    'US': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'NFLX', 'PYPL'],
    'IDX': ['BBCA.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 'INDY.JK', 'UNVR.JK'],
    'UK': ['FTSE:ULVR', 'FTSE:HSBA', 'FTSE:SHEL'],
}

# GUI Settings
GUI_THEME = 'dark'  # 'light' or 'dark'
REFRESH_INTERVAL = 300  # Refresh every 5 minutes (300 seconds)

# Colors
COLORS = {
    'STRONG_BUY': '#00AA00',
    'BUY': '#00DD00',
    'HOLD': '#FFAA00',
    'SELL': '#FF5500',
    'STRONG_SELL': '#FF0000',
    'CHART_UP': '#00DD00',
    'CHART_DOWN': '#FF0000',
}

# Swing Trade Strategy Settings
SWING_TRADE_CONFIG = {
    'entry_rsi_level': 35,        # Enter when RSI recovers from oversold
    'stop_loss_percent': 2.5,     # 2.5% stop loss
    'target_profit_percent': 5,   # 5% profit target
    'max_hold_days': 14,          # Max 2 weeks hold
}