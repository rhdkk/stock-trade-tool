"""
Technical indicators optimized for swing trading
EMA: 9/21/55 (faster than long-term, good for 1-2 week trades)
"""
import pandas as pd
import numpy as np
from config import (
    EMA_FAST, EMA_MID, EMA_SLOW,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD,
    RSI_PERIOD, STOCH_PERIOD, STOCH_K_PERIOD, STOCH_D_PERIOD
)

class TechnicalAnalyzer:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_ema(data, period):
        """EMA calculation"""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_macd(df):
        """MACD"""
        ema_fast = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
        ema_slow = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=MACD_SIGNAL, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(df):
        """Bollinger Bands"""
        sma = df['close'].rolling(window=BB_PERIOD).mean()
        std = df['close'].rolling(window=BB_PERIOD).std()
        
        upper = sma + (BB_STD * std)
        middle = sma
        lower = sma - (BB_STD * std)
        
        percent_b = (df['close'] - lower) / (upper - lower)
        
        return upper, middle, lower, percent_b
    
    @staticmethod
    def calculate_rsi(df, period=RSI_PERIOD):
        """RSI"""
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_stochastic(df):
        """%K and %D"""
        low_min = df['low'].rolling(window=STOCH_PERIOD).min()
        high_max = df['high'].rolling(window=STOCH_PERIOD).max()
        
        k_percent = 100 * (df['close'] - low_min) / (high_max - low_min)
        d_percent = k_percent.rolling(window=STOCH_D_PERIOD).mean()
        
        return k_percent, d_percent
    
    @staticmethod
    def add_all_indicators(df):
        """Add all indicators to dataframe"""
        # EMAs (Swing trade optimized: 9/21/55)
        df['ema_9'] = TechnicalAnalyzer.calculate_ema(df['close'], EMA_FAST)
        df['ema_21'] = TechnicalAnalyzer.calculate_ema(df['close'], EMA_MID)
        df['ema_55'] = TechnicalAnalyzer.calculate_ema(df['close'], EMA_SLOW)
        
        # MACD
        df['macd'], df['macd_signal'], df['macd_histogram'] = \
            TechnicalAnalyzer.calculate_macd(df)
        
        # Bollinger Bands
        df['bb_upper'], df['bb_middle'], df['bb_lower'], df['bb_percent_b'] = \
            TechnicalAnalyzer.calculate_bollinger_bands(df)
        
        # RSI
        df['rsi'] = TechnicalAnalyzer.calculate_rsi(df)
        
        # Stochastic
        df['stoch_k'], df['stoch_d'] = TechnicalAnalyzer.calculate_stochastic(df)
        
        return df