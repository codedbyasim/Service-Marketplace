/*
 * Service-Marketplace/static/js/charts.js
 * ---------------------------------------
 * Initializes Chart.js visualizations for the dashboard.
 * Requires Chart.js library to be loaded first.
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. Order Status Distribution Chart (Doughnut Chart) ---

    const orderStatusChartCtx = document.getElementById('orderStatusChart');
    if (orderStatusChartCtx) {
        // Data is assumed to be passed via Django template variables and accessible in the DOM
        // Example: data-pending="5", data-in-progress="8", data-completed="12", data-cancelled="3"
        
        const dataElement = orderStatusChartCtx.closest('[data-order-stats]');
        if (dataElement) {
            const pending = parseInt(dataElement.dataset.pending) || 0;
            const inProgress = parseInt(dataElement.dataset.inProgress) || 0;
            const completed = parseInt(dataElement.dataset.completed) || 0;
            const cancelled = parseInt(dataElement.dataset.cancelled) || 0;

            const data = {
                labels: [
                    'Completed',
                    'In Progress',
                    'Pending',
                    'Cancelled'
                ],
                datasets: [{
                    data: [completed, inProgress, pending, cancelled],
                    backgroundColor: [
                        '#28a745', // Success (Green)
                        '#17a2b8', // Info (Blue-Green)
                        '#ffc107', // Warning (Yellow)
                        '#dc3545'  // Danger (Red)
                    ],
                    hoverOffset: 4
                }]
            };

            new Chart(orderStatusChartCtx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: 'Order Status Distribution'
                        }
                    }
                }
            });
        }
    }


    // --- 2. Monthly Earnings Trend Chart (Line Chart) ---

    const earningsTrendChartCtx = document.getElementById('earningsTrendChart');
    if (earningsTrendChartCtx) {
        // Data is assumed to be passed via Django template variables
        // Example: data-months="['Jan', 'Feb', 'Mar']", data-earnings="[1200, 1900, 3000]"
        
        const dataElement = earningsTrendChartCtx.closest('[data-earnings-data]');
        if (dataElement) {
            // These would be JSON strings passed from the view, so parse them
            const months = JSON.parse(dataElement.dataset.months); 
            const earnings = JSON.parse(dataElement.dataset.earnings);

            const data = {
                labels: months,
                datasets: [{
                    label: 'Monthly Earnings ($)',
                    data: earnings,
                    borderColor: '#007bff', // Primary Blue
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            };

            new Chart(earningsTrendChartCtx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Last 6 Months Earnings Trend'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
});