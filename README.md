# Neural Edge Research - TransformIQ Analysis Platform

**Professional AI-Powered Transformer Diagnostic Analysis System**

Neural Edge Research presents TransformIQ, an enterprise-grade transformer analysis platform that provides automated PDF processing, AI-powered diagnostics, and professional dashboard visualization for critical infrastructure asset health assessment.

## Overview

TransformIQ delivers comprehensive transformer analysis with IEEE C57.152 compliant health indexing, automated equipment identifier extraction, and detailed tabular data export for enterprise asset management.

### Key Capabilities

- **Automated Analysis Pipeline**: PDF upload with one-click analysis execution
- **IEEE C57.152 Health Index**: Standards-compliant scoring with component risk assessment
- **Equipment Identifier Extraction**: Automatic detection of serial numbers, manufacturer data, and specifications
- **Professional Dashboard**: Corporate-styled interface with real-time visualization
- **Comprehensive CSV Export**: Detailed tabular data for business intelligence integration
- **Cybersecurity Focus**: Secure API key management and data protection

## Architecture

```
transformer-analysis-backend/
├── dashboard/                  # Web interface
├── app/                       # Core analysis engine
├── pdfs/                      # PDF input directory
├── results/                   # JSON analysis output
├── csv_exports/               # CSV tabular data
├── analyze.py                 # Analysis execution script
├── TransformIQ_FINAL.py      # Dashboard server
└── requirements.txt           # Dependencies
```

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Valid OpenAI API key
- Web browser for dashboard interface

### Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: Copy `env.template` to `.env` and add your API key
3. Launch TransformIQ: `python TransformIQ_FINAL.py`

### Usage
1. Access dashboard at http://localhost:3000
2. Upload transformer PDFs via drag and drop
3. Click "Run Analysis" button
4. Review comprehensive results in dashboard
5. Access CSV exports in csv_exports/ directory

## Security

### API Key Management
- Environment variables stored in .env file (not tracked in version control)
- Template configuration provides secure setup guidance
- Local server deployment with configurable access restrictions

### Data Protection
- Local processing with controlled data access
- Secure storage of analysis results
- Privacy compliance with minimal external data transmission

## Technical Specifications

### Analysis Engine
- AI Model: OpenAI GPT-4 with transformer diagnostics specialization
- Standards Compliance: IEEE C57.152, IEEE C57.12.90, NERC PRC-005-6
- Processing: Automated workflow with comprehensive error handling

### Output Formats
- JSON reports with complete technical analysis
- CSV exports with detailed tabular data
- Professional dashboard visualization

---

**Neural Edge Research - TransformIQ Platform**  
*Professional Transformer Analysis for Critical Infrastructure*
