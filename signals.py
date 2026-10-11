"""
Generate swing trade signals
"""
import pandas as pd
from config import RSI_OVERBOUGHT, RSI_OVERSOLD, SWING_TRADE_CONFIG

class SignalGenerator:
    """Generate trading signals for swing trades"""
    
    @staticmethod
    def analyze_signals(df):
        """
        Swing trade signal analysis
        Looking for: Oversold conditions + recovery signals
        """
        if df is None or len(df) < 30:
            return 'HOLD', 0, {}
        
        latest = df.iloc[-1]
        details = {}
        
        buy_score = 0
        sell_score = 0
        
        # ===== EMA ANALYSIS (Swing trade optimized) =====
        # Look for: Price above 9 EMA, 9 above 21, 21 above 55 = UPTREND
        if pd.notna(latest['ema_9']) and pd.notna(latest['ema_21']) and pd.notna(latest['ema_55']):
            close = latest['close']
            
            # Strong uptrend setup
            if close > latest['ema_9'] > latest['ema_21'] > latest['ema_55']:
                buy_score += 2
                details['EMA Setup'] = '🟢 Perfect Uptrend (Close > 9 > 21 > 55)'
            # Weak uptrend
            elif close > latest['ema_9'] > latest['ema_21']:
                buy_score += 1
                details['EMA Setup'] = '🟢 Uptrend (Close > 9 > 21)'
            # Downtrend
            elif close < latest['ema_9'] < latest['ema_21'] < latest['ema_55']:
                sell_score += 2
                details['EMA Setup'] = '🔴 Strong Downtrend'
            else:
                details['EMA Setup'] = '🟡 Mixed'
        
        # ===== RSI ANALYSIS (Key for swing trades) =====
        if pd.notna(latest['rsi']):
            rsi = latest['rsi']
            
            # Oversold = Swing trade entry opportunity
            if rsi < RSI_OVERSOLD:
                buy_score += 2
                details['RSI'] = f'🟢 OVERSOLD ({rsi:.0f}) - ENTRY SIGNAL'
            # Recovering from oversold
            elif rsi < 45:
                buy_score += 1
                details['RSI'] = f'🟢 Bullish ({rsi:.0f}) - Rising from oversold'
            # Overbought = Exit signal
            elif rsi > RSI_OVERBOUGHT:
                sell_score += 2
                details['RSI'] = f'🔴 OVERBOUGHT ({rsi:.0f}) - EXIT SIGNAL'
            # Approaching overbought
            elif rsi > 60:
                sell_score += 1
                details['RSI'] = f'🔴 Bearish ({rsi:.0f}) - Approaching overbought'
            else:
                details['RSI'] = f'🟡 Neutral ({rsi:.0f})'
        
        # ===== MACD ANALYSIS =====
        if pd.notna(latest['macd']) and pd.notna(latest['macd_signal']):
            if latest['macd'] > latest['macd_signal']:
                # Check for bullish crossover
                if len(df) > 1:
                    prev_macd = df.iloc[-2]['macd']
                    prev_signal = df.iloc[-2]['macd_signal']
                    
                    if prev_macd <= prev_signal:  # Just crossed up
                        buy_score += 2
                        details['MACD'] = '🟢 BULLISH CROSSOVER'
                    else:
                        buy_score += 0.5
                        details['MACD'] = '🟢 Bullish (MACD > Signal)'
            else:
                sell_score += 1
                details['MACD'] = '🔴 Bearish (MACD < Signal)'
        
        # ===== BOLLINGER BANDS =====
        if pd.notna(latest['bb_percent_b']):
            bb_percent = latest['bb_percent_b']
            
            if bb_percent < 0:
                buy_score += 2
                details['Bollinger Bands'] = '🟢 Price BELOW lower band (oversold)'
            elif bb_percent > 1:
                sell_score += 2
                details['Bollinger Bands'] = '🔴 Price ABOVE upper band (overbought)'
            else:
                details['Bollinger Bands'] = '🟡 Within bands'
        
        # ===== STOCHASTIC =====
        if pd.notna(latest['stoch_k']) and pd.notna(latest['stoch_d']):
            k = latest['stoch_k']
            d = latest['stoch_d']
            
            if k < 20 and d < 20:
                buy_score += 1.5
                details['Stochastic'] = f'🟢 Oversold (K:{k:.0f}, D:{d:.0f})'
            elif k > 80 and d > 80:
                sell_score += 1.5
                details['Stochastic'] = f'🔴 Overbought (K:{k:.0f}, D:{d:.0f})'
        
        # ===== CALCULATE CONFIDENCE =====
        net_score = buy_score - sell_score
        total_score = buy_score + sell_score
        
        if total_score > 0:
            confidence = abs(net_score) / total_score * 100
        else:
            confidence = 0
        
        # ===== GENERATE SIGNAL =====
        if net_score >= 5:
            signal = 'STRONG BUY'
        elif net_score >= 2:
            signal = 'BUY'
        elif net_score <= -5:
            signal = 'STRONG SELL'
        elif net_score <= -2:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        
        return signal, confidence, details