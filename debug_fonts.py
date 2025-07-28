#!/usr/bin/env python3
"""
Debug version to analyze font characteristics in complex PDF
"""

import fitz
import json
from pathlib import Path
from collections import defaultdict

def debug_pdf_fonts():
    """Debug font analysis for complex PDF."""
    pdf_path = Path("test_input/complex_document.pdf")
    
    if not pdf_path.exists():
        print("Complex PDF not found. Run test_complex.py first.")
        return
    
    doc = fitz.open(str(pdf_path))
    font_stats = defaultdict(list)
    
    print("=== FONT ANALYSIS DEBUG ===\n")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        print(f"PAGE {page_num + 1}:")
        print("-" * 40)
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text and len(text) > 3:
                            font_info = {
                                "text": text,
                                "page": page_num + 1,
                                "size": span["size"],
                                "flags": span["flags"],
                                "font": span["font"],
                                "bbox": span["bbox"],
                                "is_bold": bool(span["flags"] & 2**4),
                                "is_italic": bool(span["flags"] & 2**1),
                            }
                            
                            font_stats[span["size"]].append(font_info)
                            
                            print(f"  '{text}' - Size: {span['size']:.1f}, Bold: {font_info['is_bold']}, Font: {span['font']}")
        print()
    
    doc.close()
    
    print("\n=== FONT SIZE SUMMARY ===")
    for size in sorted(font_stats.keys(), reverse=True):
        blocks = font_stats[size]
        bold_count = sum(1 for b in blocks if b["is_bold"])
        print(f"Size {size:.1f}: {len(blocks)} blocks, {bold_count} bold")
        for block in blocks:
            print(f"  - '{block['text'][:50]}...' (Page {block['page']}, Bold: {block['is_bold']})")

if __name__ == "__main__":
    debug_pdf_fonts()
