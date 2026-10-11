"""
Stock Technical Analyzer - Web App
Flask Backend - Analysis Only
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
import pandas as pd

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from signals import SignalGenerator
from fundamental_analyzer import FundamentalAnalyzer

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Initialize components
fetcher = StockDataFetcher()
analyzer = TechnicalAnalyzer()
signal_gen = SignalGenerator()
fund_analyzer = FundamentalAnalyzer()

# ===== ROUTES =====

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """Stock analysis page"""
    return render_template('analysis.html')

# ===== API ENDPOINTS =====

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_analysis(ticker):
    """Analyze single stock"""
    try:
        ticker = ticker.upper()
        period = request.args.get('period', '3mo')
        interval = request.args.get('interval', '1d')
        
        # Fetch data
        df = fetcher.fetch_stock_data(ticker, period=period, interval=interval)
        
        if df is None or df.empty:
            return jsonify({'error': f'No data found for {ticker}'}), 404
        
        # Add indicators
        df = analyzer.add_all_indicators(df)
        
        # Get signal
        signal, confidence, details = signal_gen.analyze_signals(df)
        
        # Get fundamentals
        fundamental = fund_analyzer.get_fundamental_overview(ticker)
        
        # Prepare chart data
        latest = df.iloc[-1]
        chart_data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'close': df['close'].tolist(),
            'volume': df['volume'].tolist(),
            'ema_9': df['ema_9'].tolist(),
            'ema_21': df['ema_21'].tolist(),
            'ema_55': df['ema_55'].tolist(),
        }
        
        # Prepare indicators
        indicators = {
            'price': float(latest['close']),
            'ema_9': float(latest['ema_9']) if not pd.isna(latest['ema_9']) else None,
            'ema_21': float(latest['ema_21']) if not pd.isna(latest['ema_21']) else None,
            'ema_55': float(latest['ema_55']) if not pd.isna(latest['ema_55']) else None,
            'rsi': float(latest['rsi']) if not pd.isna(latest['rsi']) else None,
            'macd': float(latest['macd']) if not pd.isna(latest['macd']) else None,
            'macd_signal': float(latest['macd_signal']) if not pd.isna(latest['macd_signal']) else None,
            'bb_upper': float(latest['bb_upper']) if not pd.isna(latest['bb_upper']) else None,
            'bb_lower': float(latest['bb_lower']) if not pd.isna(latest['bb_lower']) else None,
            'stoch_k': float(latest['stoch_k']) if not pd.isna(latest['stoch_k']) else None,
            'stoch_d': float(latest['stoch_d']) if not pd.isna(latest['stoch_d']) else None,
            'volume': float(latest['volume']) if not pd.isna(latest['volume']) else None,
        }
        
        return jsonify({
            'ticker': ticker,
            'signal': signal,
            'confidence': confidence,
            'details': details,
            'indicators': indicators,
            'fundamentals': fundamental,
            'chart': chart_data,
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({'status': 'OK'})

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ===== MAIN =====

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)