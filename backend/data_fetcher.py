"""
Fetch stock data from Yahoo Finance
"""
import yfinance as yf
import pandas as pd

class StockDataFetcher:
    def __init__(self):
        self.data_cache = {}
    
    def fetch_stock_data(self, ticker, period='3mo', interval='1d'):
        """Fetch stock data"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                return None
            
            df.columns = df.columns.str.lower()
            df.index = df.index.tz_localize(None)
            
            self.data_cache[ticker] = df
            
            return df
        
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            return None
    
    def get_stock_info(self, ticker):
        """Get fundamental stock info"""
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