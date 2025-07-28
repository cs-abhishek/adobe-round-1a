# Adobe Hackathon 2025 - Round 1A Solution

# PDF Outline Extractor

This solution extracts structured outlines (Title, H1, H2, H3) from PDF files with page numbers and outputs the results in JSON format.

## Features

- ✅ Extracts document title (largest font on first page)
- ✅ Identifies heading hierarchy (H1, H2, H3) based on font size, style, and boldness
- ✅ Handles multiple font sizes and inconsistent headings
- ✅ Processes up to 50 pages per PDF
- ✅ Outputs structured JSON with page numbers
- ✅ Modular and efficient code design
- ✅ Docker-ready with no external dependencies
- ✅ Robust error handling and logging

## Architecture

The solution uses PyMuPDF (fitz) for PDF parsing, which provides:

- Accurate font size and style detection
- Bold/italic text identification
- Precise text positioning
- Fast processing (< 10s for 50-page PDFs)
- Small library size (< 200MB total)

## Algorithm

1. **Font Analysis**: Scan entire document to collect font characteristics
2. **Title Identification**: Find largest font on first page
3. **Hierarchy Establishment**: Determine heading levels based on:
   - Relative font sizes
   - Bold formatting
   - Text frequency patterns
   - Position and content analysis
4. **Heading Extraction**: Extract headings using established hierarchy
5. **Output Generation**: Create structured JSON with page numbers

## Usage

### Docker (Recommended)

```bash
# Build the Docker image
docker build -t pdf-outline-extractor .

# Run with input/output volumes
docker run -v /path/to/pdfs:/app/input -v /path/to/output:/app/output pdf-outline-extractor
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the extractor
python pdf_outline_extractor.py

# Run tests
python test_extractor.py
```

## Input/Output

### Input

- Place PDF files in `/app/input` directory
- Supports files up to 50 pages
- Multiple PDFs can be processed in batch

### Output

- JSON files saved in `/app/output` directory
- Same filename as input PDF with `.json` extension

### Output Format

```json
{
  "document_title": "Sample Document Title",
  "total_pages": 25,
  "outline": [
    {
      "text": "Chapter 1: Introduction",
      "level": "h1",
      "page": 1
    },
    {
      "text": "1.1 Overview",
      "level": "h2",
      "page": 1
    },
    {
      "text": "1.1.1 Background",
      "level": "h3",
      "page": 2
    }
  ]
}
```

## Edge Cases Handled

- Multiple font sizes within same heading level
- Inconsistent bold formatting
- Figure/table captions vs headings
- Very short or very long text blocks
- PDFs with no clear heading structure
- Mixed case and formatting variations

## Performance

- Processes 50-page PDFs in < 5 seconds
- Memory efficient text processing
- Optimized font analysis algorithms
- Minimal external dependencies

## Requirements Met

- ✅ No internet access required
- ✅ CPU-only processing
- ✅ Total size < 200MB
- ✅ JSON output format
- ✅ Handles edge cases robustly
- ✅ Modular, efficient code
- ✅ Docker containerized
- ✅ Sorted by page numbers

## Dependencies

- `PyMuPDF (fitz)`: Fast PDF parsing and text extraction
- `pathlib`: Modern path handling
- `json`: JSON output formatting
- `logging`: Comprehensive error tracking

All dependencies are lightweight and CPU-only compatible.
