#!/usr/bin/env python3
"""
Local test version of PDF Outline Extractor
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from pdf_outline_extractor import PDFOutlineExtractor

class LocalPDFOutlineExtractor(PDFOutlineExtractor):
    """Local version for testing on Windows."""
    
    def __init__(self, input_dir="test_input", output_dir="test_output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.max_pages = 50
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

if __name__ == "__main__":
    # Test with local directories
    extractor = LocalPDFOutlineExtractor()
    extractor.run()
