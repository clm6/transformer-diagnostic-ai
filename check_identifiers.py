#!/usr/bin/env python3
import json

# Check current analysis file
try:
    with open('results/Substation_2_analysis.json', 'r') as f:
        data = json.load(f)
    
    print("Equipment Identifiers from JSON:")
    identifiers = data.get('equipment_identifiers', {})
    print(f"Serial Number: {identifiers.get('serial_number', 'Not found')}")
    print(f"Manufacturer: {identifiers.get('manufacturer', 'Not found')}")
    print(f"Year: {identifiers.get('year_of_manufacture', 'Not found')}")
    
    if not identifiers:
        print("❌ No equipment identifiers found in JSON")
    else:
        print("✅ Equipment identifiers found")
        
except Exception as e:
    print(f"Error: {e}")
