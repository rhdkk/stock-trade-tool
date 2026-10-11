"""
Screen for swing trade opportunities
"""
import pandas as pd
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from config import MARKETS, SWING_TRADE_CONFIG

class StockScreener:
    """Screen stocks for swing trades"""
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.signal_gen = SignalGenerator()
    
    def screen_market(self, market='US'):
        """Screen market for swing trade setups"""
        print(f"\n[SCREEN] Scanning {market} market...")
        
        if market not in MARKETS:
            return None
        
        tickers = MARKETS[market]
        results = []
        
        for ticker in tickers:
            try:
                # Fetch data
                df = self.fetcher.fetch_stock_data(ticker, period='3mo', interval='1d')
                
                if df is None:
                    continue
                
                # Add indicators
                df = self.analyzer.add_all_indicators(df)
                
                # Get signal
                signal, confidence, details = self.signal_gen.analyze_signals(df)
                
                # Filter: Only BUY signals with high confidence
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
                print(f"[ERROR] {ticker}: {str(e)}")
                continue
        
        if not results:
            print("[INFO] No swing trade setups found")
            return None
        
        # Sort by score
        screen_df = pd.DataFrame(results)
        screen_df = screen_df.sort_values('Score', ascending=False)
        
        return screen_df