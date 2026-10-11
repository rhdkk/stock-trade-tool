"""
Main Stock Analysis Tool
Real-time Technical Analysis with Buy/Sell Signals
"""

import sys
from utils import (
    print_header, print_success, print_error, print_warning, 
    print_info, format_price, format_percent
)
from config import MARKETS, COLORS
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from fundamental_analyzer import FundamentalAnalyzer
from screener import StockScreener

def print_menu():
    """Print main menu"""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}{'='*60}")
    print("STOCK TECHNICAL ANALYZER - MAIN MENU".center(60))
    print(f"{'='*60}{COLORS['RESET']}\n")
    
    print("1. Analyze Single Stock (Buy/Sell Signal)")
    print("2. Screen Market for Bullish Reversals")
    print("3. Compare Multiple Stocks")
    print("4. Customize Stock Screening")
    print("0. Exit")
    print()

def analyze_single_stock():
    """Analyze a single stock"""
    print_header("SINGLE STOCK ANALYSIS")
    
    ticker = input("Enter Stock Ticker (e.g., AAPL, BBCA.JK): ").strip().upper()
    
    if not ticker:
        print_error("Invalid ticker!")
        return
    
    print("\nSelect timeframe:")
    print("1. Daily (1 year)")
    print("2. Weekly (2 years)")
    print("3. Monthly (5 years)")
    print("4. 3 months")
    
    timeframe_choice = input("Enter choice (1-4): ").strip()
    
    timeframe_map = {
        '1': ('1y', '1d'),
        '2': ('2y', '1wk'),
        '3': ('5y', '1mo'),
        '4': ('3mo', '1d'),
    }
    
    period, interval = timeframe_map.get(timeframe_choice, ('1y', '1d'))
    
    # Fetch data
    fetcher = StockDataFetcher()
    df = fetcher.fetch_stock_data(ticker, period=period, interval=interval)
    
    if df is None or df.empty:
        print_error("Failed to fetch stock data. Please check the ticker symbol.")
        return
    
    # Add technical indicators
    analyzer = TechnicalAnalyzer()
    df = analyzer.add_all_indicators(df)
    
    # Get current price
    current_price = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2] if len(df) > 1 else current_price
    price_change = current_price - prev_close
    price_change_pct = (price_change / prev_close * 100) if prev_close != 0 else 0
    
    # Generate signal
    signal_gen = SignalGenerator()
    signal_gen.print_signal_analysis(df, ticker)
    
    # Print current price info
    print(f"\n💰 PRICE INFORMATION")
    print("-" * 60)
    print(f"Current Price     : {format_price(current_price)}")
    print(f"Change (Today)    : {format_percent(price_change_pct)}")
    print()
    
    # Print indicator values
    latest = df.iloc[-1]
    print(f"📊 INDICATOR VALUES")
    print("-" * 60)
    print(f"EMA 5             : {format_price(latest['ema_5'])}")
    print(f"EMA 20            : {format_price(latest['ema_20'])}")
    print(f"EMA 200           : {format_price(latest['ema_200'])}")
    print()
    print(f"RSI (14)          : {latest['rsi']:.2f}")
    print(f"MACD              : {latest['macd']:.6f}")
    print(f"MACD Signal       : {latest['macd_signal']:.6f}")
    print(f"MACD Histogram    : {latest['macd_histogram']:.6f}")
    print()
    print(f"Stoch %K          : {latest['stoch_k']:.2f}")
    print(f"Stoch %D          : {latest['stoch_d']:.2f}")
    print()
    print(f"BB Upper          : {format_price(latest['bb_upper'])}")
    print(f"BB Middle         : {format_price(latest['bb_middle'])}")
    print(f"BB Lower          : {format_price(latest['bb_lower'])}")
    print(f"BB %B             : {latest['bb_percent_b']:.2f}")
    print()
    
    # Volume info
    if 'volume' in df.columns:
        current_volume = latest['volume']
        avg_volume_20 = df['volume'].iloc[-20:].mean()
        volume_ratio = current_volume / avg_volume_20 if avg_volume_20 > 0 else 1
        
        print(f"Current Volume    : {current_volume:,.0f}")
        print(f"Avg Volume (20d)  : {avg_volume_20:,.0f}")
        print(f"Volume Ratio      : {volume_ratio:.2f}x")
    
    print("-" * 60)
    
    # Fundamental analysis
    print("\n")
    fund_analyzer = FundamentalAnalyzer()
    fundamental_data = fund_analyzer.get_fundamental_overview(ticker)
    fund_analyzer.print_fundamental_overview(ticker, fundamental_data)
    
    # Recommendation
    print_header("FINAL RECOMMENDATION")
    signal, confidence = signal_gen.analyze_signals(df)
    
    if signal == 'STRONG BUY':
        print(f"{COLORS['GREEN']}🚀 STRONG BUY SIGNAL{COLORS['RESET']}")
        print(f"Confidence: {confidence:.1f}%")
        print("\nRationale:")
        print("- Multiple indicators showing bullish momentum")
        print("- Technical setup favors upside move")
        print("- Consider entering long position with stop loss")
    
    elif signal == 'BUY':
        print(f"{COLORS['GREEN']}✅ BUY SIGNAL{COLORS['RESET']}")
        print(f"Confidence: {confidence:.1f}%")
        print("\nRationale:")
        print("- Bullish signals detected on charts")
        print("- Risk/reward looks favorable")
        print("- Consider starting or adding to position")
    
    elif signal == 'HOLD':
        print(f"{COLORS['YELLOW']}⏸️  HOLD SIGNAL{COLORS['RESET']}")
        print(f"Confidence: {confidence:.1f}%")
        print("\nRationale:")
        print("- Mixed signals, no clear direction")
        print("- Wait for better setup")
        print("- Monitor for breakout")
    
    elif signal == 'SELL':
        print(f"{COLORS['RED']}📉 SELL SIGNAL{COLORS['RESET']}")
        print(f"Confidence: {confidence:.1f}%")
        print("\nRationale:")
        print("- Bearish signals dominant")
        print("- Risk of further downside")
        print("- Consider exiting position or waiting for reversal")
    
    elif signal == 'STRONG SELL':
        print(f"{COLORS['RED']}🔴 STRONG SELL SIGNAL{COLORS['RESET']}")
        print(f"Confidence: {confidence:.1f}%")
        print("\nRationale:")
        print("- Multiple indicators showing weakness")
        print("- High probability of continued decline")
        print("- Strongly consider closing positions")
    
    print(f"\n{COLORS['YELLOW']}⚠️  DISCLAIMER{COLORS['RESET']}")
    print("This analysis is for educational purposes only.")
    print("Always do your own research and consult with financial advisors.")
    print("Past performance doesn't guarantee future results.")

