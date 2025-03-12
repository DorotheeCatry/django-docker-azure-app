document.addEventListener("DOMContentLoaded", function () {
    // Vérification des données
    console.log("Loan Dates:", loanDates);
    console.log("Loan Amounts:", loanAmounts);
    console.log("Approved:", approvedCount, "Pending:", pendingCount, "Rejected:", rejectedCount);

    // Vérification si les éléments existent avant d'exécuter Chart.js
    const trendsCanvas = document.getElementById('loanTrendsChart');
    const distributionCanvas = document.getElementById('loanDistributionChart');

    if (trendsCanvas) {
        const trendsCtx = trendsCanvas.getContext('2d');
        new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: loanDates,
                datasets: [{
                    label: 'Loan Amount',
                    data: loanAmounts,
                    borderColor: '#C9A05F',
                    backgroundColor: 'rgba(201, 160, 95, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } else {
        console.error("Element loanTrendsChart introuvable.");
    }

    if (distributionCanvas) {
        const distributionCtx = distributionCanvas.getContext('2d');
        new Chart(distributionCtx, {
            type: 'doughnut',
            data: {
                labels: ['Approved', 'Pending', 'Rejected'],
                datasets: [{
                    data: [approvedCount, pendingCount, rejectedCount],
                    backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                cutout: '70%'
            }
        });
    } else {
        console.error("Element loanDistributionChart introuvable.");
    }
});
