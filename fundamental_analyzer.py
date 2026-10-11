"""
Fundamental analysis for additional decision-making support
"""
import pandas as pd
from data_fetcher import StockDataFetcher

class FundamentalAnalyzer:
    """Analyze fundamental data"""
    
    @staticmethod
    def get_fundamental_overview(ticker):
        """Get fundamental overview"""
        fetcher = StockDataFetcher()
        info = fetcher.get_stock_info(ticker)
        
        if not info:
            return None
        
        return {
            'name': info.get('name'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'market_cap': info.get('market_cap'),
            'pe_ratio': info.get('pe_ratio'),
            'eps': info.get('eps'),
            'dividend_yield': info.get('dividend_yield'),
            '52_week_high': info.get('52_week_high'),
            '52_week_low': info.get('52_week_low'),
            'avg_volume': info.get('avg_volume'),
        }
    
    @staticmethod
    def print_fundamental_overview(ticker, fundamental_data):
        """Print fundamental data in formatted way"""
        from utils import format_price, format_percent, format_volume
        
        print("\n" + "="*60)
        print("FUNDAMENTAL OVERVIEW".center(60))
        print("="*60 + "\n")
        
        if not fundamental_data:
            print("❌ Fundamental data not available")
            return
        
        # Company Info
        if fundamental_data.get('name'):
            print(f"Company Name      : {fundamental_data['name']}")
        if fundamental_data.get('sector'):
            print(f"Sector            : {fundamental_data['sector']}")
        if fundamental_data.get('industry'):
            print(f"Industry          : {fundamental_data['industry']}")
        
        print()
        
        # Valuation
        if fundamental_data.get('market_cap') and fundamental_data['market_cap'] != 'N/A':
            cap = fundamental_data['market_cap']
            if cap >= 1e12:
                cap_str = f"${cap/1e12:.2f}T"
            elif cap >= 1e9:
                cap_str = f"${cap/1e9:.2f}B"
            else:
                cap_str = f"${cap/1e6:.2f}M"
            print(f"Market Cap        : {cap_str}")
        
        if fundamental_data.get('pe_ratio') and fundamental_data['pe_ratio'] != 'N/A':
            print(f"P/E Ratio         : {fundamental_data['pe_ratio']:.2f}x")
        
        if fundamental_data.get('eps') and fundamental_data['eps'] != 'N/A':
            print(f"EPS               : ${fundamental_data['eps']:.2f}")
        
        if fundamental_data.get('dividend_yield') and fundamental_data['dividend_yield'] != 'N/A':
            div_yield = fundamental_data['dividend_yield'] * 100
            print(f"Dividend Yield    : {div_yield:.2f}%")
        
        print()
        
        # Price Range
        if fundamental_data.get('52_week_high') and fundamental_data['52_week_high'] != 'N/A':
            print(f"52-Week High      : {format_price(fundamental_data['52_week_high'])}")
        
        if fundamental_data.get('52_week_low') and fundamental_data['52_week_low'] != 'N/A':
            print(f"52-Week Low       : {format_price(fundamental_data['52_week_low'])}")
        
        if fundamental_data.get('avg_volume') and fundamental_data['avg_volume'] != 'N/A':
            print(f"Avg Volume        : {format_volume(fundamental_data['avg_volume'])}")
        
        print("\n" + "="*60)