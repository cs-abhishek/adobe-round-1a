#!/usr/bin/env python3
"""
Performance test for PDF Outline Extractor
Tests speed and memory efficiency
"""

import time
import psutil
import os
from pathlib import Path
from pdf_outline_extractor import PDFOutlineExtractor

def measure_performance():
    """Measure processing performance."""
    print("=== PERFORMANCE TEST ===\n")
    
    # Setup
    test_input = Path("test_input")
    test_output = Path("test_output") 
    
    # Initialize extractor
    extractor = PDFOutlineExtractor(input_dir=test_input, output_dir=test_output)
    
    # Get PDF files
    pdf_files = list(test_input.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files to test\n")
    
    total_time = 0
    total_pages = 0
    
    # Memory baseline
    process = psutil.Process(os.getpid())
    baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    for pdf_path in pdf_files:
        print(f"Testing: {pdf_path.name}")
        
        # Measure processing time
        start_time = time.time()
        result = extractor.process_pdf(pdf_path)
        end_time = time.time()
        
        processing_time = end_time - start_time
        total_time += processing_time
        total_pages += result["total_pages"]
        
        # Memory usage
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_usage = current_memory - baseline_memory
        
        print(f"  ⏱️  Processing Time: {processing_time:.3f}s")
        print(f"  📄 Pages: {result['total_pages']}")
        print(f"  📋 Headings: {len(result['outline'])}")
        print(f"  💾 Memory Usage: {memory_usage:.1f}MB")
        print(f"  🚀 Speed: {result['total_pages']/processing_time:.1f} pages/second")
        print()
    
    # Summary
    print("=== PERFORMANCE SUMMARY ===")
    print(f"Total Files: {len(pdf_files)}")
    print(f"Total Pages: {total_pages}")
    print(f"Total Time: {total_time:.3f}s")
    print(f"Average Speed: {total_pages/total_time:.1f} pages/second")
    print(f"Memory Efficient: {memory_usage:.1f}MB peak usage")
    
    # Check requirements
    max_time_per_50_pages = 10.0  # seconds
    estimated_50_page_time = (total_time / total_pages) * 50
    
    print("\n=== REQUIREMENT CHECK ===")
    print(f"Estimated 50-page processing time: {estimated_50_page_time:.2f}s")
    
    if estimated_50_page_time <= max_time_per_50_pages:
        print("✅ SPEED REQUIREMENT MET: <10s for 50-page PDF")
    else:
        print("❌ SPEED REQUIREMENT NOT MET")
    
    if memory_usage <= 200:  # MB
        print("✅ MEMORY REQUIREMENT MET: <200MB usage")
    else:
        print("❌ MEMORY REQUIREMENT NOT MET")
    
    print("\n🎯 Performance test completed!")

if __name__ == "__main__":
    measure_performance()
