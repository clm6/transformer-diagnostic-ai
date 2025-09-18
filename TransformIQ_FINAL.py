#!/usr/bin/env python3
"""
TransformIQ - Final Automated Solution
Simple, reliable, fully automated PDF analysis dashboard
"""

import json
import webbrowser
import os
import shutil
import time
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Import analysis components
from app.pdf_parser import extract_text_from_pdf, extract_substation_name, extract_document_date, extract_equipment_identifiers
from app.ai_analyzer import TransformerAnalyzer

class TransformIQHandler(SimpleHTTPRequestHandler):
    """Simple reliable handler for TransformIQ"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        if self.path == '/':
            self.path = '/automated_interface.html'
        elif self.path == '/dashboard-summary':
            self.serve_dashboard_summary()
            return
        elif self.path == '/health':
            self.serve_health()
            return
        elif self.path == '/run-analysis':
            self.handle_run_analysis()
            return
        
        # Serve static files
        super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        
        if self.path == '/analyze':
            self.handle_automated_analysis()
        elif self.path == '/run-analysis':
            self.handle_run_analysis()
        else:
            self.send_error(404, "Not Found")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        
        if self.path == '/clear':
            self.handle_clear_all()
        else:
            self.send_error(404, "Not Found")
    
    def serve_health(self):
        """Serve health check"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        health_data = json.dumps({
            "status": "healthy",
            "mode": "automated",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.wfile.write(health_data.encode('utf-8'))
    
    def serve_dashboard_summary(self):
        """Serve dashboard summary"""
        
        try:
            results_dir = Path("../results")
            reports = []
            
            if results_dir.exists():
                for report_file in results_dir.glob("*.json"):
                    try:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        if "asset_health" in data:
                            health_score = data.get("asset_health", {}).get("overall_score", 0)
                            
                            # Handle different score formats
                            if isinstance(health_score, str):
                                try:
                                    health_score = float(health_score)
                                except:
                                    health_score = 0
                            
                            # Return the complete analysis data for comprehensive display
                            reports.append({
                                "equipment_name": data.get("equipment_name", "Unknown"),
                                "health_score": health_score,
                                "condition": data.get("asset_health", {}).get("condition", "Unknown"),
                                "risk_level": data.get("risk_assessment", {}).get("risk_level", "Unknown"),
                                "critical_issues_count": len(data.get("risk_assessment", {}).get("critical_issues", [])),
                                "analysis_date": data.get("analysis_date", "Unknown"),
                                "estimated_remaining_life_years": data.get("asset_health", {}).get("estimated_remaining_life_years", "N/A"),
                                "automated": True,
                                # Include complete analysis data for detailed view
                                "asset_health": data.get("asset_health", {}),
                                "risk_assessment": data.get("risk_assessment", {}),
                                "financial_analysis": data.get("financial_analysis", {}),
                                "technical_analysis": data.get("technical_analysis", {}),
                                "executive_summary": data.get("executive_summary", ""),
                                "maintenance_recommendations": data.get("maintenance_recommendations", [])
                            })
                    except (json.JSONDecodeError, Exception) as e:
                        print(f"Error loading {report_file}: {e}")
                        continue
            
            # Calculate summary
            if reports:
                valid_scores = [r["health_score"] for r in reports if isinstance(r["health_score"], (int, float))]
                avg_health = sum(valid_scores) / len(valid_scores) if valid_scores else 0
                critical_count = len([r for r in reports if r["risk_level"] == "CRITICAL"])
                high_risk_count = len([r for r in reports if r["risk_level"] in ["HIGH", "CRITICAL"]])
            else:
                avg_health = 0
                critical_count = 0
                high_risk_count = 0
            
            summary_data = {
                "summary": {
                    "total_equipment": len(reports),
                    "average_health_score": round(avg_health, 1),
                    "critical_equipment": critical_count,
                    "high_risk_equipment": high_risk_count,
                    "last_updated": time.strftime("%H:%M:%S")
                },
                "equipment_list": reports
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = json.dumps(summary_data, indent=2)
            self.wfile.write(response_data.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Dashboard error: {str(e)}")
    
    def handle_automated_analysis(self):
        """Handle automated PDF analysis"""
        
        try:
            print("🤖 AUTOMATED ANALYSIS TRIGGERED")
            
            # Simple approach: save the uploaded file and analyze it
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No file data")
                return
            
            # Read the raw data
            raw_data = self.rfile.read(content_length)
            
            # Extract PDF data from multipart (simplified)
            # Find the PDF content between boundary markers
            if b'Content-Type: application/pdf' in raw_data:
                # Find start of PDF data
                pdf_start = raw_data.find(b'%PDF-')
                if pdf_start != -1:
                    # Find end of PDF data (look for %%EOF or boundary)
                    pdf_end = raw_data.find(b'%%EOF', pdf_start)
                    if pdf_end != -1:
                        pdf_end += 5  # Include %%EOF
                        pdf_data = raw_data[pdf_start:pdf_end]
                        
                        # Save and analyze
                        self.process_pdf_data(pdf_data, "uploaded_transformer.pdf")
                        return
            
            self.send_error(400, "Invalid PDF data")
            
        except Exception as e:
            print(f"❌ Automated analysis error: {e}")
            self.send_error(500, f"Analysis failed: {str(e)}")
    
    def process_pdf_data(self, pdf_data, filename):
        """Process PDF data and run automated analysis"""
        
        try:
            # Save PDF to pdfs folder
            pdfs_dir = Path("../pdfs")
            pdfs_dir.mkdir(exist_ok=True)
            
            pdf_path = pdfs_dir / filename
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
            
            print(f"💾 PDF saved: {pdf_path}")
            
            # Run automated analysis
            analyzer = TransformerAnalyzer()
            
            text = extract_text_from_pdf(str(pdf_path))
            equipment_name = extract_substation_name(text)
            document_date = extract_document_date(str(pdf_path), text)
            
            print(f"📍 Equipment: {equipment_name}")
            
            analysis = analyzer.generate_comprehensive_report(text, equipment_name, document_date)
            
            # Save analysis
            results_dir = Path("../results")
            results_dir.mkdir(exist_ok=True)
            
            report_path = results_dir / f"{equipment_name}_analysis.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Automated analysis complete: {equipment_name}")
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            result = {
                "success": True,
                "message": f"Automated analysis completed for {equipment_name}",
                "equipment_name": equipment_name,
                "health_score": analysis.get("asset_health", {}).get("overall_score", 0),
                "automated": True
            }
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
            self.send_error(500, f"Processing failed: {str(e)}")
    
    def handle_clear_all(self):
        """Clear all data"""
        
        try:
            # Clear results
            results_dir = Path("../results")
            pdfs_dir = Path("../pdfs")
            cleared_count = 0
            
            if results_dir.exists():
                for file in results_dir.glob("*.json"):
                    file.unlink()
                    cleared_count += 1
            
            if pdfs_dir.exists():
                for file in pdfs_dir.glob("*.pdf"):
                    file.unlink()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            result = {
                "message": f"Cleared {cleared_count} analyses",
                "cleared_count": cleared_count
            }
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Clear failed: {str(e)}")
    
    def handle_run_analysis(self):
        """Handle automated analysis execution"""
        
        try:
            print("🚀 RUNNING AUTOMATED ANALYSIS FROM INTERFACE")
            
            # Import analysis functions directly instead of subprocess
            import sys
            import os
            
            # Add parent directory to path to import analyze module
            parent_dir = Path("..").resolve()
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            # Change to parent directory for analysis
            original_cwd = os.getcwd()
            os.chdir(parent_dir)
            
            try:
                # Import and run analysis directly
                from analyze import analyze_all_pdfs
                
                print("📊 Running comprehensive analysis...")
                results = analyze_all_pdfs("pdfs", "results")
                
                print(f"✅ Analysis completed: {len(results)} files processed")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = json.dumps({
                    "success": True,
                    "message": f"Automated analysis completed successfully. Processed {len(results)} files.",
                    "results_count": len(results),
                    "csv_generated": True
                })
                self.wfile.write(response_data.encode('utf-8'))
                
            finally:
                # Restore original working directory
                os.chdir(original_cwd)
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            import traceback
            traceback.print_exc()
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_data = json.dumps({
                "error": f"Analysis failed: {str(e)}",
                "success": False
            })
            self.wfile.write(error_data.encode('utf-8'))

def main():
    """Start TransformIQ automated dashboard"""
    
    print("🤖 TRANSFORMIQ AUTOMATED DASHBOARD")
    print("=" * 50)
    print("🚀 Fully automated PDF analysis")
    print("📱 Professional branding")
    print("⚡ Real-time results")
    print("🔧 No manual steps required!")
    print("=" * 50)
    
    # Change to dashboard directory
    dashboard_dir = Path("dashboard")
    if dashboard_dir.exists():
        os.chdir(dashboard_dir)
    
    # Start server
    server = HTTPServer(('localhost', 3000), TransformIQHandler)
    
    print("✅ TransformIQ ready at: http://localhost:3000")
    print("🤖 Drag PDFs for instant automated analysis!")
    print("=" * 50)
    
    # Open browser
    webbrowser.open("http://localhost:3000")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 TransformIQ stopped")

if __name__ == "__main__":
    main()
