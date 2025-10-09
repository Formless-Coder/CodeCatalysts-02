document.addEventListener('DOMContentLoaded', () => {
    const mainContent = document.getElementById('main-content');
    const navLinks = document.querySelectorAll('.nav-link');

    // Make sure these paths match your file names in the 'components' folder
    const routes = {
        '': 'components/dashboard.html',
        '#dashboard': 'components/dashboard.html',
        '#upload': 'components/uploadpage.html',
        '#calendar': 'components/calendarpage.html',
        '#audit': 'components/auditpage.html'
    };
    
    // The chart initialization logic for the dashboard
    function initializeDashboardCharts() {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js library is not loaded. Make sure the script tag is in index.html.');
            return;
        }

        // Set global styles for charts
        Chart.defaults.color = '#a0aec0';
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
        
        // Destroy existing chart instances to prevent errors on re-navigation
        if (Chart.getChart('complianceTrendChart')) {
            Chart.getChart('complianceTrendChart').destroy();
        }
        if (Chart.getChart('complianceCategoryChart')) {
            Chart.getChart('complianceCategoryChart').destroy();
        }

        // Draw Trend Chart
        const trendChartEl = document.getElementById('complianceTrendChart');
        if (trendChartEl) {
            new Chart(trendChartEl.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
                    datasets: [{
                        label: 'Compliance Score',
                        data: [88, 90, 85, 92, 95, 93],
                        backgroundColor: 'rgba(20, 209, 192, 0.2)',
                        borderColor: '#14D1C0',
                        borderWidth: 2,
                        pointBackgroundColor: '#14D1C0',
                        pointRadius: 4,
                        tension: 0.4
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { 
                        legend: { display: false } 
                    }, 
                    scales: { 
                        y: { 
                            beginAtZero: false, 
                            min: 75, 
                            max: 100,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    } 
                }
            });
        }

        // Draw Category Chart
        const categoryChartEl = document.getElementById('complianceCategoryChart');
        if (categoryChartEl) {
            new Chart(categoryChartEl.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['On Track', 'Needs Attention', 'Urgent'],
                    datasets: [{
                        label: 'Compliance Status',
                        data: [18, 4, 1],
                        backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'],
                        borderColor: '#0B1120',
                        borderWidth: 4,
                        hoverOffset: 8
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    cutout: '70%', 
                    plugins: { 
                        legend: { 
                            position: 'bottom', 
                            labels: { 
                                padding: 20, 
                                usePointStyle: true, 
                                pointStyle: 'circle' 
                            } 
                        } 
                    } 
                }
            });
        }
    }

    // Function to fetch and display content
    async function loadContent(url) {
        try {
            // Add a timestamp to prevent browser caching issues
            const response = await fetch(`${url}?v=${new Date().getTime()}`);
            if (!response.ok) {
                throw new Error(`Could not find the file at '${url}'. Please check your file structure and names.`);
            }
            
            mainContent.innerHTML = await response.text();

            // After the content is loaded, check if it's the dashboard and run the chart function
            if (url.includes('dashboard.html')) {
                // Add a small delay to ensure DOM elements are rendered
                setTimeout(initializeDashboardCharts, 100);
            }

        } catch (error) {
            mainContent.innerHTML = `
                <div class="text-center py-10 bg-red-900/20 rounded-lg">
                    <h2 class="text-2xl font-bold text-red-400">Error Loading Page</h2>
                    <p class="text-gray-400 mt-2">
                        <strong class="text-red-300">${error.message}</strong>
                    </p>
                    <p class="text-gray-500 mt-4 text-sm">
                        Make sure all component files exist in the 'components' directory.
                    </p>
                </div>
            `;
            console.error("Error details:", error);
        }
    }

    // Function to highlight the active navigation link
    function updateActiveLink(hash) {
        const activeHash = hash || '#dashboard';
        navLinks.forEach(link => {
            if (link.getAttribute('href') === activeHash) {
                link.classList.add('text-white', 'font-semibold');
                link.classList.remove('text-gray-300');
            } else {
                link.classList.remove('text-white', 'font-semibold');
                link.classList.add('text-gray-300');
            }
        });
    }

    // Main router function
    function router() {
        const hash = window.location.hash || '#dashboard';
        const path = routes[hash] || routes['']; 
        if (path) {
            loadContent(path);
            updateActiveLink(hash);
        } else {
            mainContent.innerHTML = `
                <div class="text-center py-10">
                    <h2 class="text-2xl font-bold text-white">Page not found</h2>
                    <p class="text-gray-400 mt-2">The requested page could not be found.</p>
                    <a href="#dashboard" class="text-teal-400 hover:text-teal-300 mt-4 inline-block">Go to Dashboard</a>
                </div>
            `;
        }
    }

    // Listen for hash changes and load initial page
    window.addEventListener('hashchange', router);
    router();

    // Add smooth scrolling for anchor links
    document.addEventListener('click', function(e) {
        if (e.target.matches('a[href^="#"]')) {
            e.preventDefault();
            const targetHash = e.target.getAttribute('href');
            if (routes[targetHash]) {
                window.location.hash = targetHash;
            }
        }
    });
});