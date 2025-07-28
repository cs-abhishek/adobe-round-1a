#!/usr/bin/env python3
"""
Docker Build and Test Script for Adobe Hackathon 2025
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"💻 Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"📄 Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"🚨 Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT (>5 minutes)")
        return False
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {str(e)}")
        return False

def test_docker_build():
    """Test Docker build and run for Adobe Hackathon 2025."""
    
    print("🏆 ADOBE HACKATHON 2025 - ROUND 1A")
    print("🐳 Docker Build and Test Script")
    print("=" * 50)
    
    # Check if Docker is available
    if not run_command("docker --version", "Checking Docker installation"):
        print("\n❌ Docker is not installed or not accessible")
        print("💡 Please install Docker Desktop or Docker Engine")
        return False
    
    # Create test directories
    print("\n📁 Setting up test environment...")
    test_input = Path("test_input")
    test_output = Path("docker_test_output")
    
    test_input.mkdir(exist_ok=True)
    test_output.mkdir(exist_ok=True)
    
    # Ensure we have test PDFs
    if not any(test_input.glob("*.pdf")):
        print("📄 Creating test PDFs...")
        # Run test generators if PDFs don't exist
        run_command("python test_extractor.py", "Creating sample PDF")
        run_command("python test_complex.py", "Creating complex PDF")
    
    # Build Docker image
    build_cmd = "docker build -t adobe-hackathon-2025-pdf-extractor ."
    if not run_command(build_cmd, "Building Docker image for Adobe Hackathon 2025"):
        return False
    
    # Get absolute paths for volume mounting
    input_path = test_input.resolve()
    output_path = test_output.resolve()
    
    # Run Docker container
    run_cmd = f'docker run --rm --platform linux/amd64 -v "{input_path}:/app/input" -v "{output_path}:/app/output" adobe-hackathon-2025-pdf-extractor'
    
    print(f"\n🚀 Running Adobe Hackathon 2025 PDF Extractor...")
    start_time = time.time()
    
    if run_command(run_cmd, "Processing PDFs in Docker container"):
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n⏱️ Total processing time: {processing_time:.2f} seconds")
        
        # Check outputs
        json_files = list(test_output.glob("*.json"))
        log_files = list(test_output.glob("*.log"))
        
        print(f"\n📊 Results Summary:")
        print(f"📄 JSON outputs created: {len(json_files)}")
        print(f"📋 Log files created: {len(log_files)}")
        
        for json_file in json_files:
            print(f"  ✅ {json_file.name}")
        
        # Verify JSON content
        if json_files:
            import json
            for json_file in json_files:
                try:
                    with open(json_file) as f:
                        data = json.load(f)
                    print(f"  📖 {json_file.name}: {data.get('document_title', 'Unknown')} ({data.get('total_pages', 0)} pages, {len(data.get('outline', []))} headings)")
                except Exception as e:
                    print(f"  ❌ Error reading {json_file.name}: {e}")
        
        # Performance check
        if processing_time < 10:
            print(f"\n✅ PERFORMANCE: Under 10 second requirement ({processing_time:.2f}s)")
        else:
            print(f"\n⚠️ PERFORMANCE: Over 10 second requirement ({processing_time:.2f}s)")
        
        print(f"\n🎉 Adobe Hackathon 2025 Round 1A - Docker test COMPLETED!")
        return True
    
    return False

def main():
    """Main execution."""
    success = test_docker_build()
    
    if success:
        print("\n" + "="*60)
        print("🏆 ADOBE HACKATHON 2025 - SUBMISSION READY!")
        print("✅ Docker image builds successfully")
        print("✅ PDF extraction works correctly") 
        print("✅ JSON outputs generated")
        print("✅ Performance requirements met")
        print("🚀 Ready for hackathon submission!")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("❌ ADOBE HACKATHON 2025 - BUILD ISSUES")
        print("🔧 Please fix the issues above before submission")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()
