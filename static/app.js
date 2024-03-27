document.addEventListener('DOMContentLoaded', function() {
    fetchKeyDistribution();
    fetchNodeDetails();
    fetchSystemStats();
    fetchNodeData();
    setInterval(fetchKeyDistribution, 5000); // Refresh every 5 seconds
    setInterval(fetchNodeDetails, 5000); // Refresh every 5 seconds
    setInterval(fetchNodeData, 5000); // Refresh every 5 seconds
    setInterval(fetchSystemStats, 10000); // Refresh every 10 seconds
});

function fetchKeyDistribution() {
    const ctx = document.getElementById('keyDistributionChart').getContext('2d');
    fetch('/key-distribution')
        .then(response => response.json())
        .then(data => {
            const chartData = {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Number of Keys',
                    data: Object.values(data),
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            };
            const chartOptions = {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            };
            new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: chartOptions
            });
        })
        .catch(error => console.error('Error fetching key distribution:', error));
}

function fetchNodeDetails() {
    const nodeInfoDiv = document.getElementById('nodeInfo');
    fetch('/health')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            nodeInfoDiv.innerHTML = ''; // Clear previous content
            Object.entries(data).forEach(([node, status]) => {
                const infoElement = document.createElement('p');
                infoElement.textContent = `${node}: ${status}`;
                nodeInfoDiv.appendChild(infoElement);
            });
        })
        .catch(error => {
            console.error('Error fetching node details:', error);
            nodeInfoDiv.textContent = 'Failed to load node details.';
        });
}

function fetchNodeData() {
    fetch('/all')
        .then(response => response.json())
        .then(nodesData => {
            const nodeDataSection = document.getElementById('nodeData');
            nodeDataSection.innerHTML = ''; // Clear previous content

            Object.entries(nodesData).forEach(([nodeUrl, keyValues], index) => {
                // Create a table for each node
                const table = document.createElement('table');
                table.id = `nodeTable${index}`;
                table.innerHTML = `<caption>Node: ${nodeUrl}</caption><tr><th>Key</th><th>Value</th></tr>`;

                // Populate the table with key-value pairs
                Object.entries(keyValues).forEach(([key, value]) => {
                    const row = table.insertRow(-1);
                    const keyCell = row.insertCell(0);
                    const valueCell = row.insertCell(1);
                    keyCell.textContent = key;
                    valueCell.textContent = value;
                });

                // Append the table to the section
                nodeDataSection.appendChild(table);
            });
        })
        .catch(error => console.error('Error fetching node key-value data:', error));
}

function fetchSystemStats() {
    const systemStatsDiv = document.getElementById('systemStats');
    fetch('/system-stats')
        .then(response => response.json())
        .then(data => {
            systemStatsDiv.innerHTML = ''; // Clear previous content
            const totalKeysElement = document.createElement('p');
            totalKeysElement.textContent = `Total Keys: ${data.total_keys}`;
            systemStatsDiv.appendChild(totalKeysElement);

            const totalSizeElement = document.createElement('p');
            totalSizeElement.textContent = `Total Size: ${data.total_size} bytes`;
            systemStatsDiv.appendChild(totalSizeElement);
        })
        .catch(error => console.error('Error fetching system stats:', error));
}
