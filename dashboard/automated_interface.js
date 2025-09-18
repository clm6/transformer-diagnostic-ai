// TransformIQ Automated Interface - Upload → Click Run → Results
class AutomatedInterface {
    constructor() {
        this.uploadedFiles = [];
        this.currentAnalyses = [];
        this.setupEventListeners();
        this.loadExistingResults();
    }

    setupEventListeners() {
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');

        // File input change
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleFiles(e.dataTransfer.files);
        });

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    handleFiles(files) {
        const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');
        
        if (pdfFiles.length === 0) {
            this.showStatus('Please select PDF files only.', 'error');
            return;
        }

        // Store files for analysis
        this.uploadedFiles = pdfFiles;
        
        // Show analysis control panel
        const analysisPanel = document.getElementById('analysisPanel');
        const uploadedFilesText = document.getElementById('uploadedFiles');
        
        const fileNames = pdfFiles.map(f => f.name).join(', ');
        uploadedFilesText.textContent = `${pdfFiles.length} file(s) ready: ${fileNames}`;
        analysisPanel.style.display = 'block';
        
        this.showStatus(`${pdfFiles.length} PDF file(s) uploaded. Click "Run Analysis" to process automatically.`, 'success');
    }

    async runAutomatedAnalysis() {
        if (!this.uploadedFiles || this.uploadedFiles.length === 0) {
            this.showStatus('No files to analyze', 'error');
            return;
        }

        const runBtn = document.getElementById('runAnalysisBtn');
        runBtn.disabled = true;
        runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        try {
            this.showLoading('Starting automated analysis...');
            this.updateProgressStep(1);

            // First, upload all files
            this.updateLoadingText('Uploading PDF files...');
            for (let i = 0; i < this.uploadedFiles.length; i++) {
                const file = this.uploadedFiles[i];
                await this.processFile(file);
            }

            this.updateProgressStep(2);
            this.updateLoadingText('Running comprehensive analysis...');
            
            // Trigger automated analysis
            const analysisResponse = await fetch('/run-analysis', {
                method: 'POST'
            });

            if (!analysisResponse.ok) {
                throw new Error('Failed to run automated analysis');
            }

            this.updateProgressStep(3);
            this.updateLoadingText('Generating comprehensive reports and CSV exports...');
            
            // Wait for analysis to complete
            await new Promise(resolve => setTimeout(resolve, 3000));

            this.updateProgressStep(4);
            this.updateLoadingText('Loading results...');

            // Reload results
            await this.loadExistingResults();
            
            // Hide analysis panel
            document.getElementById('analysisPanel').style.display = 'none';
            this.uploadedFiles = [];
            
            this.hideLoading();
            this.showStatus('Automated analysis completed! Comprehensive results, CSV exports, and tabular data generated.', 'success');
            
        } catch (error) {
            this.hideLoading();
            this.showStatus(`Analysis failed: ${error.message}`, 'error');
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = '<i class="fas fa-play"></i> Run Analysis';
        }
    }

    async processFile(file) {
        // Upload file to backend for automated processing
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Failed to process ${file.name}: ${response.status}`);
        }

        return await response.json();
    }

    async loadExistingResults() {
        try {
            const response = await fetch('/dashboard-summary');
            if (response.ok) {
                const data = await response.json();
                this.updateDashboard(data);
                
                if (data.equipment_list && data.equipment_list.length > 0) {
                    this.currentAnalyses = data.equipment_list;
                    this.displayResults();
                }
            }
        } catch (error) {
            console.log('Loading existing results...');
        }
    }

    updateDashboard(data) {
        const summary = data.summary || {};
        
        document.getElementById('totalEquipment').textContent = summary.total_equipment || 0;
        document.getElementById('avgHealth').textContent = 
            summary.average_health_score ? `${summary.average_health_score}/100` : '0/100';
        document.getElementById('criticalEquipment').textContent = summary.critical_equipment || 0;
        document.getElementById('highRiskEquipment').textContent = summary.high_risk_equipment || 0;
        document.getElementById('lastUpdated').textContent = 
            summary.last_updated ? `Updated: ${summary.last_updated}` : 'Ready for analysis';
    }

    displayResults() {
        const resultsGrid = document.getElementById('resultsGrid');
        const resultsSection = document.getElementById('resultsSection');
        const resultsCount = document.getElementById('resultsCount');

        if (this.currentAnalyses.length === 0) {
            resultsSection.style.display = 'none';
            return;
        }

        resultsSection.style.display = 'block';
        resultsCount.textContent = `${this.currentAnalyses.length} comprehensive ${this.currentAnalyses.length === 1 ? 'analysis' : 'analyses'}`;
        resultsGrid.innerHTML = '';

        this.currentAnalyses.forEach((analysis, index) => {
            const card = this.createResultCard(analysis, index);
            resultsGrid.appendChild(card);
        });
    }

    createResultCard(analysis, index) {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.onclick = () => this.showAnalysisDetails(analysis);

        const healthScore = analysis.health_score || 0;
        const condition = analysis.condition || 'Unknown';
        const riskLevel = analysis.risk_level || 'Unknown';
        const equipmentName = analysis.equipment_name || `Equipment ${index + 1}`;

        const healthBadgeClass = this.getHealthBadgeClass(healthScore);
        const riskIndicatorClass = this.getRiskIndicatorClass(riskLevel);

        card.innerHTML = `
            <div class="auto-badge"><i class="fas fa-robot"></i></div>
            <div class="result-header">
                <div class="result-title">${equipmentName}</div>
                <div class="health-badge ${healthBadgeClass}">${healthScore}/100</div>
            </div>
            <div class="result-metrics">
                <div class="result-metric">
                    <div class="value">${condition}</div>
                    <div class="label">Condition</div>
                </div>
                <div class="result-metric">
                    <div class="value">${analysis.estimated_remaining_life_years || 'N/A'}</div>
                    <div class="label">Est. Life (Years)</div>
                </div>
            </div>
            <div class="risk-indicator ${riskIndicatorClass}">
                Risk Level: ${riskLevel}
            </div>
        `;

        return card;
    }

    getHealthBadgeClass(score) {
        if (score >= 90) return 'excellent';
        if (score >= 75) return 'good';
        if (score >= 50) return 'fair';
        return 'poor';
    }

    getRiskIndicatorClass(riskLevel) {
        switch (riskLevel.toLowerCase()) {
            case 'low': return 'low';
            case 'moderate': return 'moderate';
            case 'high': return 'high';
            case 'critical': return 'critical';
            default: return 'moderate';
        }
    }

    showAnalysisDetails(analysis) {
        const modal = document.getElementById('analysisModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');

        modalTitle.textContent = `${analysis.equipment_name} - Automated Analysis Results`;
        modalBody.innerHTML = `
            <div class="automation-indicator">Automated Comprehensive Analysis</div>
            
            <div class="analysis-section">
                <h3>Asset Health Overview</h3>
                <div class="analysis-grid">
                    <div class="analysis-item">
                        <div class="label">Health Score</div>
                        <div class="value">${analysis.health_score}/100</div>
                    </div>
                    <div class="analysis-item">
                        <div class="label">Condition</div>
                        <div class="value">${analysis.condition}</div>
                    </div>
                    <div class="analysis-item">
                        <div class="label">Risk Level</div>
                        <div class="value">${analysis.risk_level}</div>
                    </div>
                    <div class="analysis-item">
                        <div class="label">Analysis Date</div>
                        <div class="value">${analysis.analysis_date}</div>
                    </div>
                </div>
            </div>
            
            <div class="analysis-section">
                <h3>Generated Reports</h3>
                <div class="analysis-grid">
                    <div class="analysis-item">
                        <div class="label">JSON Report</div>
                        <div class="value">${analysis.equipment_name}_analysis.json</div>
                    </div>
                    <div class="analysis-item">
                        <div class="label">CSV Export</div>
                        <div class="value">${analysis.equipment_name}_detailed_analysis.csv</div>
                    </div>
                    <div class="analysis-item">
                        <div class="label">Location</div>
                        <div class="value">results/ and csv_exports/ folders</div>
                    </div>
                </div>
            </div>
            
            <div class="analysis-section">
                <h3>CSV Export Features</h3>
                <ul>
                    <li>IEEE-compliant analysis with standards references</li>
                    <li>Risk scoring (1-5 scale) for each component</li>
                    <li>Predictive maintenance planning with timelines</li>
                    <li>Life expectancy forecasting and remaining life calculations</li>
                    <li>ROI scenario comparisons (Repair vs Run-to-Failure vs Replace)</li>
                    <li>V-curve analysis and tap sweep assessment</li>
                    <li>Detailed cost estimates for remediation</li>
                </ul>
            </div>
        `;

        modal.style.display = 'block';
    }

    clearUploadedFiles() {
        this.uploadedFiles = [];
        document.getElementById('analysisPanel').style.display = 'none';
        this.showStatus('Uploaded files cleared', 'success');
    }

    updateProgressStep(step) {
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach((stepEl, index) => {
            if (index < step) {
                stepEl.classList.add('active', 'completed');
            } else if (index === step - 1) {
                stepEl.classList.add('active');
                stepEl.classList.remove('completed');
            } else {
                stepEl.classList.remove('active', 'completed');
            }
        });
    }

    showLoading(message) {
        const overlay = document.getElementById('loadingOverlay');
        const text = document.getElementById('loadingText');
        text.textContent = message;
        overlay.style.display = 'block';
    }

    updateLoadingText(message) {
        const text = document.getElementById('loadingText');
        text.textContent = message;
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = 'none';
        
        // Reset progress steps
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach(step => {
            step.classList.remove('active', 'completed');
        });
    }

    showStatus(message, type) {
        const statusEl = document.getElementById('uploadStatus');
        statusEl.innerHTML = `<p>${message}</p>`;
        statusEl.className = `upload-status ${type}`;
        statusEl.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 5000);
        }
    }
}

// Global functions
let dashboard;

function runAutomatedAnalysis() {
    dashboard.runAutomatedAnalysis();
}

function clearUploadedFiles() {
    dashboard.clearUploadedFiles();
}

function loadResults() {
    dashboard.loadExistingResults();
    dashboard.showStatus('Results refreshed', 'success');
}

function clearAll() {
    if (confirm('Clear all analysis data?')) {
        dashboard.currentAnalyses = [];
        dashboard.displayResults();
        dashboard.updateDashboard({summary: {}});
        dashboard.showStatus('Dashboard cleared', 'success');
    }
}

function closeModal() {
    document.getElementById('analysisModal').style.display = 'none';
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new AutomatedInterface();
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('analysisModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
