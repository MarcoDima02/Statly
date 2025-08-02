// Configurazione API
const API_BASE_URL = 'http://localhost:8000/api';

// Elementi DOM
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const selectFileBtn = document.getElementById('selectFileBtn');
const uploadSection = document.getElementById('uploadSection');
const fileInfoSection = document.getElementById('fileInfoSection');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

// Bottoni azione
const analyzeBtn = document.getElementById('analyzeBtn');
const generateReportBtn = document.getElementById('generateReportBtn');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');

// Contenitori risultati
const fileDetails = document.getElementById('fileDetails');
const statsSummary = document.getElementById('statsSummary');
const chartsContainer = document.getElementById('chartsContainer');

// Variabili globali
let currentFile = null;
let analysisResults = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Upload eventi
    selectFileBtn.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag & Drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleFileDrop);
    
    // Bottoni azione
    analyzeBtn.addEventListener('click', analyzeFile);
    generateReportBtn.addEventListener('click', generateReport);
    downloadPdfBtn.addEventListener('click', generateReport);
}

// === GESTIONE FILE ===

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleFileDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    // Validazione tipo file
    if (!file.name.toLowerCase().endsWith('.xlsx') && !file.name.toLowerCase().endsWith('.xls')) {
        showError('Il file deve essere in formato Excel (.xlsx o .xls)');
        return;
    }
    
    // Validazione dimensione (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('Il file è troppo grande. Dimensione massima: 10MB');
        return;
    }
    
    currentFile = file;
    uploadFilePreview(file);
}

async function uploadFilePreview(file) {
    showLoading('Caricamento file in corso...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE_URL}/upload-excel`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore nel caricamento del file');
        }
        
        const data = await response.json();
        displayFileInfo(data);
        showSuccess('File caricato con successo!');
        
    } catch (error) {
        console.error('Errore upload:', error);
        showError(`Errore nel caricamento: ${error.message}`);
    } finally {
        hideLoading();
    }
}

function displayFileInfo(fileData) {
    // Mostra la sezione informazioni file
    fileInfoSection.style.display = 'block';
    
    // Popola i dettagli del file
    fileDetails.innerHTML = `
        <div class="detail-item">
            <span class="detail-label">📁 Nome File:</span>
            <span class="detail-value">${fileData.filename}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">📊 Righe:</span>
            <span class="detail-value">${fileData.rows.toLocaleString()}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">📋 Colonne:</span>
            <span class="detail-value">${fileData.columns}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">🏷️ Nomi Colonne:</span>
            <span class="detail-value">${fileData.column_names.join(', ')}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">❓ Valori Mancanti:</span>
            <span class="detail-value">${fileData.has_missing_values ? '⚠️ Presenti' : '✅ Nessuno'}</span>
        </div>
    `;
    
    // Mostra anteprima dati se disponibile
    if (fileData.preview && fileData.preview.length > 0) {
        fileDetails.innerHTML += `
            <div class="detail-item" style="flex-direction: column; align-items: flex-start;">
                <span class="detail-label">👀 Anteprima Dati (prime 5 righe):</span>
                <div class="preview-table" style="margin-top: 0.5rem; width: 100%; overflow-x: auto;">
                    ${createPreviewTable(fileData.preview, fileData.column_names)}
                </div>
            </div>
        `;
    }
}

