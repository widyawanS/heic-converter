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

# Copy app code
COPY app/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories for runtime data
RUN mkdir -p data/uploads data/converted logs && \
    chmod 777 data/uploads data/converted logs

# Expose port (Heroku will override this with $PORT)
EXPOSE 8000

# Run application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
