#!/usr/bin/env python3
"""
Advanced test script with complex PDF scenarios
"""

import fitz
from pathlib import Path
from pdf_outline_extractor import PDFOutlineExtractor

def create_complex_pdf():
    """Create a more complex PDF with various edge cases."""
    doc = fitz.open()
    
    # Page 1 - Title page with multiple large fonts
    page1 = doc.new_page()
    
    # Large title
    page1.insert_text((50, 80), "Advanced Research Paper", fontsize=28, fontname="helv")
    # Subtitle 
    page1.insert_text((50, 120), "A Comprehensive Study", fontsize=20, fontname="helv")
    # Author (should not be detected as heading)
    page1.insert_text((50, 180), "Dr. Jane Smith", fontsize=14, fontname="helv")
    # Abstract heading
    page1.insert_text((50, 250), "Abstract", fontsize=16, fontname="hebo")
    # Abstract text (body text)
    page1.insert_text((50, 280), "This paper presents a comprehensive analysis...", fontsize=12, fontname="helv")
    
    # Page 2 - Table of contents and introduction
    page2 = doc.new_page()
    
    # TOC heading
    page2.insert_text((50, 50), "Table of Contents", fontsize=16, fontname="hebo")
    # TOC entries (should not be headings)
    page2.insert_text((50, 100), "1. Introduction ........................ 3", fontsize=12, fontname="helv")
    page2.insert_text((50, 120), "2. Literature Review .................. 5", fontsize=12, fontname="helv")
    
    # Actual Introduction heading
    page2.insert_text((50, 200), "1. Introduction", fontsize=16, fontname="hebo")
    page2.insert_text((50, 240), "This study examines...", fontsize=12, fontname="helv")
    
    # Subsection
    page2.insert_text((50, 300), "1.1 Research Questions", fontsize=14, fontname="hebo")
    
    # Page 3 - Literature review with numbered subsections
    page3 = doc.new_page()
    
    page3.insert_text((50, 50), "2. Literature Review", fontsize=16, fontname="hebo")
    page3.insert_text((50, 100), "Previous research has shown...", fontsize=12, fontname="helv")
    
    page3.insert_text((50, 150), "2.1 Theoretical Framework", fontsize=14, fontname="hebo")
    page3.insert_text((50, 180), "The theoretical foundation...", fontsize=12, fontname="helv")
    
    page3.insert_text((50, 230), "2.1.1 Core Concepts", fontsize=13, fontname="hebo")
    page3.insert_text((50, 260), "The core concepts include...", fontsize=12, fontname="helv")
    
    # Figure caption (should not be heading)
    page3.insert_text((50, 320), "Figure 1: Conceptual Framework", fontsize=11, fontname="helv")
    
    # Page 4 - Methodology
    page4 = doc.new_page()
    
    page4.insert_text((50, 50), "3. Methodology", fontsize=16, fontname="hebo")
    page4.insert_text((50, 100), "This section describes...", fontsize=12, fontname="helv")
    
    page4.insert_text((50, 150), "3.1 Data Collection", fontsize=14, fontname="hebo")
    page4.insert_text((50, 200), "3.2 Analysis Techniques", fontsize=14, fontname="hebo")
    
    # Mixed case heading
    page4.insert_text((50, 250), "3.2.1 STATISTICAL ANALYSIS", fontsize=13, fontname="hebo")
    
    # Table caption (should not be heading)
    page4.insert_text((50, 320), "Table 1: Sample Demographics", fontsize=11, fontname="helv")
    
    # Page 5 - Results and conclusions
    page5 = doc.new_page()
    
    page5.insert_text((50, 50), "4. Results and Discussion", fontsize=16, fontname="hebo")
    page5.insert_text((50, 100), "The analysis revealed...", fontsize=12, fontname="helv")
    
    page5.insert_text((50, 150), "4.1 Key Findings", fontsize=14, fontname="hebo")
    page5.insert_text((50, 200), "4.2 Implications", fontsize=14, fontname="hebo")
    
    # Conclusion
    page5.insert_text((50, 280), "5. Conclusion", fontsize=16, fontname="hebo")
    
    # Save the complex PDF
    complex_path = Path("test_input/complex_document.pdf")
    doc.save(str(complex_path))
    doc.close()
    
    print(f"Created complex PDF: {complex_path}")
    return complex_path

def test_complex_extraction():
    """Test extraction on complex PDF."""
    print("Creating complex PDF...")
    complex_pdf = create_complex_pdf()
    
    print("Testing complex PDF extraction...")
    
    # Create directories
    test_input = Path("test_input")
    test_output = Path("test_output")
    test_output.mkdir(exist_ok=True)
    
    # Initialize extractor
    extractor = PDFOutlineExtractor(input_dir=test_input, output_dir=test_output)
    
    # Process the complex PDF
    result = extractor.process_pdf(complex_pdf)
    
    # Save result
    output_file = test_output / "complex_document.json"
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplex extraction completed! Result saved to: {output_file}")
    print("\nExtracted outline:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_complex_extraction()
