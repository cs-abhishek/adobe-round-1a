#!/usr/bin/env python3
"""
Adobe Hackathon 2025 - Round 1A
PDF Outline Extractor

Extracts structured outline (Title, H1, H2, H3) from PDF files with page numbers.
Outputs results in JSON format.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFOutlineExtractor:
    """Extract structured outline from PDF files."""
    
    def __init__(self, input_dir=None, output_dir=None):
        self.input_dir = Path(input_dir) if input_dir else Path("/app/input")
        self.output_dir = Path(output_dir) if output_dir else Path("/app/output")
        self.max_pages = 50
        
        # Only create directory if it doesn't exist and path is valid
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, FileNotFoundError):
            # For Docker, the directories should already exist or be mounted
            pass
    
    def analyze_font_characteristics(self, doc: fitz.Document) -> Dict:
        """Analyze font characteristics across the document to establish hierarchy."""
        font_stats = defaultdict(list)
        text_blocks = []
        
        # Collect all text blocks with their characteristics
        for page_num in range(min(len(doc), self.max_pages)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text and len(text) > 3:  # Filter out short text
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
                                text_blocks.append(font_info)
        
        return {"font_stats": font_stats, "text_blocks": text_blocks}
    
    def identify_title(self, analysis: Dict) -> Optional[str]:
        """Identify document title (usually largest font on first page)."""
        first_page_blocks = [block for block in analysis["text_blocks"] if block["page"] == 1]
        
        if not first_page_blocks:
            return None
        
        # Find the largest font size on first page
        max_size = max(block["size"] for block in first_page_blocks)
        
        # Get candidates with largest font size
        title_candidates = [
            block for block in first_page_blocks 
            if block["size"] == max_size and len(block["text"]) > 10
        ]
        
        if title_candidates:
            # Prefer bold text or text closer to top
            title_candidates.sort(key=lambda x: (not x["is_bold"], x["bbox"][1]))
            return title_candidates[0]["text"]
        
        return None
    
    def establish_heading_hierarchy(self, analysis: Dict) -> Dict[str, float]:
        """Establish heading hierarchy based on font sizes and characteristics."""
        font_stats = analysis["font_stats"]
        
        # Get font sizes sorted by frequency and size
        size_frequency = {size: len(blocks) for size, blocks in font_stats.items()}
        total_blocks = sum(size_frequency.values())
        
        # Analyze all font sizes
        size_characteristics = {}
        for size, blocks in font_stats.items():
            if len(blocks) > 0:
                bold_count = sum(1 for block in blocks if block["is_bold"])
                heading_like = sum(1 for block in blocks if self.is_likely_heading(block["text"]))
                
                frequency_ratio = len(blocks) / total_blocks
                
                size_characteristics[size] = {
                    "total": len(blocks),
                    "bold_ratio": bold_count / len(blocks),
                    "heading_ratio": heading_like / len(blocks),
                    "frequency_ratio": frequency_ratio,
                    "all_bold": bold_count == len(blocks),
                    "has_headings": heading_like > 0,
                }
        
        # Find title size (largest font, usually not bold)
        title_size = max(size_characteristics.keys())
        
        # Find heading candidates (exclude title size, prefer bold text)
        heading_candidates = []
        for size, stats in size_characteristics.items():
            # Skip title size and very small fonts
            if size == title_size or size < 10:
                continue
                
            # Skip very common body text (unless it's bold)
            if stats["frequency_ratio"] > 0.5 and stats["bold_ratio"] < 0.5:
                continue
            
            # Score based on heading characteristics
            score = 0
            if stats["all_bold"] and stats["has_headings"]:
                score += 100  # Perfect heading candidate
            elif stats["bold_ratio"] > 0.5:
                score += 50   # Mostly bold
            elif stats["has_headings"]:
                score += 25   # Has heading patterns
                
            # Bonus for reasonable frequency (not too rare, not too common)
            if 0.02 <= stats["frequency_ratio"] <= 0.3:
                score += 20
            
            # Font size factor
            score += size
            
            if score > 15:  # Minimum threshold
                heading_candidates.append((score, size, stats))
        
        # Sort by font size (descending) to maintain proper hierarchy
        heading_candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Assign heading levels h1 > h2 > h3 by font size
        hierarchy = {}
        level_names = ["h1", "h2", "h3"]
        
        for i, (score, size, stats) in enumerate(heading_candidates[:3]):
            hierarchy[level_names[i]] = size
        
        # Ensure we have at least one level
        if not hierarchy and heading_candidates:
            hierarchy["h1"] = heading_candidates[0][1]
        
        return hierarchy
    
    def is_likely_heading(self, text: str) -> bool:
        """Check if text is likely a heading based on content patterns."""
        text = text.strip()
        
        # Basic length constraints
        if len(text) < 3 or len(text) > 200:
            return False
        
        # Common heading patterns
        heading_patterns = [
            r'^\d+\.',  # 1. 2. 3.
            r'^\d+\.\d+',  # 1.1 1.2
            r'^Chapter\s+\d+',  # Chapter 1
            r'^Section\s+\d+',  # Section 1
            r'^Part\s+[IVX]+',  # Part I, II, III
            r'^\d+\.\d+\.\d+',  # 1.1.1
        ]
        
        import re
        has_pattern = any(re.match(pattern, text, re.IGNORECASE) for pattern in heading_patterns)
        
        # Content-based heuristics
        heading_indicators = [
            text[0].isupper(),  # Starts with capital
            not text.endswith('.') or text.count('.') <= 2,  # Doesn't end with period (except numbering)
            len(text.split()) <= 20,  # Not too long (increased limit)
            not text.lower().startswith(('fig', 'table', 'figure', 'image', 'photo')),  # Not captions
            not text.lower().startswith(('page', 'see', 'refer', 'note:')),  # Not references
            ':' not in text or text.count(':') == 1,  # At most one colon
            not text.isdigit(),  # Not just a number
            has_pattern or text[0].isupper(),  # Has pattern or starts with capital
        ]
        
        return sum(heading_indicators) >= 5
    
    def extract_headings(self, analysis: Dict, hierarchy: Dict[str, float]) -> List[Dict]:
        """Extract headings based on established hierarchy."""
        headings = []
        text_blocks = analysis["text_blocks"]
        
        # Get title font size to exclude it from headings
        title_size = None
        first_page_blocks = [block for block in text_blocks if block["page"] == 1]
        if first_page_blocks:
            title_size = max(block["size"] for block in first_page_blocks)
        
        for block in text_blocks:
            text = block["text"].strip()
            size = block["size"]
            
            # Skip if it's likely the title (largest font on first page)
            if title_size and abs(size - title_size) < 0.1 and block["page"] == 1:
                continue
            
            # Check if this block matches any heading level
            for level, level_size in hierarchy.items():
                if abs(size - level_size) < 0.1:  # Allow small size variations
                    # More specific checks for each level
                    is_heading = False
                    
                    if level == "h1":
                        # H1: Must be bold OR large font with heading pattern
                        is_heading = (block["is_bold"] or size >= 16) and self.is_likely_heading(text)
                    elif level == "h2":
                        # H2: Should be bold and heading-like
                        is_heading = block["is_bold"] and self.is_likely_heading(text)
                    elif level == "h3":
                        # H3: Should be bold and heading-like
                        is_heading = block["is_bold"] and self.is_likely_heading(text)
                    
                    # Additional filters
                    if is_heading:
                        # Skip table of contents entries and figure captions
                        text_lower = text.lower()
                        if any(skip in text_lower for skip in [
                            "table of contents", "figure", "table 1:", "page ", 
                            "see section", "refer to", "....................", "......."
                        ]):
                            continue
                        
                        headings.append({
                            "text": text,
                            "level": level,
                            "page": block["page"],
                            "size": size,
                            "is_bold": block["is_bold"]
                        })
                        break
        
        # Remove duplicates and sort by page then by position
        seen = set()
        unique_headings = []
        for heading in headings:
            key = (heading["text"], heading["page"])
            if key not in seen:
                seen.add(key)
                unique_headings.append(heading)
        
        # Sort by page number
        unique_headings.sort(key=lambda x: x["page"])
        
        return unique_headings
    
    def process_pdf(self, pdf_path: Path) -> Dict:
        """Process a single PDF file and extract outline."""
        logger.info(f"Processing: {pdf_path.name}")
        
        try:
            doc = fitz.open(str(pdf_path))
            
            # Limit to max pages
            if len(doc) > self.max_pages:
                logger.warning(f"PDF has {len(doc)} pages, processing only first {self.max_pages}")
            
            # Analyze font characteristics
            analysis = self.analyze_font_characteristics(doc)
            
            # Identify title
            title = self.identify_title(analysis)
            
            # Establish heading hierarchy
            hierarchy = self.establish_heading_hierarchy(analysis)
            logger.info(f"Established hierarchy: {hierarchy}")
            
            # Extract headings
            headings = self.extract_headings(analysis, hierarchy)
            
            # Structure output
            result = {
                "document_title": title or "Untitled Document",
                "total_pages": min(len(doc), self.max_pages),
                "outline": []
            }
            
            # Group headings by level
            for heading in headings:
                result["outline"].append({
                    "text": heading["text"],
                    "level": heading["level"],
                    "page": heading["page"]
                })
            
            doc.close()
            
            logger.info(f"Extracted {len(result['outline'])} headings from {pdf_path.name}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {str(e)}")
            return {
                "document_title": f"Error processing {pdf_path.name}",
                "total_pages": 0,
                "outline": [],
                "error": str(e)
            }
    
    def run(self):
        """Main execution method."""
        logger.info("Starting PDF outline extraction...")
        
        # Check if input directory exists
        if not self.input_dir.exists():
            logger.error(f"Input directory {self.input_dir} does not exist")
            return
        
        # Find all PDF files
        pdf_files = list(self.input_dir.glob("*.pdf")) + list(self.input_dir.glob("*.PDF"))
        
        if not pdf_files:
            logger.warning("No PDF files found in input directory")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        for pdf_path in pdf_files:
            try:
                # Extract outline
                result = self.process_pdf(pdf_path)
                
                # Save result
                output_filename = pdf_path.stem + ".json"
                output_path = self.output_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Saved outline to: {output_path}")
                
            except Exception as e:
                logger.error(f"Failed to process {pdf_path.name}: {str(e)}")
        
        logger.info("PDF outline extraction completed")

def main():
    """Main entry point."""
    extractor = PDFOutlineExtractor()
    extractor.run()

if __name__ == "__main__":
    main()
