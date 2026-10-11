"""
Fetch real-time stock data
"""
import yfinance as yf
import pandas as pd

class StockDataFetcher:
    """Fetch stock data from Yahoo Finance"""
    
    def __init__(self):
        self.data_cache = {}
    
    def fetch_stock_data(self, ticker, period='3mo', interval='1d'):
        """
        Fetch stock data
        For swing trading: use 3mo daily data
        """
        try:
            print(f"[DATA] Fetching {ticker}...")
            
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                print(f"[ERROR] No data for {ticker}")
                return None
            
            # Standardize column names
            df.columns = df.columns.str.lower()
            df.index = df.index.tz_localize(None)
            
            # Cache
            self.data_cache[ticker] = df
            
            print(f"[OK] Fetched {len(df)} rows for {ticker}")
            return df
        
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None
    
    def get_stock_info(self, ticker):
        """Get fundamental info"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'eps': info.get('trailingEps', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'avg_volume': info.get('averageVolume', 'N/A'),
            }
        except:
            return None
    
    def get_latest_price(self, ticker):
        """Get current price"""
        try:
            stock = yf.Ticker(ticker)
            return stock.info.get('currentPrice') or stock.info.get('regularMarketPrice')
        except:
            return None