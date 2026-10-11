"""
Stock market screener
"""
import pandas as pd
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from config import MARKETS

class StockScreener:
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.signal_gen = SignalGenerator()
    
    def screen_market(self, market='US', lookback='3mo'):
        """Screen market for opportunities"""
        if market not in MARKETS:
            return None
        
        tickers = MARKETS[market]
        results = []
        
        for ticker in tickers:
            try:
                df = self.fetcher.fetch_stock_data(ticker, period=lookback)
                
                if df is None:
                    continue
                
                df = self.analyzer.add_all_indicators(df)
                signal, confidence, details = self.signal_gen.analyze_signals(df)
                
                if signal in ['BUY', 'STRONG BUY'] and confidence > 60:
                    current_price = df['close'].iloc[-1]
                    rsi = df['rsi'].iloc[-1]
                    
                    results.append({
                        'Ticker': ticker,
                        'Signal': signal,
                        'Confidence': confidence,
                        'Price': current_price,
                        'RSI': rsi,
                        'Score': confidence * (2 if signal == 'STRONG BUY' else 1)
                    })
            
            except Exception as e:
                print(f"Error screening {ticker}: {str(e)}")
                continue
        
        if not results:
            return None
        
        screen_df = pd.DataFrame(results)
        screen_df = screen_df.sort_values('Score', ascending=False)
        
        return screen_df