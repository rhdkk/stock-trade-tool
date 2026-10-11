"""
Utility functions
"""
from config import COLORS as CONFIG_COLORS

def format_price(price):
    """Format price"""
    if price is None or price != price:  # NaN check
        return "N/A"
    return f"${price:,.2f}"

def format_percent(value):
    """Format percentage"""
    if value is None or value != value:  # NaN check
        return "N/A"
    return f"{value:+.2f}%"

def format_volume(volume):
    """Format volume"""
    if volume is None:
        return "N/A"
    if volume >= 1e9:
        return f"{volume/1e9:.2f}B"
    elif volume >= 1e6:
        return f"{volume/1e6:.2f}M"
    else:
        return f"{volume/1e3:.2f}K"

def get_signal_color(signal):
    """Get color for signal"""
    colors = {
        'STRONG BUY': CONFIG_COLORS['STRONG_BUY'],
        'BUY': CONFIG_COLORS['BUY'],
        'HOLD': CONFIG_COLORS['HOLD'],
        'SELL': CONFIG_COLORS['SELL'],
        'STRONG SELL': CONFIG_COLORS['STRONG_SELL'],
    }
    return colors.get(signal, '#CCCCCC')

def get_signal_emoji(signal):
    """Get emoji for signal"""
    signals = {
        'STRONG BUY': '🟢🟢',
        'BUY': '🟢',
        'HOLD': '🟡',
        'SELL': '🔴',
        'STRONG SELL': '🔴🔴',
    }
    return signals.get(signal, '⚪')