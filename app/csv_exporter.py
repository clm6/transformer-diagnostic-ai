#!/usr/bin/env python3
"""
CSV Exporter for Detailed Transformer Analysis
Generates comprehensive tabular data in CSV format
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def export_analysis_to_csv(analysis_data: Dict[str, Any], output_dir: str = "results") -> str:
    """
    Export detailed tabular analysis data to CSV format
    
    Args:
        analysis_data: Complete analysis data from AI analyzer
        output_dir: Directory to save CSV file
    
    Returns:
        str: Path to generated CSV file
    """
    
    # Extract equipment name for filename
    equipment_name = analysis_data.get("equipment_name", "Unknown")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate CSV filename
    csv_filename = f"{equipment_name}_detailed_analysis.csv"
    csv_path = output_path / csv_filename
    
    # Define CSV headers (matching your requested format with equipment identifiers)
    headers = [
        "Equipment Name",
        "Serial Number",
        "Manufacturer",
        "MVA Rating",
        "Voltage Class",
        "Date",
        "Test Type", 
        "Measurement Point",
        "Value(s)",
        "IEEE Reference / Correction",
        "Comment",
        "Risk Analysis",
        "Risk Score (1–5)",
        "Predictive Maintenance (Action Plan)",
        "Life Expectancy (Years)",
        "Remaining Life Forecast (Unit-Level)",
        "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)",
        "V-Curve Analysis (Tap Sweep)",
        "Estimated Cost to Remediate (USD)",
        "Health Index (IEEE C57.152)",
        "Average Risk Score"
    ]
    
    # Extract equipment identifiers and tabular data
    equipment_identifiers = analysis_data.get("equipment_identifiers", {})
    tabular_data = analysis_data.get("detailed_tabular_data", [])
    asset_health = analysis_data.get("asset_health", {})
    
    # Write CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write header
        writer.writeheader()
        
        # Write data rows with equipment identifiers
        for row_data in tabular_data:
            csv_row = {
                "Equipment Name": equipment_name,
                "Serial Number": equipment_identifiers.get("serial_number", ""),
                "Manufacturer": equipment_identifiers.get("manufacturer", ""),
                "MVA Rating": equipment_identifiers.get("mva_rating", ""),
                "Voltage Class": equipment_identifiers.get("voltage_class", ""),
                "Date": row_data.get("date", ""),
                "Test Type": row_data.get("test_type", ""),
                "Measurement Point": row_data.get("measurement_point", ""),
                "Value(s)": row_data.get("values", ""),
                "IEEE Reference / Correction": row_data.get("ieee_reference", ""),
                "Comment": row_data.get("comment", ""),
                "Risk Analysis": row_data.get("risk_analysis", ""),
                "Risk Score (1–5)": row_data.get("risk_score", ""),
                "Predictive Maintenance (Action Plan)": row_data.get("predictive_maintenance", ""),
                "Life Expectancy (Years)": row_data.get("life_expectancy_years", ""),
                "Remaining Life Forecast (Unit-Level)": row_data.get("remaining_life_forecast", ""),
                "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)": row_data.get("roi_scenario_comparison", ""),
                "V-Curve Analysis (Tap Sweep)": row_data.get("v_curve_analysis", ""),
                "Estimated Cost to Remediate (USD)": row_data.get("estimated_cost_usd", ""),
                "Health Index (IEEE C57.152)": asset_health.get("health_index_ieee", ""),
                "Average Risk Score": asset_health.get("average_risk_score", "")
            }
            writer.writerow(csv_row)
        
        # Add summary row if available
        csv_summary = analysis_data.get("csv_summary", {})
        if csv_summary:
            summary_row = {
                "Date": "—",
                "Test Type": "Roll-Up",
                "Measurement Point": "Unit Summary",
                "Value(s)": "—",
                "IEEE Reference / Correction": "—",
                "Comment": "—",
                "Risk Analysis": "—",
                "Risk Score (1–5)": f"Avg ≈ {csv_summary.get('total_risk_score', 0)}",
                "Predictive Maintenance (Action Plan)": "—",
                "Life Expectancy (Years)": "—",
                "Remaining Life Forecast (Unit-Level)": "—",
                "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)": "—",
                "V-Curve Analysis (Tap Sweep)": "—",
                "Estimated Cost to Remediate (USD)": f"${csv_summary.get('total_estimated_cost', 0):,} (Total)"
            }
            writer.writerow(summary_row)
            
            # Add health index row
            health_row = {
                "Date": "—",
                "Test Type": "Health Index (0–100)",
                "Measurement Point": "Unit Score",
                "Value(s)": "—",
                "IEEE Reference / Correction": "—",
                "Comment": "—",
                "Risk Analysis": "—",
                "Risk Score (1–5)": "—",
                "Predictive Maintenance (Action Plan)": "—",
                "Life Expectancy (Years)": "—",
                "Remaining Life Forecast (Unit-Level)": "—",
                "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)": "—",
                "V-Curve Analysis (Tap Sweep)": "—",
                "Estimated Cost to Remediate (USD)": f"≈ {csv_summary.get('health_index', 0)}"
            }
            writer.writerow(health_row)
    
    return str(csv_path)

def export_all_analyses_to_csv(results_dir: str = "results", output_dir: str = "csv_exports") -> List[str]:
    """
    Export all analysis files to individual CSV files
    
    Args:
        results_dir: Directory containing JSON analysis files
        output_dir: Directory to save CSV files
    
    Returns:
        List[str]: Paths to generated CSV files
    """
    
    results_path = Path(results_dir)
    if not results_path.exists():
        return []
    
    csv_files = []
    
    # Process each JSON analysis file
    for json_file in results_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            # Export to CSV
            csv_path = export_analysis_to_csv(analysis_data, output_dir)
            csv_files.append(csv_path)
            
            print(f"✅ CSV exported: {csv_path}")
            
        except Exception as e:
            print(f"❌ Error exporting {json_file}: {e}")
    
    return csv_files

def create_master_csv(results_dir: str = "results", output_dir: str = "csv_exports") -> str:
    """
    Create a master CSV file combining all analyses
    
    Args:
        results_dir: Directory containing JSON analysis files
        output_dir: Directory to save master CSV
    
    Returns:
        str: Path to master CSV file
    """
    
    results_path = Path(results_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    master_csv_path = output_path / "TransformIQ_Master_Analysis.csv"
    
    # Headers for master CSV with equipment identifiers
    headers = [
        "Equipment Name",
        "Serial Number",
        "Manufacturer",
        "MVA Rating",
        "Voltage Class",
        "Date",
        "Test Type", 
        "Measurement Point",
        "Value(s)",
        "IEEE Reference / Correction",
        "Comment",
        "Risk Analysis",
        "Risk Score (1–5)",
        "Predictive Maintenance (Action Plan)",
        "Life Expectancy (Years)",
        "Remaining Life Forecast (Unit-Level)",
        "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)",
        "V-Curve Analysis (Tap Sweep)",
        "Estimated Cost to Remediate (USD)",
        "Health Index (IEEE C57.152)",
        "Average Risk Score"
    ]
    
    all_rows = []
    
    # Collect data from all analysis files
    if results_path.exists():
        for json_file in results_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    analysis_data = json.load(f)
                
                equipment_name = analysis_data.get("equipment_name", "Unknown")
                equipment_identifiers = analysis_data.get("equipment_identifiers", {})
                tabular_data = analysis_data.get("detailed_tabular_data", [])
                asset_health = analysis_data.get("asset_health", {})
                
                # Add equipment identifiers and analysis data to each row
                for row_data in tabular_data:
                    master_row = {
                        "Equipment Name": equipment_name,
                        "Serial Number": equipment_identifiers.get("serial_number", ""),
                        "Manufacturer": equipment_identifiers.get("manufacturer", ""),
                        "MVA Rating": equipment_identifiers.get("mva_rating", ""),
                        "Voltage Class": equipment_identifiers.get("voltage_class", ""),
                        "Date": row_data.get("date", ""),
                        "Test Type": row_data.get("test_type", ""),
                        "Measurement Point": row_data.get("measurement_point", ""),
                        "Value(s)": row_data.get("values", ""),
                        "IEEE Reference / Correction": row_data.get("ieee_reference", ""),
                        "Comment": row_data.get("comment", ""),
                        "Risk Analysis": row_data.get("risk_analysis", ""),
                        "Risk Score (1–5)": row_data.get("risk_score", ""),
                        "Predictive Maintenance (Action Plan)": row_data.get("predictive_maintenance", ""),
                        "Life Expectancy (Years)": row_data.get("life_expectancy_years", ""),
                        "Remaining Life Forecast (Unit-Level)": row_data.get("remaining_life_forecast", ""),
                        "ROI Scenario Comparison (A=Bushings / B=Run-to-Failure / C=Replace)": row_data.get("roi_scenario_comparison", ""),
                        "V-Curve Analysis (Tap Sweep)": row_data.get("v_curve_analysis", ""),
                        "Estimated Cost to Remediate (USD)": row_data.get("estimated_cost_usd", ""),
                        "Health Index (IEEE C57.152)": asset_health.get("health_index_ieee", ""),
                        "Average Risk Score": asset_health.get("average_risk_score", "")
                    }
                    all_rows.append(master_row)
                    
            except Exception as e:
                print(f"❌ Error processing {json_file}: {e}")
    
    # Write master CSV
    with open(master_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_rows)
    
    return str(master_csv_path)
