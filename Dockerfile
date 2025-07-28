# Dockerfile for Adobe Hackathon 2025 Round 1A
# Goal: Run a Python script that extracts title and headings from PDFs placed in /app/input
# Constraints:
# - Must run on linux/amd64
# - No GPU, no internet
# - Output JSON in /app/output
# - All Python dependencies must be installed inside Docker

FROM python:3.10-slim

# Set platform for cross-compatibility
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies (no internet access during runtime)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all local files to /app
COPY . .

# Create input and output directories with proper permissions
RUN mkdir -p /app/input /app/output && \
    chmod 755 /app/input /app/output

# Rename the main script to main.py for hackathon requirements
RUN cp pdf_outline_extractor.py main.py

# Run main.py on container start
CMD ["python", "main.py"]
