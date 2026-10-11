"""
Signal generation
"""
import pandas as pd
from config import RSI_OVERBOUGHT, RSI_OVERSOLD

class SignalGenerator:
    
    @staticmethod
    def analyze_signals(df):
        """Generate trading signal"""
        if df is None or len(df) < 30:
            return 'HOLD', 0, {}
        
        latest = df.iloc[-1]
        details = {}
        
        buy_score = 0
        sell_score = 0
        
        # EMA Analysis
        if pd.notna(latest['ema_9']) and pd.notna(latest['ema_21']) and pd.notna(latest['ema_55']):
            close = latest['close']
            
            if close > latest['ema_9'] > latest['ema_21'] > latest['ema_55']:
                buy_score += 2
                details['EMA'] = '🟢 Perfect Uptrend'
            elif close < latest['ema_9'] < latest['ema_21'] < latest['ema_55']:
                sell_score += 2
                details['EMA'] = '🔴 Strong Downtrend'
            else:
                details['EMA'] = '🟡 Mixed'
        
        # RSI Analysis
        if pd.notna(latest['rsi']):
            rsi = latest['rsi']
            if rsi < RSI_OVERSOLD:
                buy_score += 2
                details['RSI'] = f'🟢 Oversold ({rsi:.0f})'
            elif rsi > RSI_OVERBOUGHT:
                sell_score += 2
                details['RSI'] = f'🔴 Overbought ({rsi:.0f})'
            else:
                details['RSI'] = f'🟡 Neutral ({rsi:.0f})'
        
        # MACD Analysis
        if pd.notna(latest['macd']) and pd.notna(latest['macd_signal']):
            if latest['macd'] > latest['macd_signal']:
                buy_score += 1
                details['MACD'] = '🟢 Bullish'
            else:
                sell_score += 1
                details['MACD'] = '🔴 Bearish'
        
        # Bollinger Bands
        if pd.notna(latest['bb_percent_b']):
            bb = latest['bb_percent_b']
            if bb < 0:
                buy_score += 1.5
                details['BB'] = '🟢 Oversold'
            elif bb > 1:
                sell_score += 1.5
                details['BB'] = '🔴 Overbought'
        
        # Stochastic
        if pd.notna(latest['stoch_k']):
            k = latest['stoch_k']
            if k < 20:
                buy_score += 1
                details['Stoch'] = f'🟢 Oversold ({k:.0f})'
            elif k > 80:
                sell_score += 1
                details['Stoch'] = f'🔴 Overbought ({k:.0f})'
        
        # Calculate confidence
        net_score = buy_score - sell_score
        total_score = buy_score + sell_score
        
        if total_score > 0:
            confidence = abs(net_score) / total_score * 100
        else:
            confidence = 0
        
        # Generate signal
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