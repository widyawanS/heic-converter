# Gunakan Python 3.11 slim (lebih ringan)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy aplikasi
COPY . .

# Create necessary directories
RUN mkdir -p uploads converted logs && \
    chmod 777 uploads converted logs

# Expose port (Heroku akan override ini dengan $PORT)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run aplikasi
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
