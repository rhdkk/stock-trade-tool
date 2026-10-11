"""
Utility functions
"""

def format_price(price):
    """Format price"""
    if price is None:
        return "N/A"
    return f"${price:,.2f}"

def format_percent(value):
    """Format percentage"""
    if value is None:
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
        'STRONG BUY': '#00AA00',
        'BUY': '#00DD00',
        'HOLD': '#FFAA00',
        'SELL': '#FF5500',
        'STRONG SELL': '#FF0000',
    }
    return colors.get(signal, '#CCCCCC')