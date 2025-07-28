# Build and test script for Windows PowerShell

Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t pdf-outline-extractor .

Write-Host "Creating test directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "test_input", "test_output"

Write-Host "Running test extractor to create sample PDF..." -ForegroundColor Green
python test_extractor.py

Write-Host "Running Docker container with test data..." -ForegroundColor Green
docker run -v "${PWD}/test_input:/app/input" -v "${PWD}/test_output:/app/output" pdf-outline-extractor

Write-Host "Test completed! Check test_output/ for results." -ForegroundColor Green