def screen_market():
    """Screen market for opportunities"""
    print_header("MARKET SCREENING")
    
    print("Available Markets:")
    for i, market in enumerate(MARKETS.keys(), 1):
        print(f"{i}. {market}")
    
    choice = input("Select market: ").strip()
    
    market_list = list(MARKETS.keys())
    if choice.isdigit() and 1 <= int(choice) <= len(market_list):
        market = market_list[int(choice) - 1]
    else:
        market = choice.upper()
    
    screener = StockScreener()
    results = screener.screen_market(market, lookback='3mo')
    
    if results is not None and len(results) > 0:
        print_success(f"\nFound {len(results)} bullish reversal opportunities!")
        print("\nTop 3 Opportunities:")
        for idx, row in results.head(3).iterrows():
            print(f"\n{idx+1}. {row['Ticker']}")
            print(f"   Signal: {row['Signal']} (Confidence: {row['Confidence']:.1f}%)")
            print(f"   Price: ${row['Current Price']:.2f}")
            print(f"   RSI: {row['RSI']:.2f}")

def compare_stocks():
    """Compare multiple stocks"""
    print_header("STOCK COMPARISON")
    
    tickers_input = input("Enter tickers separated by comma (e.g., AAPL,MSFT,GOOGL): ")
    tickers = [t.strip().upper() for t in tickers_input.split(',')]
    
    if not tickers:
        print_error("No tickers provided!")
        return
    
    screener = StockScreener()
    results = screener.screen_custom_list(tickers)
    
    if results is not None:
        print_header("COMPARISON RESULTS")
        print(results.to_string(index=False))

def custom_screening():
    """Custom stock screening"""
    print_header("CUSTOM STOCK SCREENING")
    
    print("Enter stock tickers (one per line, empty line to finish):")
    tickers = []
    
    while True:
        ticker = input(f"Ticker {len(tickers)+1}: ").strip().upper()
        if not ticker:
            break
        tickers.append(ticker)
    
    if tickers:
        screener = StockScreener()
        results = screener.screen_custom_list(tickers)
        if results is not None:
            print_header("SCREENING RESULTS")
            print(results.to_string(index=False))

def main():
    """Main application loop"""
    print_header("WELCOME TO STOCK TECHNICAL ANALYZER")
    print("Real-time Technical Analysis Tool")
    print("Indicators: MACD, Bollinger Bands, EMA, RSI, Stochastic, Volume")
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-4): ").strip()
        
        if choice == '1':
            analyze_single_stock()
        
        elif choice == '2':
            screen_market()
        
        elif choice == '3':
            compare_stocks()
        
        elif choice == '4':
            custom_screening()
        
        elif choice == '0':
            print_success("\nThank you for using Stock Technical Analyzer!")
            print("Happy trading! 📈")
            sys.exit(0)
        
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        sys.exit(1)