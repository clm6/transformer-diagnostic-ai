# 🤖 TransformIQ - Automated Transformer Analysis Platform

**Professional AI-Powered Transformer Diagnostic Analysis with Automated Dashboard**

TransformIQ is a comprehensive transformer analysis platform that provides automated PDF processing, AI-powered diagnostics, and professional dashboard visualization for transformer health assessment.

## ✨ Key Features

- **🤖 Fully Automated Analysis**: Upload PDFs → Automatic AI analysis → Instant comprehensive results
- **🎨 Professional Branding**: Corporate TransformIQ styling with custom color scheme
- **📊 Comprehensive Reports**: Health scoring, risk assessment, financial analysis, and maintenance recommendations
- **📋 Detailed Tabular Data**: IEEE-compliant analysis with predictive maintenance planning
- **📈 CSV Export**: Professional tabular format for Excel, Power BI, and Tableau integration
- **🌐 Modern Dashboard**: Real-time visualization with professional interface
- **⚡ Enhanced Analysis**: Detailed technical analysis with IEEE references and cost estimates

## 🏗️ Project Structure

```
transformer-analysis-backend/
├── dashboard/                   # 🌐 Professional web dashboard
│   ├── comprehensive_dashboard.html  # Main dashboard (WORKING)
│   ├── styles.css              # TransformIQ professional styling
│   └── script.js               # Dashboard functionality
├── pdfs/                       # 📁 PDF input folder (auto-populated)
├── results/                    # 💾 Analysis results (JSON files)
├── csv_exports/                # 📈 CSV tabular data exports
├── app/                        # 🔧 Core analysis engine
│   ├── main.py                 # FastAPI server
│   ├── ai_analyzer.py          # Enhanced AI analysis engine
│   ├── csv_exporter.py         # CSV export functionality
│   └── pdf_parser.py           # PDF text extraction
├── analyze.py                  # 📄 Enhanced analysis script with CSV export
├── export_csv.py               # 📊 Standalone CSV export utility
├── TransformIQ_FINAL.py       # 🚀 Automated dashboard server
├── TransformIQ_AUTO.bat       # 🖱️ Windows launcher
├── requirements.txt            # 📦 Dependencies
└── README.md                   # 📚 This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch TransformIQ Dashboard
```bash
# Start the automated dashboard
python TransformIQ_FINAL.py

# Or on Windows, double-click:
TransformIQ_AUTO.bat
```

### 3. Use the Enhanced Dashboard
1. **Dashboard opens** at `http://localhost:3000`
2. **Upload PDFs** by dragging to the upload area
3. **Run enhanced analysis** with `python analyze.py` (includes CSV export)
4. **Load results** by clicking "Load Data" button
5. **View comprehensive analysis** by clicking any equipment card
6. **Access CSV data** in `csv_exports/` folder for Excel/Power BI integration

## 🎨 Professional Branding

