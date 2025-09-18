#!/usr/bin/env python3
from app.pdf_parser import extract_text_from_pdf, extract_equipment_identifiers

# Test Sub 2 PDF
text = extract_text_from_pdf('pdfs/Sub 2 transformer.pdf')
print("Testing Sub 2 PDF...")
print("Text length:", len(text))

# Check for H 880287
if 'H 880287' in text:
    print("✅ H 880287 found in text")
else:
    print("❌ H 880287 not found")

# Test extraction
identifiers = extract_equipment_identifiers(text)
print("Found identifiers:", identifiers)

# Show first 1000 characters
print("\nFirst 1000 characters:")
print(text[:1000])
