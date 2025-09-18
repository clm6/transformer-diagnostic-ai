#!/usr/bin/env python3
"""
Test equipment identifier extraction
"""

from app.pdf_parser import extract_text_from_pdf, extract_equipment_identifiers
import re

def test_extraction():
    """Test identifier extraction from PDF"""
    
    text = extract_text_from_pdf('pdfs/uploaded_transformer.pdf')
    
    print("📄 PDF Text Analysis")
    print("=" * 50)
    
    # Look for "Serial" in text
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'Serial' in line:
            print(f"Line {i}: '{line}'")
            # Show surrounding lines
            for j in range(max(0, i-2), min(len(lines), i+5)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j}: '{lines[j]}'")
            print("-" * 30)
    
    # Test specific patterns
    print("\n🔍 Testing Serial Number Patterns:")
    
    # Look for H 880287 format specifically
    h_pattern = r'\b([A-Z]\s+\d{6})\b'
    h_matches = re.findall(h_pattern, text)
    print(f"H + 6 digits pattern: {h_matches}")
    
    # Look for any letter + numbers
    letter_num_pattern = r'\b([A-Z]\s*\d{5,})\b'
    letter_matches = re.findall(letter_num_pattern, text)
    print(f"Letter + 5+ digits: {letter_matches}")
    
    # Test current extraction
    identifiers = extract_equipment_identifiers(text)
    print(f"\nCurrent extraction result: {identifiers}")
    
    # Look for manufacturer info
    if 'GE' in text:
        print(f"\n✅ Found 'GE' in text")
    if 'Manufacturer' in text:
        print(f"✅ Found 'Manufacturer' in text")

if __name__ == "__main__":
    test_extraction()