### TransformIQ Corporate Color Scheme
- **Deep Blue (#1E3A8A)**: Primary branding and headers
- **Electric Blue (#3B82F6)**: Interactive buttons and accents
- **Peach Gradient (#FCA5A5 → #FDBA74)**: Logo and accent elements
- **Purple Accent (#A78BFA)**: Automation indicators
- **Neutral Gray (#374151)**: Professional text content

### Brand Identity
- **TransformIQ Logo**: Custom gradient "T" icon
- **Professional Typography**: Inter font family
- **Clean Interface**: Minimal emojis, corporate-appropriate styling
- **Modern Design**: Professional appearance suitable for enterprise use

## 📊 Enhanced Analysis Features

### Dashboard Metrics
- **Total Equipment**: Count of analyzed transformers
- **Average Health Score**: Fleet health indicator (0-100 scale)
- **Critical Equipment**: Immediate attention alerts
- **High Risk Equipment**: Priority monitoring count

### Comprehensive Analysis Results
Each analysis provides detailed data:
- **Asset Health Score** (0-100) with component breakdown
- **Risk Assessment** (LOW/MODERATE/HIGH/CRITICAL) with 1-5 risk scoring
- **Financial Impact Analysis** with ROI scenario comparisons
- **Component Health Scores** (Windings, Insulation, Bushings, etc.)
- **Executive Summary** for management
- **Maintenance Recommendations** with priority and timeframes
- **Technical Analysis** with IEEE references and standards compliance

### Enhanced Tabular Data Export
**Detailed CSV format includes:**
- **Date & Test Type**: Comprehensive test documentation
- **Measurement Points**: Specific test locations and values
- **IEEE References**: Standards compliance and correction factors
- **Risk Analysis**: Detailed risk assessment with 1-5 scoring
- **Predictive Maintenance**: Specific action plans with timelines
- **Life Expectancy**: Forecasting with remaining life calculations
- **ROI Scenarios**: Cost-benefit analysis (Repair vs Run-to-Failure vs Replace)
- **V-Curve Analysis**: Tap sweep assessment and balance analysis
- **Cost Estimates**: Detailed remediation cost breakdowns

### Professional Display
- **Equipment Cards**: Visual summary with health scores and risk levels
- **Detailed Analysis Modal**: Click any card for comprehensive analysis
- **Color-coded Health**: Green (excellent) to Red (critical)
- **Risk Indicators**: Professional risk level visualization
- **Data Management**: Clear all and individual analysis management

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Dashboard interface
- `GET /dashboard-summary` - Comprehensive dashboard data
- `POST /analyze` - Automated PDF analysis
- `DELETE /clear` - Clear all analyses
- `GET /health` - System health check

### API Documentation
Interactive API docs available when running the FastAPI server separately

## 🤖 Automated Workflow

### Simple 3-Step Process
1. **Start TransformIQ**: `python TransformIQ_FINAL.py`
2. **Upload PDFs**: Drag transformer reports to dashboard
3. **Run Analysis**: Execute `python analyze.py` → Click "Load Data"

### What Happens Automatically
- **PDF Upload** → Files saved to `pdfs/` folder automatically
- **Analysis Execution** → Run `python analyze.py` for batch processing
- **Results Loading** → Click "Load Data" to display comprehensive analysis
- **Dashboard Update** → Real-time metrics and equipment cards
- **Detailed View** → Click cards for complete analysis modal

## 📈 Analysis Capabilities

### Health Assessment
- **Overall Health Score**: 0-100 scale with component breakdown
- **Condition Rating**: Excellent/Good/Fair/Poor classification
- **Remaining Life**: Estimated years of service life
- **Component Scores**: Individual component health assessment

### Risk Analysis
- **Risk Level**: LOW/MODERATE/HIGH/CRITICAL classification
- **Critical Issues**: Immediate attention items
- **Immediate Actions**: Actions needed within 30 days
- **Near-term Actions**: Actions needed within 6 months

### Financial Analysis
- **Investment Required**: Immediate maintenance costs
- **Failure Cost Avoidance**: Potential savings from preventive action
- **ROI Percentage**: Return on investment calculations

### Technical Analysis
- **Winding Resistance**: LV/HV winding condition assessment
- **Turns Ratio**: Accuracy and excitation current analysis
- **Tan Delta**: Power factor analysis with thresholds
- **Bushing Analysis**: Individual bushing power factor assessment

## 💻 Integration

### For Loveable Projects
The dashboard can be easily integrated into Loveable applications:
- **Modern HTML/CSS/JS**: Standard web technologies
- **Professional Styling**: Corporate-ready appearance
- **Responsive Design**: Works on all devices
- **API-ready**: Backend available for custom integrations

### For Enterprise Use
- **Professional Appearance**: Suitable for management presentations
- **Comprehensive Data**: Complete technical and financial analysis
- **Standards Compliance**: IEEE and NERC compliant analysis
- **Audit Trail**: Complete analysis documentation

## 🔧 Configuration

### Environment
- **Python 3.7+**: Required for analysis engine
- **OpenAI API Key**: Configured in `.env` file
- **Web Browser**: For dashboard interface

### File Management
- **Input**: PDFs uploaded via dashboard (saved to `pdfs/` folder)
- **Processing**: Run `python analyze.py` for batch analysis
- **Output**: JSON reports saved to `results/` folder
- **Visualization**: Dashboard displays comprehensive analysis

## 🎯 Current Status

### ✅ Working Features
- **Professional Dashboard**: TransformIQ branded interface
- **PDF Upload**: Drag & drop functionality
- **Comprehensive Analysis**: Complete health, risk, and financial assessment
- **Data Management**: Clear all and individual analysis management
- **Professional Display**: Corporate-styled results visualization

### 📊 Sample Analysis Results
- **Substation_15**: 85/100 health score, Good condition, MODERATE risk
- **Substation_2**: 75/100 health score, Fair condition, MODERATE risk
- **Average Fleet Health**: 80/100
- **Critical Equipment**: 0 (no immediate failures)

## 🚀 Getting Started

### Quick Launch
```bash
# Start TransformIQ
python TransformIQ_FINAL.py

# Dashboard opens at: http://localhost:3000
# Upload PDFs → Run analysis → View comprehensive results
```

### Analysis Workflow
1. **Upload**: Drag PDFs to dashboard upload area
2. **Process**: Run `python analyze.py` in terminal
3. **View**: Click "Load Data" to display comprehensive analysis
4. **Details**: Click any equipment card for complete analysis

## 📈 CSV Export Features

### Detailed Tabular Data
Each analysis generates comprehensive CSV files with:
- **IEEE-Compliant Analysis**: Standards references and correction factors
- **Risk Scoring**: 1-5 scale risk assessment for each component
- **Predictive Maintenance**: Specific action plans with timelines
- **Life Expectancy**: Forecasting with remaining life calculations
- **ROI Analysis**: Cost-benefit scenarios (Repair/Run-to-Failure/Replace)
- **V-Curve Assessment**: Tap sweep and balance analysis
- **Cost Estimates**: Detailed remediation cost breakdowns

### Export Formats
- **Individual CSV**: Detailed analysis per transformer
- **Master CSV**: Combined analysis for fleet management
- **Excel Ready**: Professional tabular format
- **BI Integration**: Power BI and Tableau compatible

### CSV Generation
```bash
# Automatic CSV export with analysis
python analyze.py

# Or export existing analyses
python export_csv.py
```

## 🎉 Production Ready

TransformIQ provides enterprise-grade transformer analysis with:
- **Professional Interface**: Corporate branding and styling
- **Enhanced Analysis**: IEEE-compliant detailed technical assessment
- **CSV Export**: Professional tabular data for business intelligence
- **Automated Workflow**: Streamlined PDF processing with comprehensive output
- **Management Dashboard**: Executive-ready visualization
- **Standards Compliance**: IEEE and NERC aligned analysis with detailed references

**TransformIQ delivers comprehensive transformer diagnostics with professional presentation and detailed tabular data suitable for enterprise deployment.** 🚀