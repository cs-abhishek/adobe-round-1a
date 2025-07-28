#!/usr/bin/env python3
"""
Adobe Hackathon 2025 Round 1A - Final Submission Validator
Comprehensive test of the PDF outline extraction solution
"""

import json
import time
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_submission():
    """Validate the Adobe Hackathon 2025 submission."""
    
    print("🏆 ADOBE HACKATHON 2025 - ROUND 1A")
    print("📄 PDF Outline Extractor - Final Validation")
    print("=" * 60)
    
    # Test local execution
    logger.info("🧪 Testing local execution...")
    
    try:
        # Import and test the main extractor
        from pdf_outline_extractor import PDFOutlineExtractor
        
        # Setup test environment
        test_input = Path("test_input")
        test_output = Path("final_test_output")
        test_output.mkdir(exist_ok=True)
        
        # Create test PDFs if they don't exist
        if not any(test_input.glob("*.pdf")):
            logger.info("📄 Creating test PDFs...")
            exec(open("test_extractor.py").read())
            exec(open("test_complex.py").read())
        
        # Initialize extractor
        extractor = PDFOutlineExtractor(input_dir=test_input, output_dir=test_output)
        
        # Process PDFs and measure performance
        pdf_files = list(test_input.glob("*.pdf"))
        logger.info(f"📁 Found {len(pdf_files)} PDF files to process")
        
        total_time = 0
        total_pages = 0
        results = []
        
        for pdf_path in pdf_files:
            logger.info(f"🔄 Processing: {pdf_path.name}")
            
            start_time = time.time()
            result = extractor.process_pdf(pdf_path)
            end_time = time.time()
            
            processing_time = end_time - start_time
            total_time += processing_time
            total_pages += result["total_pages"]
            
            results.append({
                "file": pdf_path.name,
                "time": processing_time,
                "pages": result["total_pages"],
                "headings": len(result["outline"]),
                "title": result["document_title"]
            })
            
            # Save individual result
            output_file = test_output / f"{pdf_path.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Performance analysis
        avg_time_per_page = total_time / total_pages if total_pages > 0 else 0
        estimated_50_page_time = avg_time_per_page * 50
        
        print("\n📊 PERFORMANCE RESULTS")
        print("-" * 40)
        for result in results:
            print(f"📄 {result['file']}")
            print(f"   ⏱️  Time: {result['time']:.3f}s")
            print(f"   📖 Pages: {result['pages']}")
            print(f"   📋 Headings: {result['headings']}")
            print(f"   📑 Title: {result['title']}")
            print(f"   🚀 Speed: {result['pages']/result['time']:.1f} pages/sec")
            print()
        
        print(f"📈 OVERALL PERFORMANCE")
        print(f"   📄 Total pages: {total_pages}")
        print(f"   ⏱️  Total time: {total_time:.3f}s")
        print(f"   🚀 Average speed: {total_pages/total_time:.1f} pages/sec")
        print(f"   📊 50-page estimate: {estimated_50_page_time:.2f}s")
        
        # Requirement checks
        print("\n✅ REQUIREMENT VALIDATION")
        print("-" * 40)
        
        requirements_met = True
        
        # Speed requirement
        if estimated_50_page_time <= 10.0:
            print("✅ Speed: Under 10s for 50-page PDF")
        else:
            print("❌ Speed: Over 10s for 50-page PDF")
            requirements_met = False
        
        # Output format check
        json_files = list(test_output.glob("*.json"))
        if json_files:
            print("✅ JSON Output: Valid format generated")
            
            # Validate JSON structure
            for json_file in json_files:
                with open(json_file) as f:
                    data = json.load(f)
                
                required_fields = ["document_title", "total_pages", "outline"]
                if all(field in data for field in required_fields):
                    print(f"✅ JSON Structure: {json_file.name} has required fields")
                else:
                    print(f"❌ JSON Structure: {json_file.name} missing required fields")
                    requirements_met = False
                
                # Check outline structure
                for item in data.get("outline", []):
                    outline_fields = ["text", "level", "page"]
                    if not all(field in item for field in outline_fields):
                        print(f"❌ Outline Structure: Missing fields in {json_file.name}")
                        requirements_met = False
                        break
                else:
                    print(f"✅ Outline Structure: {json_file.name} properly formatted")
        else:
            print("❌ JSON Output: No output files generated")
            requirements_met = False
        
        # Docker file check
        dockerfile = Path("Dockerfile")
        if dockerfile.exists():
            print("✅ Docker: Dockerfile present")
            
            # Check Dockerfile content
            with open(dockerfile) as f:
                content = f.read()
            
            if "python:3.10-slim" in content:
                print("✅ Docker: Uses Python 3.10 slim base")
            else:
                print("⚠️  Docker: Different Python version specified")
            
            if "main.py" in content:
                print("✅ Docker: Runs main.py as specified")
            else:
                print("❌ Docker: Does not run main.py")
                requirements_met = False
        else:
            print("❌ Docker: Dockerfile not found")
            requirements_met = False
        
        # Main.py check
        main_py = Path("main.py")
        if main_py.exists():
            print("✅ Entry Point: main.py exists")
        else:
            print("❌ Entry Point: main.py not found")
            requirements_met = False
        
        # Final verdict
        print("\n" + "=" * 60)
        if requirements_met:
            print("🎉 ADOBE HACKATHON 2025 - SUBMISSION VALIDATED!")
            print("✅ All requirements met")
            print("🚀 Ready for final submission")
            
            # Create submission summary
            summary = {
                "hackathon": "Adobe Hackathon 2025 - Round 1A",
                "challenge": "PDF Outline Extraction",
                "status": "VALIDATED",
                "performance": {
                    "total_time": total_time,
                    "total_pages": total_pages,
                    "avg_speed": total_pages/total_time,
                    "estimated_50_page_time": estimated_50_page_time
                },
                "outputs": [{"file": r["file"], "headings": r["headings"]} for r in results],
                "requirements_met": requirements_met
            }
            
            with open(test_output / "submission_summary.json", 'w') as f:
                json.dump(summary, f, indent=2)
            
            print("📄 Submission summary saved to submission_summary.json")
        else:
            print("❌ ADOBE HACKATHON 2025 - VALIDATION FAILED")
            print("🔧 Please fix the issues above")
        
        print("=" * 60)
        return requirements_met
        
    except Exception as e:
        logger.error(f"💥 Validation failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = validate_submission()
    exit(0 if success else 1)
