#!/usr/bin/env python3
"""
Test script for PDF Outline Extractor
Creates sample PDFs and tests the extraction functionality
"""

import os
import json
from pathlib import Path
import fitz  # PyMuPDF
from pdf_outline_extractor import PDFOutlineExtractor

def create_sample_pdf():
    """Create a sample PDF with different heading levels for testing."""
    doc = fitz.open()
    
    # Page 1
    page1 = doc.new_page()
    
    # Title (largest font)
    page1.insert_text((50, 100), "Sample Document Title", fontsize=24, fontname="helv")
    
    # H1 heading
    page1.insert_text((50, 200), "Chapter 1: Introduction", fontsize=16, fontname="hebo")
    
    # Some body text
    page1.insert_text((50, 250), "This is some body text content...", fontsize=12, fontname="helv")
    
    # H2 heading
    page1.insert_text((50, 300), "1.1 Overview", fontsize=14, fontname="hebo")
    
    # H3 heading
    page1.insert_text((50, 350), "1.1.1 Background", fontsize=13, fontname="hebo")
    
    # Page 2
    page2 = doc.new_page()
    
    # H1 heading
    page2.insert_text((50, 100), "Chapter 2: Methodology", fontsize=16, fontname="hebo")
    
    # H2 heading
    page2.insert_text((50, 150), "2.1 Approach", fontsize=14, fontname="hebo")
    
    # H3 heading
    page2.insert_text((50, 200), "2.1.1 Data Collection", fontsize=13, fontname="hebo")
    
    # Save the sample PDF
    sample_path = Path("test_input/sample_document.pdf")
    sample_path.parent.mkdir(exist_ok=True)
    doc.save(str(sample_path))
    doc.close()
    
    print(f"Created sample PDF: {sample_path}")
    return sample_path

def test_extractor():
    """Test the PDF outline extractor."""
    print("Creating sample PDF...")
    sample_pdf = create_sample_pdf()
    
    print("Testing PDF outline extraction...")
    
    # Create test directories
    test_input = Path("test_input")
    test_output = Path("test_output")
    test_output.mkdir(exist_ok=True)
    
    # Initialize extractor with test directories
    extractor = PDFOutlineExtractor(input_dir=test_input, output_dir=test_output)
    
    # Process the sample PDF
    result = extractor.process_pdf(sample_pdf)
    
    # Save and display result
    output_file = test_output / "sample_document.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtraction completed! Result saved to: {output_file}")
    print("\nExtracted outline:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_extractor()
