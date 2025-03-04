document.addEventListener('DOMContentLoaded', function() {
    // Parse dates and prepare datasets
    const dates = financialData.map(item => new Date(item.date));
    
    // Major financial stats data
    const totalAssets = financialData.map(item => item.total_asset);
    const totalLiabilities = financialData.map(item => item.total_liability);
    const totalEquities = financialData.map(item => item.total_equity);
    const netIncomes = financialData.map(item => item.net_income);
    
    // Financial ratios data
    const currentRatios = financialData.map(item => item.ratios.current_ratio);
    const debtToEquityRatios = financialData.map(item => item.ratios.debt_to_equity_ratio);
    const returnOnEquities = financialData.map(item => item.ratios.return_on_equity);
    const equityMultipliers = financialData.map(item => item.ratios.equity_multiplier);
    const debtRatios = financialData.map(item => item.ratios.debt_ratio);
    const netProfitMargins = financialData.map(item => item.ratios.net_profit_margin);
    
    // Store chart instances
    const chartInstances = {};
    
    // Find the selected date index to highlight the data point
    let selectedDateIndex = -1;
    if (selectedDate) {
        const selectedDateObj = new Date(selectedDate);
        selectedDateIndex = dates.findIndex(date => 
            date.getFullYear() === selectedDateObj.getFullYear() && 
            date.getMonth() === selectedDateObj.getMonth() && 
            date.getDate() === selectedDateObj.getDate()
        );
    }
    
    // Chart configuration options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    boxWidth: 12,
                    padding: 15
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'MMM yyyy'
                    }
                },
                title: {
                    display: true,
                    text: 'Date'
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)' // Lighter grid lines
                }
            },
            y: {
                title: {
                    display: true
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)' // Lighter grid lines
                }
            }
        },
        // Add a light blue background to the chart area
        backgroundColor: '#f0f8ff',
        // Add point hover styling
        elements: {
            point: {
                radius: (context) => {
                    // Return larger radius for the selected date point
                    const index = context.dataIndex;
                    return index === selectedDateIndex ? 8 : 3;
                },
                hoverRadius: 7,
                backgroundColor: (context) => {
                    // Highlight the selected date point
                    const index = context.dataIndex;
                    return index === selectedDateIndex ? '#FF5733' : context.dataset.borderColor;
                },
                borderWidth: (context) => {
                    // Add border to the selected date point
                    const index = context.dataIndex;
                    return index === selectedDateIndex ? 2 : 1;
                },
                borderColor: (context) => {
                    // White border on the selected point for contrast
                    const index = context.dataIndex;
                    return index === selectedDateIndex ? 'white' : context.dataset.borderColor;
                }
            }
        }
    };
    
    // Function to create major financial stats chart
    function createMajorFinancialStatsChart() {
        if (chartInstances['majorFinancialStats']) {
            chartInstances['majorFinancialStats'].destroy();
        }
        
        chartInstances['majorFinancialStats'] = new Chart(document.getElementById('majorFinancialStats'), {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Total Assets',
                        data: totalAssets,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1,
                        pointRadius: (ctx) => ctx.dataIndex === selectedDateIndex ? 8 : 3,
                        pointHoverRadius: 7,
                        pointBackgroundColor: (ctx) => ctx.dataIndex === selectedDateIndex ? '#FF5733' : 'rgb(75, 192, 192)'
                    },
                    {
                        label: 'Total Liabilities',
                        data: totalLiabilities,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1,
                        pointRadius: (ctx) => ctx.dataIndex === selectedDateIndex ? 8 : 3,
                        pointHoverRadius: 7,
                        pointBackgroundColor: (ctx) => ctx.dataIndex === selectedDateIndex ? '#FF5733' : 'rgb(255, 99, 132)'
                    },
                    {
                        label: 'Total Equity',
                        data: totalEquities,
                        borderColor: 'rgb(153, 102, 255)',
                        tension: 0.1,
                        pointRadius: (ctx) => ctx.dataIndex === selectedDateIndex ? 8 : 3,
                        pointHoverRadius: 7,
                        pointBackgroundColor: (ctx) => ctx.dataIndex === selectedDateIndex ? '#FF5733' : 'rgb(153, 102, 255)'
                    },
                    {
                        label: 'Net Income',
                        data: netIncomes,
                        borderColor: 'rgb(255, 159, 64)',
                        tension: 0.1,
                        pointRadius: (ctx) => ctx.dataIndex === selectedDateIndex ? 8 : 3,
                        pointHoverRadius: 7,
                        pointBackgroundColor: (ctx) => ctx.dataIndex === selectedDateIndex ? '#FF5733' : 'rgb(255, 159, 64)'
                    }
                ]
            },
            options: {
                ...commonOptions,
                plugins: {
                    title: {
                        display: false  // Title now handled by carousel
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    ...commonOptions.scales,
                    y: {
                        ...commonOptions.scales.y,
                        title: {
                            display: true,
                            text: 'Value (USD)'
                        }
                    }
                }
            }
        });
    }
    
    // Function to create ratio charts
    function createRatioChart(canvasId, title, data, color) {
        if (chartInstances[canvasId]) {
            chartInstances[canvasId].destroy();
        }
        
        // Create a proper background color with better opacity
        const backgroundColor = color.replace('rgb', 'rgba').replace(')', ', 0.2)');
        
        chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: title,
                    data: data,
                    borderColor: color,
                    backgroundColor: backgroundColor,
                    fill: true,
                    tension: 0.1,
                    pointRadius: (ctx) => ctx.dataIndex === selectedDateIndex ? 8 : 3,
                    pointHoverRadius: 7,
                    pointBackgroundColor: (ctx) => ctx.dataIndex === selectedDateIndex ? '#FF5733' : color
                }]
            },
            options: {
                ...commonOptions,
                plugins: {
                    title: {
                        display: false  // Title now handled by carousel
                    }
                },
                scales: {
                    ...commonOptions.scales,
                    y: {
                        ...commonOptions.scales.y,
                        title: {
                            display: true,
                            text: 'Ratio'
                        }
                    }
                }
            }
        });
    }
    
    // Mapping of slide index to chart creation function
    const chartCreators = [
        () => createMajorFinancialStatsChart(),
        () => createRatioChart('currentRatio', 'Current Ratio', currentRatios, 'rgb(54, 162, 235)'),
        () => createRatioChart('debtToEquityRatio', 'Debt to Equity Ratio', debtToEquityRatios, 'rgb(255, 99, 132)'),
        () => createRatioChart('returnOnEquity', 'Return on Equity', returnOnEquities, 'rgb(75, 192, 192)'),
        () => createRatioChart('equityMultiplier', 'Equity Multiplier', equityMultipliers, 'rgb(153, 102, 255)'),
        () => createRatioChart('debtRatio', 'Debt Ratio', debtRatios, 'rgb(255, 159, 64)'),
        () => createRatioChart('netProfitMargin', 'Net Profit Margin', netProfitMargins, 'rgb(255, 205, 86)')
    ];
    
    // Carousel functionality
    function initCarousel() {
        const prevBtn = document.getElementById('prevChart');
        const nextBtn = document.getElementById('nextChart');
        const slides = document.querySelectorAll('.carousel-slide');
        const dots = document.querySelectorAll('.dot');
        const chartTitle = document.getElementById('chartTitle');
        let currentIndex = 0;
        let chartsInitialized = [false, false, false, false, false, false, false];
        
        // Function to update carousel
        function updateCarousel(index) {
            // Hide all slides and deactivate all dots
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            // Show current slide and activate current dot
            slides[index].classList.add('active');
            dots[index].classList.add('active');
            
            // Update chart title
            chartTitle.textContent = slides[index].getAttribute('data-title');
            
            // Initialize chart if not already done
            if (!chartsInitialized[index]) {
                // Small delay to ensure the canvas is visible
                setTimeout(() => {
                    chartCreators[index]();
                    chartsInitialized[index] = true;
                }, 50);
            }
            
            currentIndex = index;
        }
        
        // Previous button click
        prevBtn.addEventListener('click', () => {
            const newIndex = currentIndex === 0 ? slides.length - 1 : currentIndex - 1;
            updateCarousel(newIndex);
        });
        
        // Next button click
        nextBtn.addEventListener('click', () => {
            const newIndex = currentIndex === slides.length - 1 ? 0 : currentIndex + 1;
            updateCarousel(newIndex);
        });
        
        // Dot clicks
        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                const index = parseInt(dot.getAttribute('data-index'));
                updateCarousel(index);
            });
        });
        
        // Initialize first slide
        updateCarousel(0);
    }
    
    // Initialize the carousel
    initCarousel();
}); 