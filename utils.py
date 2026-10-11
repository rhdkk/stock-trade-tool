"""
Utility functions
"""
from config import COLORS as CONFIG_COLORS
from colorama import init

init(autoreset=True)

# ===== CONSOLE OUTPUT FUNCTIONS =====

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")

# ===== FORMATTING FUNCTIONS =====

def format_price(price):
    """Format price to currency"""
    if price is None or price != price:  # NaN check
        return "N/A"
    try:
        return f"${price:,.2f}"
    except:
        return "N/A"

def format_percent(value):
    """Format percentage"""
    if value is None or value != value:  # NaN check
        return "N/A"
    try:
        symbol = "+" if value > 0 else ""
        return f"{symbol}{value:.2f}%"
    except:
        return "N/A"

def format_volume(volume):
    """Format volume in millions/billions"""
    if volume is None:
        return "N/A"
    try:
        if volume >= 1e9:
            return f"{volume/1e9:.2f}B"
        elif volume >= 1e6:
            return f"{volume/1e6:.2f}M"
        else:
            return f"{volume/1e3:.2f}K"
    except:
        return "N/A"

# ===== SIGNAL FUNCTIONS =====

def get_signal_color(signal):
    """Get color for signal (hex code)"""
    colors = {
        'STRONG BUY': '#00AA00',
        'BUY': '#00DD00',
        'HOLD': '#FFAA00',
        'SELL': '#FF5500',
        'STRONG SELL': '#FF0000',
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

# ===== CONVERSION FUNCTIONS =====

def ticker_to_display(ticker):
    """Convert ticker to display name"""
    return ticker.upper()

def price_change_percent(current, previous):
    """Calculate price change percentage"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100