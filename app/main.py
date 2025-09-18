#!/usr/bin/env python3
"""
Transformer Analysis Backend API
FastAPI server for generating comprehensive transformer diagnostic reports
Designed for integration with Loveable frontend
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .pdf_parser import extract_text_from_pdf, extract_substation_name, extract_document_date
from .ai_analyzer import TransformerAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="Transformer Analysis Backend",
    description="API for generating comprehensive transformer diagnostic reports",
    version="1.0.0"
)

# Add CORS middleware for Loveable integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer on demand to avoid startup issues
analyzer = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = TransformerAnalyzer()
    return analyzer

# Create necessary directories
UPLOAD_DIR = Path("uploads")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Transformer Analysis Backend API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "active",
            "openai": "configured",
            "file_system": "ready"
        },
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze/upload")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """
    Upload and analyze a TRAX PDF report
    Returns comprehensive diagnostic analysis
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        
        # Save uploaded file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Extract text and metadata
        text = extract_text_from_pdf(str(file_path))
        equipment_name = extract_substation_name(text)
        document_date = extract_document_date(str(file_path), text)
        
        # Generate comprehensive analysis
        analysis = get_analyzer().generate_comprehensive_report(text, equipment_name, document_date)
        
        # Add metadata
        analysis["file_info"] = {
            "original_filename": file.filename,
            "file_id": file_id,
            "upload_timestamp": datetime.now().isoformat(),
            "file_size": len(content)
        }
        
        # Save analysis report to results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        equipment_name = analysis.get('equipment_name', 'Unknown')
        report_filename = f"{equipment_name}_analysis.json"
        report_path = results_dir / report_filename
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Clean up uploaded file (optional)
        os.remove(file_path)
        
        return JSONResponse(content=analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/text")
async def analyze_text_content(data: Dict[str, Any]):
    """
    Analyze transformer data from text content
    Useful for direct data input without file upload
    """
    
    required_fields = ["text", "equipment_name"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    try:
        text = data["text"]
        equipment_name = data["equipment_name"]
        document_date = data.get("document_date", datetime.now().strftime("%Y-%m-%d"))
        
        # Generate comprehensive analysis
        analysis = get_analyzer().generate_comprehensive_report(text, equipment_name, document_date)
        
        # Add metadata
        analysis["file_info"] = {
            "input_type": "text",
            "analysis_timestamp": datetime.now().isoformat(),
            "text_length": len(text)
        }
        
        # Save analysis report to results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        equipment_name = analysis.get('equipment_name', 'Unknown')
        report_filename = f"{equipment_name}_text_analysis.json"
        report_path = results_dir / report_filename
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        return JSONResponse(content=analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/reports")
async def list_reports():
    """List all generated reports"""
    
    try:
        reports = []
        results_dir = Path("results")
        
        if results_dir.exists():
            for report_file in results_dir.glob("*.json"):
                with open(report_file, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        reports.append({
                            "filename": report_file.name,
                            "equipment_name": data.get("equipment_name", "Unknown"),
                            "analysis_date": data.get("analysis_date", "Unknown"),
                            "asset_health_score": data.get("asset_health", {}).get("overall_score", "N/A"),
                            "risk_level": data.get("risk_assessment", {}).get("risk_level", "Unknown")
                        })
                    except json.JSONDecodeError:
                        continue
        
        return {"reports": reports, "count": len(reports)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list reports: {str(e)}")


@app.get("/reports/{file_id}")
async def get_report(file_id: str):
    """Get specific report by file ID"""
    
    # Try different filename patterns
    possible_files = [
        REPORTS_DIR / f"{file_id}_analysis.json",
        REPORTS_DIR / f"{file_id}_text_analysis.json"
    ]
    
    for report_path in possible_files:
        if report_path.exists():
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return JSONResponse(content=data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Report file is corrupted")
    
    raise HTTPException(status_code=404, detail="Report not found")


@app.delete("/reports/clear")
async def clear_all_reports():
    """Clear all analysis reports"""
    
    try:
        results_dir = Path("results")
        
        if not results_dir.exists():
            return {"message": "No reports to clear", "cleared_count": 0}
        
        # Count and remove all JSON files
        json_files = list(results_dir.glob("*.json"))
        cleared_count = len(json_files)
        
        for json_file in json_files:
            json_file.unlink()
        
        return {
            "message": f"Successfully cleared {cleared_count} reports",
            "cleared_count": cleared_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear reports: {str(e)}")


@app.delete("/reports/{equipment_name}")
async def delete_specific_report(equipment_name: str):
    """Delete a specific equipment report"""
    
    try:
        results_dir = Path("results")
        report_files = list(results_dir.glob(f"{equipment_name}*.json"))
        
        if not report_files:
            raise HTTPException(status_code=404, detail=f"No reports found for {equipment_name}")
        
        deleted_count = 0
        for report_file in report_files:
            report_file.unlink()
            deleted_count += 1
        
        return {
            "message": f"Successfully deleted {deleted_count} reports for {equipment_name}",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete reports: {str(e)}")


@app.get("/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary data for visualization"""
    
    try:
        reports = []
        results_dir = Path("results")
        
        if results_dir.exists():
            for report_file in results_dir.glob("*.json"):
                with open(report_file, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if "asset_health" in data:
                            reports.append({
                                "equipment_name": data.get("equipment_name", "Unknown"),
                                "health_score": data.get("asset_health", {}).get("overall_score", 0),
                                "condition": data.get("asset_health", {}).get("condition", "Unknown"),
                                "risk_level": data.get("risk_assessment", {}).get("risk_level", "Unknown"),
                                "critical_issues_count": len(data.get("risk_assessment", {}).get("critical_issues", [])),
                                "analysis_date": data.get("analysis_date", "Unknown")
                            })
                    except json.JSONDecodeError:
                        continue
        
        # Calculate summary statistics
        if reports:
            avg_health = sum(r["health_score"] for r in reports) / len(reports)
            critical_count = len([r for r in reports if r["risk_level"] == "CRITICAL"])
            high_risk_count = len([r for r in reports if r["risk_level"] in ["HIGH", "CRITICAL"]])
        else:
            avg_health = 0
            critical_count = 0
            high_risk_count = 0
        
        return {
            "summary": {
                "total_equipment": len(reports),
                "average_health_score": round(avg_health, 1),
                "critical_equipment": critical_count,
                "high_risk_equipment": high_risk_count
            },
            "equipment_list": reports
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard summary: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
