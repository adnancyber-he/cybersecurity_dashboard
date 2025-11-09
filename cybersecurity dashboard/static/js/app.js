let currentScanId = null;

async function performScan() {
    const url = document.getElementById('url-input').value;
    if (!url) {
        alert('Please enter a URL');
        return;
    }

    document.getElementById('scan-btn').disabled = true;
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
            currentScanId = data.id; // Assuming the response includes scan ID
        } else {
            alert('Scan failed: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('scan-btn').disabled = false;
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResults(data) {
    document.getElementById('results').style.display = 'block';

    // Risk Score
    const riskScore = data.risk_score || 0;
    document.getElementById('risk-score').textContent = riskScore;
    document.getElementById('risk-bar').style.width = `${riskScore}%`;

    // Headers
    const headersResult = document.getElementById('headers-result');
    if (data.headers.error) {
        headersResult.innerHTML = `<p style="color: #ff0040;">Error: ${data.headers.error}</p>`;
    } else {
        headersResult.innerHTML = `
            <p>Missing Headers: ${data.headers.missing_headers.join(', ') || 'None'}</p>
            <p>Present Headers: ${Object.keys(data.headers.present_headers).join(', ') || 'None'}</p>
        `;
    }

    // SSL
    const sslResult = document.getElementById('ssl-result');
    if (data.ssl.error) {
        sslResult.innerHTML = `<p style="color: #ff0040;">Error: ${data.ssl.error}</p>`;
    } else {
        sslResult.innerHTML = `
            <p>Valid: ${data.ssl.valid ? 'Yes' : 'No'}</p>
            <p>Cipher: ${data.ssl.cipher ? data.ssl.cipher[0] : 'N/A'}</p>
        `;
    }

    // Ports
    const portsResult = document.getElementById('ports-result');
    if (data.ports.error) {
        portsResult.innerHTML = `<p style="color: #ff0040;">Error: ${data.ports.error}</p>`;
    } else {
        portsResult.innerHTML = `
            <p>Open Ports: ${data.ports.open_ports.length}</p>
            <ul>${data.ports.open_ports.map(p => `<li>${p.port}/${p.protocol} - ${p.service}</li>`).join('')}</ul>
        `;
    }

    // Cookies
    const cookiesResult = document.getElementById('cookies-result');
    if (data.cookies.error) {
        cookiesResult.innerHTML = `<p style="color: #ff0040;">Error: ${data.cookies.error}</p>`;
    } else {
        cookiesResult.innerHTML = `
            <p>Server: ${data.cookies.server_info}</p>
            <p>Insecure Cookies: ${data.cookies.insecure_cookies.length}</p>
            <ul>${data.cookies.insecure_cookies.map(c => `<li>${c.name}</li>`).join('')}</ul>
        `;
    }

    // Chart
    createChart(data);
}

function createChart(data) {
    const ctx = document.getElementById('vulnerabilityChart').getContext('2d');
    const vulnerabilities = [
        data.headers.missing_headers ? data.headers.missing_headers.length : 0,
        data.ssl.valid ? 0 : 1,
        data.ports.open_ports ? data.ports.open_ports.length : 0,
        data.cookies.insecure_cookies ? data.cookies.insecure_cookies.length : 0
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Missing Headers', 'SSL Issues', 'Open Ports', 'Insecure Cookies'],
            datasets: [{
                label: 'Vulnerabilities',
                data: vulnerabilities,
                backgroundColor: ['#ff0040', '#ffa500', '#00bfff', '#00ff41'],
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function showHistory() {
    try {
        const response = await fetch('/history');
        const scans = await response.json();

        const historyList = document.getElementById('history-list');
        historyList.innerHTML = scans.map(scan => `
            <div class="history-item">
                <p><strong>URL:</strong> ${scan.url}</p>
                <p><strong>Date:</strong> ${new Date(scan.timestamp).toLocaleString()}</p>
                <p><strong>Risk Score:</strong> ${scan.results.risk_score}/100</p>
                <button onclick="loadScan(${scan.id})">View Details</button>
            </div>
        `).join('');

        document.getElementById('history-modal').style.display = 'block';
    } catch (error) {
        alert('Error loading history: ' + error.message);
    }
}

function closeHistory() {
    document.getElementById('history-modal').style.display = 'none';
}

function loadScan(scanId) {
    // Load specific scan details (simplified)
    alert('Loading scan details for ID: ' + scanId);
    closeHistory();
}

async function exportReport() {
    if (!currentScanId) {
        alert('No scan to export');
        return;
    }

    try {
        const response = await fetch(`/export/${currentScanId}`);
        const data = await response.json();
        alert('PDF exported: ' + data.filename);
    } catch (error) {
        alert('Export failed: ' + error.message);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('history-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
