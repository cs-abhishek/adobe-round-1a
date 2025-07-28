# Build and test script for Windows PowerShell

Write-Host "=== Adobe Hackathon 2025 - PDF Outline Extractor ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t pdf-outline-extractor .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Creating test directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "test_input", "docker_output" | Out-Null

Write-Host "Creating test PDFs..." -ForegroundColor Green
python test_extractor.py | Out-Null
python test_complex.py | Out-Null

Write-Host "Running Docker container with test data..." -ForegroundColor Green
$inputPath = (Resolve-Path "test_input").Path
$outputPath = (Resolve-Path "docker_output").Path

docker run --rm -v "${inputPath}:/app/input" -v "${outputPath}:/app/output" pdf-outline-extractor

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Test Results ===" -ForegroundColor Cyan
    Write-Host "Docker container executed successfully!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Output files created:" -ForegroundColor Yellow
    Get-ChildItem "docker_output" -Filter "*.json" | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor White
        
        # Show first few lines of each output
        $content = Get-Content $_.FullName | ConvertFrom-Json
        Write-Host "    Title: $($content.document_title)" -ForegroundColor Gray
        Write-Host "    Pages: $($content.total_pages)" -ForegroundColor Gray
        Write-Host "    Headings: $($content.outline.Count)" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "Test completed successfully! 🎉" -ForegroundColor Green
} else {
    Write-Host "Docker container failed!" -ForegroundColor Red
    exit 1
}
