#!/usr/bin/env python3
"""
AI Analyzer for Transformer Diagnostics
Generates comprehensive reports using OpenAI GPT-4
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
import os
from pathlib import Path

# Get the parent directory (project root) where .env is located
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

class TransformerAnalyzer:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Please check your .env file.")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_comprehensive_report(self, text: str, equipment_name: str, document_date: str) -> Dict[str, Any]:
        """Generate comprehensive transformer diagnostic report"""
        
        prompt = f"""
You are an expert transformer diagnostic engineer analyzing TRAX test reports with IEEE standards expertise.
Generate a comprehensive diagnostic analysis for equipment: {equipment_name}

ENHANCED ANALYSIS REQUIREMENTS:
1. IEEE C57.152 Health Index scoring (0-100) with component risk scores (1-5)
2. Risk assessment with priority levels aligned to IEEE standards
3. Financial impact analysis with ROI scenarios
4. Maintenance recommendations with specific timelines
5. Technical analysis of all components with IEEE references
6. Executive summary for management
7. DETAILED TABULAR DATA for CSV export
8. Predictive maintenance planning with life expectancy forecasting
9. Cost-benefit analysis with multiple scenarios

CRITICAL SCORING CALIBRATION:
- Assign component-level Risk Scores (1–5) for each major component:
  1 = Very Low Risk (Excellent condition)
  2 = Low Risk (Acceptable, monitor)
  3 = Moderate Risk (Aging, some corrective work needed)
  4 = High Risk (Outside IEEE guidelines, corrective maintenance required soon)
  5 = Critical Risk (Immediate action required; end-of-life)

- Calculate Average Risk Score across all components
- Convert to IEEE C57.152 Health Index using: Health Index = 100 – ((Average Risk Score – 1) / 4) × 100

DETAILED COMPONENT ANALYSIS:
- Winding Resistance Analysis (with IEEE C57.152 temperature correction)
- Turns Ratio & Excitation Current (IEEE ±0.5% tolerance)
- Tan Delta/Power Factor Analysis (IEEE thresholds and trending)
- Bushing C1 Power Factor (with nameplate comparison and replacement recommendations)
- V-Curve Analysis and tap sweep assessment
- Life expectancy forecasting with remaining life calculations
- ROI scenario comparison (repair vs run-to-failure vs replacement)

RETURN FORMAT:
Provide a comprehensive report with DETAILED TABULAR DATA in the following JSON structure:

