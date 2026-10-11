/**
 * Stock Technical Analyzer - Main App Logic
 */

const API_BASE = '/api';

/**
 * Fetch stock analysis data
 */
async function fetchStockAnalysis(ticker) {
    try {
        const response = await fetch(`${API_BASE}/stock/${ticker}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error fetching data');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Format functions
 */
function formatPrice(price) {
    if (!price) return 'N/A';
    return '$' + parseFloat(price).toFixed(2);
}

function formatVolume(volume) {
    if (!volume) return 'N/A';
    if (volume >= 1e9) return (volume / 1e9).toFixed(2) + 'B';
    if (volume >= 1e6) return (volume / 1e6).toFixed(2) + 'M';
    if (volume >= 1e3) return (volume / 1e3).toFixed(2) + 'K';
    return volume.toFixed(0);
}

function formatMarketCap(cap) {
    if (!cap || cap === 'N/A') return 'N/A';
    if (cap >= 1e12) return '$' + (cap / 1e12).toFixed(2) + 'T';
    if (cap >= 1e9) return '$' + (cap / 1e9).toFixed(2) + 'B';
    if (cap >= 1e6) return '$' + (cap / 1e6).toFixed(2) + 'M';
    return '$' + cap;
}

/**
 * Signal display functions
 */
function getSignalColor(signal) {
    const colors = {
        'STRONG BUY': 'text-green-400',
        'BUY': 'text-green-400',
        'HOLD': 'text-yellow-400',
        'SELL': 'text-red-400',
        'STRONG SELL': 'text-red-400',
    };
    return colors[signal] || 'text-gray-400';
}

function getSignalClass(signal) {
    const classes = {
        'STRONG BUY': 'border-green-600 bg-green-900',
        'BUY': 'border-green-600 bg-green-900',
        'HOLD': 'border-yellow-600 bg-yellow-900',
        'SELL': 'border-red-600 bg-red-900',
        'STRONG SELL': 'border-red-600 bg-red-900',
    };
    return classes[signal] || 'border-gray-600';
}

function getSignalEmoji(signal) {
    const emojis = {
        'STRONG BUY': '🟢🟢',
        'BUY': '🟢',
        'HOLD': '🟡',
        'SELL': '🔴',
        'STRONG SELL': '🔴🔴',
    };
    return emojis[signal] || '⚪';
}

/**
 * Alpine.js component for analysis page
 */
function analysisPage() {
    return {
        ticker: '',
        loading: false,
        error: '',
        data: null,
        activeTab: 'analysis',
        chart: null,
        
        async analyzeStock() {
            if (!this.ticker) {
                this.error = 'Please enter a ticker';
                return;
            }
            
            this.loading = true;
            this.error = '';
            this.data = null;
            
            try {
                this.data = await fetchStockAnalysis(this.ticker);
                setTimeout(() => this.drawChart(), 100);
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },
        
        drawChart() {
            try {
                const canvasPrice = document.getElementById('priceChart');
                const canvasVolume = document.getElementById('volumeChart');
                
                if (!canvasPrice || !canvasVolume) {
                    console.error('Canvas elements not found');
                    return;
                }
                
                drawPriceChart(canvasPrice, this.data.chart);
                drawVolumeChart(canvasVolume, this.data.chart);
                
            } catch (error) {
                console.error('Chart error:', error);
            }
        },
        
        getSignalColor,
        getSignalClass,
        getSignalEmoji,
        formatPrice,
        formatVolume,
        formatMarketCap,
    };
}

// Export for use
window.analysisPage = analysisPage;
window.fetchStockAnalysis = fetchStockAnalysis;
window.formatPrice = formatPrice;
window.formatVolume = formatVolume;
window.formatMarketCap = formatMarketCap;