from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Configuration
EMA_FAST = 9
EMA_MID = 21
EMA_SLOW = 55
RSI_PERIOD = 14

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/api/stock/<ticker>')
def get_stock(ticker):
    try:
        ticker = ticker.upper()
        
        # Fetch data
        stock = yf.Ticker(ticker)
        df = stock.history(period='3mo')
        
        if df.empty:
            return jsonify({'error': 'No data found'}), 404
        
        df.columns = df.columns.str.lower()
        
        # Calculate EMA
        df['ema_9'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
        df['ema_21'] = df['close'].ewm(span=EMA_MID, adjust=False).mean()
        df['ema_55'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=RSI_PERIOD).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=RSI_PERIOD).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        latest = df.iloc[-1]
        
        # Determine signal
        if latest['close'] > latest['ema_9'] > latest['ema_21'] > latest['ema_55']:
            signal = 'BUY'
            confidence = 85
        elif latest['close'] < latest['ema_9'] < latest['ema_21'] < latest['ema_55']:
            signal = 'SELL'
            confidence = 85
        else:
            signal = 'HOLD'
            confidence = 50
        
        return jsonify({
            'ticker': ticker,
            'signal': signal,
            'confidence': confidence,
            'price': float(latest['close']),
            'rsi': float(latest['rsi']),
            'ema_9': float(latest['ema_9']),
            'ema_21': float(latest['ema_21']),
            'ema_55': float(latest['ema_55']),
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)