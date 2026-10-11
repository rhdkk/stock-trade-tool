/**
 * Stock Technical Analyzer - Chart Functions
 */

let chartInstances = {
    price: null,
    volume: null
};

/**
 * Draw price chart with EMAs
 */
function drawPriceChart(canvas, chartData) {
    const ctx = canvas.getContext('2d');
    
    if (!ctx) {
        console.error('Could not get 2D context for price chart');
        return;
    }
    
    if (chartInstances.price) {
        chartInstances.price.destroy();
    }
    
    chartInstances.price = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [
                {
                    label: 'Close Price',
                    data: chartData.close,
                    borderColor: '#ffffff',
                    borderWidth: 2.5,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                },
                {
                    label: 'EMA 9 (Fast)',
                    data: chartData.ema_9,
                    borderColor: '#10b981',
                    borderWidth: 1,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                },
                {
                    label: 'EMA 21 (Mid)',
                    data: chartData.ema_21,
                    borderColor: '#eab308',
                    borderWidth: 1,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                },
                {
                    label: 'EMA 55 (Slow)',
                    data: chartData.ema_55,
                    borderColor: '#f97316',
                    borderWidth: 1,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 12,
                            weight: 'bold',
                        },
                        padding: 15,
                        usePointStyle: true,
                        boxWidth: 12,
                    },
                    position: 'top',
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#0078d4',
                    borderWidth: 1,
                    padding: 10,
                    titleFont: {
                        size: 13,
                        weight: 'bold',
                    },
                    bodyFont: {
                        size: 12,
                    },
                },
            },
            scales: {
                y: {
                    ticks: {
                        color: '#888888',
                        font: {
                            size: 11,
                        },
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        },
                    },
                    grid: {
                        color: '#333333',
                        drawBorder: false,
                        drawTicks: false,
                    },
                },
                x: {
                    ticks: {
                        color: '#888888',
                        font: {
                            size: 10,
                        },
                        maxRotation: 45,
                        minRotation: 0,
                    },
                    grid: {
                        color: '#333333',
                        drawBorder: false,
                        drawTicks: false,
                    },
                },
            },
        },
    });
}

/**
 * Draw volume chart with 20-day average line
 */
function drawVolumeChart(canvas, chartData) {
    const ctx = canvas.getContext('2d');
    
    if (!ctx) {
        console.error('Could not get 2D context for volume chart');
        return;
    }
    
    if (chartInstances.volume) {
        chartInstances.volume.destroy();
    }
    
    // Calculate 20-day moving average
    const volumeAverage20 = calculateMovingAverage(chartData.volume, 20);
    
    // Color volume bars based on price movement
    const colors = [];
    for (let i = 0; i < chartData.close.length; i++) {
        if (i === 0) {
            colors.push('#888888');
        } else {
            colors.push(chartData.close[i] > chartData.close[i - 1] ? '#10b981' : '#ef4444');
        }
    }
    
    chartInstances.volume = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.dates,
            datasets: [
                {
                    label: 'Volume',
                    data: chartData.volume,
                    backgroundColor: colors,
                    borderColor: 'transparent',
                    barThickness: 'flex',
                    maxBarThickness: 8,
                    yAxisID: 'y',
                    order: 2,
                },
                {
                    label: '20-Day Average',
                    data: volumeAverage20,
                    borderColor: '#3b82f6',
                    borderWidth: 2.5,
                    type: 'line',
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    yAxisID: 'y',
                    order: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 11,
                        },
                        padding: 10,
                        boxWidth: 12,
                    },
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#0078d4',
                    borderWidth: 1,
                    padding: 10,
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = formatVolumeCompact(context.parsed.y);
                            return label + ': ' + value;
                        },
                    },
                },
            },
            scales: {
                y: {
                    ticks: {
                        color: '#888888',
                        font: {
                            size: 10,
                        },
                        callback: function(value) {
                            return formatVolumeCompact(value);
                        },
                    },
                    grid: {
                        color: '#333333',
                        drawBorder: false,
                        drawTicks: false,
                    },
                    position: 'left',
                },
                x: {
                    ticks: {
                        color: '#888888',
                        font: {
                            size: 10,
                        },
                        maxRotation: 45,
                        minRotation: 0,
                    },
                    grid: {
                        display: false,
                        drawBorder: false,
                    },
                },
            },
        },
    });
}

/**
 * Calculate moving average
 */
function calculateMovingAverage(data, period) {
    const result = [];
    
    for (let i = 0; i < data.length; i++) {
        if (i < period - 1) {
            result.push(null);
        } else {
            let sum = 0;
            for (let j = i - period + 1; j <= i; j++) {
                sum += data[j];
            }
            result.push(sum / period);
        }
    }
    
    return result;
}

/**
 * Format volume for display
 */
function formatVolumeCompact(volume) {
    if (!volume) return '0';
    if (volume >= 1e9) return (volume / 1e9).toFixed(1) + 'B';
    if (volume >= 1e6) return (volume / 1e6).toFixed(1) + 'M';
    if (volume >= 1e3) return (volume / 1e3).toFixed(1) + 'K';
    return volume.toFixed(0);
}

// Export for use
window.drawPriceChart = drawPriceChart;
window.drawVolumeChart = drawVolumeChart;
window.chartInstances = chartInstances;