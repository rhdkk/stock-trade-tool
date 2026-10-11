"""
Fundamental analysis
"""
from data_fetcher import StockDataFetcher

class FundamentalAnalyzer:
    
    @staticmethod
    def get_fundamental_overview(ticker):
        """Get fundamental data"""
        fetcher = StockDataFetcher()
        return fetcher.get_stock_info(ticker)