#!/usr/bin/env python3
"""
PDF Parser for TRAX Transformer Reports
Extracts text and metadata from transformer diagnostic PDFs
"""

import fitz  # PyMuPDF
import re
from datetime import datetime
from typing import Optional, Tuple


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        doc = fitz.open(file_path)
        text = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        
        # Limit text length for optimal AI analysis
        if len(text) > 15000:
            text = text[:15000]
        
        return text
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_substation_name(text: str) -> str:
    """Extract substation/equipment name from PDF text"""
    
    # Common patterns for substation identification
    patterns = [
        r'(?i)substation\s+(\d+)',
        r'(?i)sub\s+(\d+)',
        r'(?i)station\s+(\d+)',
        r'(?i)transformer\s+(\w+)',
        r'(?i)tx[_-]?(\w+)',
        r'(?i)unit\s+(\w+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return f"Substation_{match.group(1)}"
    
    # Fallback to timestamp-based naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Transformer_{timestamp}"


def extract_document_date(file_path: str, text: str) -> str:
    """Extract document date from PDF content or filename"""
    
    # Try to find date patterns in text
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
        r'(?i)(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                # Try to parse the found date
                date_str = match.group(1)
                # This is a simple approach - you might want more sophisticated date parsing
                return date_str
            except:
                continue
    
    # Fallback to current date
    return datetime.now().strftime("%Y-%m-%d")


def extract_equipment_identifiers(text: str) -> dict:
    """Extract equipment identifiers from transformer test report"""
    
    identifiers = {}
    
    # Serial number patterns (enhanced for TRAX format)
    serial_patterns = [
        # TRAX format: "Serial #" followed by value on next line or nearby
        r'(?i)serial\s*#\s*([A-Z]\s+\d{6,})',
        r'(?i)serial\s*#?\s*([A-Z]?\s*\d{5,})',
        r'(?i)serial\s*number\s*:?\s*([A-Z]?\s*\d+)',
        r'(?i)s/n\s*:?\s*([A-Z]?\s*\d+)',
        # Pattern for "H 880287" format specifically
        r'\b([A-Z]\s+\d{6,})\b',
        # Look for patterns after "Serial #" in table format
        r'Serial\s*#\s*([A-Z]\s+\d+)',
        r'Serial\s*#\s+([A-Z]\d+)',
        # More flexible patterns
        r'(?i)asset\s*id\s*:?\s*([A-Z]?\s*\d+)',
        r'(?i)unit\s*id\s*:?\s*([A-Z]?\s*\d+)',
        r'(?i)transformer\s*id\s*:?\s*([A-Z]?\s*\d+)'
    ]
    
    for pattern in serial_patterns:
        match = re.search(pattern, text)
        if match:
            serial = match.group(1).strip()
            if serial and len(serial) > 3:  # Valid serial number
                identifiers['serial_number'] = serial
                break
    
    # Manufacturer patterns
    manufacturer_patterns = [
        r'(?i)manufacturer\s*:?\s*(GE|ABB|Siemens|Westinghouse|Cooper|Eaton|Schneider)',
        r'(?i)made\s*by\s*:?\s*(GE|ABB|Siemens|Westinghouse|Cooper|Eaton|Schneider)',
        r'(?i)mfg\s*:?\s*(GE|ABB|Siemens|Westinghouse|Cooper|Eaton|Schneider)',
        r'\b(GE|ABB|Siemens|Westinghouse|Cooper|Eaton|Schneider)\b'
    ]
    
    for pattern in manufacturer_patterns:
        match = re.search(pattern, text)
        if match:
            identifiers['manufacturer'] = match.group(1).upper()
            break
    
    # Year patterns
    year_patterns = [
        r'(?i)year\s*:?\s*(\d{4})',
        r'(?i)manufactured\s*:?\s*(\d{4})',
        r'(?i)date\s*of\s*manufacture\s*:?\s*(\d{4})',
        r'\b(19\d{2}|20\d{2})\b'  # Years 1900-2099
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, text)
        if match:
            year = int(match.group(1))
            if 1950 <= year <= 2030:  # Reasonable transformer manufacturing years
                identifiers['year_of_manufacture'] = year
                break
    
    # MVA rating patterns
    mva_patterns = [
        r'(?i)(\d+\.?\d*)\s*mva',
        r'(?i)mva\s*:?\s*(\d+\.?\d*)',
        r'(?i)rating\s*:?\s*(\d+\.?\d*)\s*mva'
    ]
    
    for pattern in mva_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                mva = float(match.group(1))
                if 0.1 <= mva <= 1000:  # Reasonable MVA range
                    identifiers['mva_rating'] = mva
                    break
            except:
                continue
    
    # Voltage class patterns
    voltage_patterns = [
        r'(\d+\.?\d*)\s*kv\s*/\s*(\d+\.?\d*)\s*kv',
        r'(\d+\.?\d*)\s*kv\s*-\s*(\d+\.?\d*)\s*kv',
        r'(?i)voltage\s*:?\s*(\d+\.?\d*)\s*kv\s*/\s*(\d+\.?\d*)\s*kv'
    ]
    
    for pattern in voltage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            hv = match.group(1)
            lv = match.group(2)
            identifiers['voltage_class'] = f"{hv}kV/{lv}kV"
            break
    
    return identifiers
