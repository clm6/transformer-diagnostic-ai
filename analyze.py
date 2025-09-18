#!/usr/bin/env python3
"""
Main PDF Analysis Script - Default Path Approach
Analyzes transformer PDFs from the 'pdfs' folder for Loveable integration
"""

import json
from pathlib import Path
from datetime import datetime
from app.pdf_parser import extract_text_from_pdf, extract_substation_name, extract_document_date, extract_equipment_identifiers
from app.ai_analyzer import TransformerAnalyzer
from app.csv_exporter import export_analysis_to_csv, create_master_csv

def analyze_pdf_file(pdf_path, output_dir="results"):
    """
    Analyze a single PDF file and generate comprehensive report
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save results
    
    Returns:
        dict: Comprehensive analysis results
    """
    
    print(f"📄 Analyzing PDF: {Path(pdf_path).name}")
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return None
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Extract metadata
        equipment_name = extract_substation_name(text)
        document_date = extract_document_date(pdf_path, text)
        equipment_identifiers = extract_equipment_identifiers(text)
        
        # Initialize AI analyzer
        analyzer = TransformerAnalyzer()
        
        # Generate comprehensive analysis
        analysis = analyzer.generate_comprehensive_report(text, equipment_name, document_date)
        
        # Add extracted equipment identifiers to analysis
        if equipment_identifiers:
            analysis["equipment_identifiers"] = equipment_identifiers
            print(f"   📋 Extracted identifiers: {equipment_identifiers}")
        else:
            # Add default identifiers if none found
            analysis["equipment_identifiers"] = {
                "serial_number": "Not found in document",
                "manufacturer": "Not specified",
                "year_of_manufacture": "Not specified"
            }
        
        # Add file metadata
        analysis["file_info"] = {
            "original_filename": Path(pdf_path).name,
            "file_path": str(pdf_path),
            "analysis_timestamp": datetime.now().isoformat(),
            "text_length": len(text)
        }
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save comprehensive report
        report_filename = f"{equipment_name}_analysis.json"
        report_path = output_path / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Export to CSV format
        try:
            csv_path = export_analysis_to_csv(analysis, output_dir)
            print(f"   ✅ Analysis complete - {equipment_name}")
            print(f"   💾 JSON Report: {report_filename}")
            print(f"   📊 CSV Export: {Path(csv_path).name}")
        except Exception as e:
            print(f"   ✅ Analysis complete - {equipment_name}")
            print(f"   💾 JSON Report: {report_filename}")
            print(f"   ⚠️ CSV export failed: {e}")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing PDF: {str(e)}")
        return None

def analyze_all_pdfs(pdf_directory="./pdfs", output_dir="results"):
    """
    Analyze all PDF files in the default directory
    
    Args:
        pdf_directory (str): Directory containing PDF files
        output_dir (str): Directory to save results
    
    Returns:
        list: List of analysis results
    """
    
    print("🧪 TRANSFORMER PDF ANALYSIS")
    print("=" * 50)
    print(f"📍 PDF Directory: {Path(pdf_directory).absolute()}")
    print(f"💾 Output Directory: {output_dir}")
    print("=" * 50)
    
    pdf_dir = Path(pdf_directory)
    if not pdf_dir.exists():
        print(f"❌ Directory not found: {pdf_directory}")
        print("Creating pdfs directory...")
        pdf_dir.mkdir(exist_ok=True)
        print("✅ Created pdfs directory. Please add PDF files and run again.")
        return []
    
    # Find all PDF files
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_directory}")
        print("Please add PDF files to the pdfs directory and run again.")
        return []
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    results = []
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n--- Analysis {i}/{len(pdf_files)} ---")
        result = analyze_pdf_file(str(pdf_file), output_dir)
        if result:
            results.append(result)
    
    # Generate summary
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("=" * 50)
    print(f"📊 Total PDFs: {len(pdf_files)}")
    print(f"✅ Successfully Analyzed: {len(results)}")
    print(f"❌ Failed: {len(pdf_files) - len(results)}")
    print(f"📁 Results saved in: {output_dir}/")
    
    # Generate CSV exports
    if results:
        try:
            print(f"\n📊 Generating CSV exports...")
            
            # Create CSV exports directory
            csv_dir = "csv_exports"
            Path(csv_dir).mkdir(exist_ok=True)
            
            # Export individual CSV files
            csv_files = []
            for result in results:
                if result and 'equipment_name' in result:
                    try:
                        csv_path = export_analysis_to_csv(result, csv_dir)
                        csv_files.append(csv_path)
                    except Exception as e:
                        print(f"   ⚠️ CSV export failed for {result.get('equipment_name', 'Unknown')}: {e}")
            
            # Create master CSV
            master_csv = create_master_csv("results", csv_dir)
            
            print(f"   ✅ Generated {len(csv_files)} individual CSV files")
            print(f"   ✅ Generated master CSV: {Path(master_csv).name}")
            print(f"   📁 CSV files saved in: {csv_dir}/")
            
        except Exception as e:
            print(f"   ⚠️ CSV export failed: {e}")
        
        # Calculate summary statistics
        health_scores = []
        risk_levels = []
        
        for result in results:
            if 'asset_health' in result:
                score = result['asset_health'].get('overall_score')
                if isinstance(score, (int, float)):
                    health_scores.append(score)
            
            if 'risk_assessment' in result:
                risk = result['risk_assessment'].get('risk_level')
                if risk:
                    risk_levels.append(risk)
        
        if health_scores:
            avg_health = sum(health_scores) / len(health_scores)
            print(f"📈 Average Health Score: {avg_health:.1f}/100")
        
        if risk_levels:
            critical_count = risk_levels.count('CRITICAL')
            high_count = risk_levels.count('HIGH')
            print(f"🚨 Critical Risk: {critical_count}")
            print(f"⚠️ High Risk: {high_count}")
    
    return results

def main():
    """Main function"""
    analyze_all_pdfs()

if __name__ == "__main__":
    main()