function createPreviewTable(previewData, columnNames) {
    let tableHTML = '<table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">';
    
    // Header
    tableHTML += '<thead><tr>';
    columnNames.forEach(col => {
        tableHTML += `<th style="border: 1px solid #ddd; padding: 8px; background: #f8f9fa; text-align: left;">${col}</th>`;
    });
    tableHTML += '</tr></thead>';
    
    // Rows
    tableHTML += '<tbody>';
    previewData.forEach(row => {
        tableHTML += '<tr>';
        columnNames.forEach(col => {
            const value = row[col] !== null && row[col] !== undefined ? row[col] : '-';
            tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${value}</td>`;
        });
        tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table>';
    
    return tableHTML;
}

// === ANALISI DATI ===

async function analyzeFile() {
    if (!currentFile) {
        showError('Nessun file selezionato');
        return;
    }
    
    showLoading('Analisi in corso...');
    
    try {
        const formData = new FormData();
        formData.append('file', currentFile);
        
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore nell\'analisi');
        }
        
        const data = await response.json();
        analysisResults = data.analysis;
        displayAnalysisResults(analysisResults);
        showSuccess('Analisi completata con successo!');
        
    } catch (error) {
        console.error('Errore analisi:', error);
        showError(`Errore nell'analisi: ${error.message}`);
    } finally {
        hideLoading();
    }
}

function displayAnalysisResults(results) {
    // Mostra la sezione risultati
    resultsSection.style.display = 'block';
    
    // Statistiche riassuntive
    displayStatsSummary(results.basic_statistics.dataset_info);
    
    // Grafici
    displayCharts(results.plots);
}

function displayStatsSummary(datasetInfo) {
    statsSummary.innerHTML = `
        <div class="stat-card">
            <h4>Totale Righe</h4>
            <div class="stat-value">${datasetInfo.total_rows.toLocaleString()}</div>
        </div>
        <div class="stat-card">
            <h4>Totale Colonne</h4>
            <div class="stat-value">${datasetInfo.total_columns}</div>
        </div>
        <div class="stat-card">
            <h4>Memoria</h4>
            <div class="stat-value">${datasetInfo.memory_usage}</div>
        </div>
        <div class="stat-card">
            <h4>Valori Mancanti</h4>
            <div class="stat-value">${Object.values(datasetInfo.missing_values).reduce((a, b) => a + b, 0)}</div>
        </div>
    `;
}

function displayCharts(plots) {
    chartsContainer.innerHTML = '';
    
    // Grafici di distribuzione
    if (plots.distributions && plots.distributions.length > 0) {
        plots.distributions.forEach((plotBase64, index) => {
            if (plotBase64) {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-item';
                chartDiv.innerHTML = `
                    <div class="chart-title">Distribuzione Variabile ${index + 1}</div>
                    <img src="data:image/png;base64,${plotBase64}" alt="Grafico distribuzione ${index + 1}">
                `;
                chartsContainer.appendChild(chartDiv);
            }
        });
    }
    
    // Matrice di correlazione
    if (plots.correlation_heatmap) {
        const chartDiv = document.createElement('div');
        chartDiv.className = 'chart-item';
        chartDiv.innerHTML = `
            <div class="chart-title">Matrice di Correlazione</div>
            <img src="data:image/png;base64,${plots.correlation_heatmap}" alt="Matrice di correlazione">
        `;
        chartsContainer.appendChild(chartDiv);
    }
    
    // Grafici temporali
    if (plots.time_series && plots.time_series.length > 0) {
        plots.time_series.forEach((plotBase64, index) => {
            if (plotBase64) {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-item';
                chartDiv.innerHTML = `
                    <div class="chart-title">Andamento Temporale ${index + 1}</div>
                    <img src="data:image/png;base64,${plotBase64}" alt="Grafico temporale ${index + 1}">
                `;
                chartsContainer.appendChild(chartDiv);
            }
        });
    }
    
    // Grafici categorici
    if (plots.categorical && plots.categorical.length > 0) {
        plots.categorical.forEach((plotBase64, index) => {
            if (plotBase64) {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-item';
                chartDiv.innerHTML = `
                    <div class="chart-title">Distribuzione Categorica ${index + 1}</div>
                    <img src="data:image/png;base64,${plotBase64}" alt="Grafico categorico ${index + 1}">
                `;
                chartsContainer.appendChild(chartDiv);
            }
        });
    }
}

// === GENERAZIONE REPORT PDF ===

async function generateReport() {
    if (!currentFile) {
        showError('Nessun file selezionato');
        return;
    }
    
    showLoading('Generazione report PDF in corso...');
    
    try {
        const formData = new FormData();
        formData.append('file', currentFile);
        
        const response = await fetch(`${API_BASE_URL}/generate-report`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore nella generazione del report');
        }
        
        // Download del PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `statly_report_${currentFile.name.split('.')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showSuccess('Report PDF generato e scaricato con successo!');
        
    } catch (error) {
        console.error('Errore generazione report:', error);
        showError(`Errore nella generazione del report: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// === UTILITY FUNCTIONS ===

function showLoading(message = 'Caricamento...') {
    document.getElementById('loadingText').textContent = message;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showError(message) {
    document.getElementById('errorText').textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide dopo 5 secondi
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}

function showSuccess(message) {
    document.getElementById('successText').textContent = message;
    successMessage.style.display = 'block';
    
    // Auto-hide dopo 3 secondi
    setTimeout(() => {
        hideSuccess();
    }, 3000);
}

function hideSuccess() {
    successMessage.style.display = 'none';
}

// === API CONNECTION CHECK ===

async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            console.log('✅ Connessione API attiva');
            return true;
        }
    } catch (error) {
        console.warn('⚠️ API non raggiungibile. Assicurati che il backend sia in esecuzione su ' + API_BASE_URL);
        showError('Backend non raggiungibile. Avvia il server backend su porta 8000.');
        return false;
    }
}

// Controlla connessione all'avvio
window.addEventListener('load', () => {
    setTimeout(checkApiConnection, 1000);
});