{{
    "equipment_name": "{equipment_name}",
    "document_date": "{document_date}",
    "analysis_date": "{datetime.now().strftime('%Y-%m-%d')}",
    "asset_health": {{
        "overall_score": 85,
        "health_index_ieee": 75,
        "average_risk_score": 2.0,
        "condition": "Good/Fair/Critical",
        "estimated_remaining_life_years": 5,
        "component_risk_scores": {{
            "winding_resistance": 2,
            "turns_ratio": 2,
            "main_insulation": 3,
            "bushing_pf": 3,
            "demagnetization": 1
        }},
        "component_scores": {{
            "winding_resistance": 90,
            "turns_ratio": 85,
            "main_insulation": 70,
            "bushing_pf": 80,
            "demagnetization": 95
        }}
    }},
    "risk_assessment": {{
        "risk_level": "LOW/MODERATE/HIGH/CRITICAL",
        "critical_issues": ["List of critical issues"],
        "immediate_actions": ["Actions needed within 30 days"],
        "near_term_actions": ["Actions needed within 6 months"]
    }},
    "financial_analysis": {{
        "immediate_investment_required": 50000,
        "failure_cost_avoidance": 2500000,
        "roi_percentage": 5000
    }},
    "technical_analysis": {{
        "winding_resistance": {{
            "lv_windings": "Detailed analysis with values",
            "hv_windings": "Detailed analysis with values",
            "status": "OK/WARNING/CRITICAL"
        }},
        "turns_ratio": {{
            "error_percentage": 0.15,
            "excitation_current": "Analysis",
            "status": "OK/WARNING/CRITICAL"
        }},
        "tan_delta": {{
            "chl": {{"pf_20c_percent": 0.28, "status": "OK"}},
            "clg": {{"pf_20c_percent": 0.45, "status": "WARNING"}},
            "clh": {{"pf_20c_percent": 0.30, "status": "OK"}},
            "chg": {{"pf_20c_percent": 0.25, "status": "OK"}}
        }},
        "bushing_analysis": {{
            "h1": {{"pf_20c_percent": 0.26, "status": "OK"}},
            "h2": {{"pf_20c_percent": 0.25, "status": "OK"}},
            "h3": {{"pf_20c_percent": 0.27, "status": "OK"}},
            "x0": {{"pf_20c_percent": 0.35, "status": "WARNING"}},
            "x1": {{"pf_20c_percent": 0.32, "status": "OK"}},
            "x2": {{"pf_20c_percent": 0.30, "status": "OK"}},
            "x3": {{"pf_20c_percent": 0.33, "status": "OK"}}
        }}
    }},
    "executive_summary": "Management-ready summary with key findings, risks, and recommendations",
    "maintenance_recommendations": [
        {{"priority": "CRITICAL", "action": "Specific action", "timeframe": "Immediate"}},
        {{"priority": "HIGH", "action": "Specific action", "timeframe": "30 days"}},
        {{"priority": "ROUTINE", "action": "Specific action", "timeframe": "6 months"}}
    ],
    "detailed_tabular_data": [
        {{
            "date": "{document_date}",
            "test_type": "Winding Resistance",
            "measurement_point": "H1-H3/X1-X0",
            "values": "1.097 Ω (→ 65°C: 16.07 mΩ)",
            "ieee_reference": "IEEE C57.152 (65°C normalization)",
            "comment": "Normal",
            "risk_analysis": "Balanced, stable trend",
            "risk_score": 2,
            "predictive_maintenance": "Routine trending every 2–3 years",
            "life_expectancy_years": 12,
            "remaining_life_forecast": "~12 yrs if stable LTC maintained",
            "roi_scenario_comparison": "A: +10 yrs life for <$50k vs B: −5 yrs risk penalty vs C: +30 yrs for ~$1.5M",
            "v_curve_analysis": "V-curve symmetric, balanced (<2% phase imbalance)",
            "estimated_cost_usd": 0
        }},
        {{
            "date": "{document_date}",
            "test_type": "TTR (Turns Ratio)",
            "measurement_point": "H1-H3/X1-X0 (Tap 16R)",
            "values": "Nom: 8.289 / Meas: 8.305 (Err: 0.19%)",
            "ieee_reference": "IEEE ±0.5% tolerance",
            "comment": "Pass",
            "risk_analysis": "Error < 0.5% tolerance",
            "risk_score": 1,
            "predictive_maintenance": "No action; confirm during major maintenance",
            "life_expectancy_years": 15,
            "remaining_life_forecast": "~15 yrs baseline",
            "roi_scenario_comparison": "Same as above",
            "v_curve_analysis": "Not applicable",
            "estimated_cost_usd": 0
        }},
        {{
            "date": "{document_date}",
            "test_type": "Tan Delta – Bushings C1",
            "measurement_point": "H1",
            "values": "0.522% → 0.504% (20°C corr.)",
            "ieee_reference": "IEEE ≤0.7% warning",
            "comment": "High (replace)",
            "risk_analysis": "Trending above warning, replacement required",
            "risk_score": 4,
            "predictive_maintenance": "Replace bushing within 1 year; re-baseline after replacement",
            "life_expectancy_years": 7,
            "remaining_life_forecast": "5–7 yrs if not replaced; ~15–17 yrs if replaced",
            "roi_scenario_comparison": "A: +10 yrs for ~$45k vs B: forced outage risk vs C: +30 yrs/$1.5M",
            "v_curve_analysis": "Not applicable",
            "estimated_cost_usd": 15000
        }}
    ],
    "equipment_identifiers": {{
        "serial_number": "TX221380042",
        "manufacturer": "ABB",
        "year_of_manufacture": 2018,
        "mva_rating": 25,
        "voltage_class": "115kV/13.8kV",
        "asset_tag": "TX-22-115-13.8",
        "additional_ids": {{
            "location_id": "Sub22",
            "feeder_id": "F-22-01"
        }}
    }},
    "csv_summary": {{
        "average_risk_score": 2.7,
        "health_index_ieee": 57,
        "total_estimated_cost": 45000,
        "critical_items_count": 3,
        "immediate_actions_count": 2
    }}
}}

CRITICAL INSTRUCTIONS:
1. Calculate component-level Risk Scores (1-5) for each major component based on IEEE C57.152 guidelines
2. Compute Average Risk Score across all components
3. Convert to Health Index using: Health Index = 100 – ((Average Risk Score – 1) / 4) × 100
4. Report both "Average Risk Score" and "Health Index (IEEE C57.152)" in the JSON
5. Ensure Remaining Life Forecast aligns with Health Index and component risk scores
6. Extract equipment identifiers for historical tracking and correlation
7. Keep all other analysis sections unchanged (technical analysis, recommendations, executive summary, financial analysis)

EQUIPMENT IDENTIFIERS EXTRACTION:
- Extract and include equipment identifiers from the report for future correlation and historical tracking
- REQUIRED: serial_number (search for serial number, unit ID, asset tag, etc.)
- OPTIONAL: manufacturer, year_of_manufacture, MVA_rating, voltage_class, and any additional IDs found
- Include an "equipment_identifiers" block with at least the serial_number, plus any other identifiers available

TRANSFORMER TEST DATA:
{text}

Analyze this data and provide the comprehensive report in the exact JSON format specified above, with proper IEEE C57.152 Health Index calibration.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert transformer diagnostic engineer with 20+ years of experience analyzing TRAX test reports. Provide precise, actionable insights based on IEEE and IEC standards."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.1
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON from response
            try:
                # Find JSON content between curly braces
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    analysis_data = json.loads(json_str)
                    return analysis_data
                else:
                    # Fallback if JSON extraction fails
                    return {
                        "error": "Failed to extract JSON from response",
                        "raw_response": response_text
                    }
                    
            except json.JSONDecodeError as e:
                return {
                    "error": f"JSON parsing error: {str(e)}",
                    "raw_response": response_text
                }
                
        except Exception as e:
            return {
                "error": f"API call failed: {str(e)}"
            }
