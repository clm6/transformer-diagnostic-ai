#!/usr/bin/env python3
"""
Export Comprehensive Analysis to CSV
Generates detailed tabular data with IEEE references and predictive maintenance
"""

from app.csv_exporter import export_all_analyses_to_csv, create_master_csv

def main():
    """Export all analyses to CSV format"""
    
    print("📊 TRANSFORMIQ CSV EXPORT")
    print("=" * 50)
    print("🔧 Generating detailed tabular analysis data...")
    
    # Export individual CSV files
    csv_files = export_all_analyses_to_csv("results", "csv_exports")
    
    # Create master CSV
    master_csv = create_master_csv("results", "csv_exports")
    
    print(f"\n🎉 CSV EXPORT COMPLETE!")
    print("=" * 50)
    print(f"📄 Individual CSV files: {len(csv_files)}")
    for csv_file in csv_files:
        print(f"   • {csv_file}")
    
    print(f"\n📋 Master CSV file:")
    print(f"   • {master_csv}")
    
    print(f"\n📊 CSV files include:")
    print(f"   • Date and test type")
    print(f"   • Measurement points and values")
    print(f"   • IEEE references and corrections")
    print(f"   • Risk analysis and scoring (1-5)")
    print(f"   • Predictive maintenance planning")
    print(f"   • Life expectancy forecasting")
    print(f"   • ROI scenario comparisons")
    print(f"   • V-curve analysis")
    print(f"   • Cost estimates")
    
    print(f"\n💼 Ready for:")
    print(f"   • Excel analysis")
    print(f"   • Power BI dashboards")
    print(f"   • Tableau visualization")
    print(f"   • Management reporting")

if __name__ == "__main__":
    main()
