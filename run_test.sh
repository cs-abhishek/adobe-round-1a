#!/bin/bash

# Build and test script for PDF Outline Extractor

echo "Building Docker image..."
docker build -t pdf-outline-extractor .

echo "Creating test directories..."
mkdir -p test_input test_output

echo "Running test extractor to create sample PDF..."
python test_extractor.py

echo "Running Docker container with test data..."
docker run -v "$(pwd)/test_input:/app/input" -v "$(pwd)/test_output:/app/output" pdf-outline-extractor

echo "Test completed! Check test_output/ for results."
