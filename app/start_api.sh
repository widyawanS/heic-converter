#!/bin/bash

# HEIC to Image Converter API - Startup Script

PROJECT_DIR="/home/sigitdev"
VENV_DIR="$PROJECT_DIR/venv"
PORT="${1:-8000}"
HOST="${2:-127.0.0.1}"

echo "╔══════════════════════════════════════════════════╗"
echo "║  HEIC to Image Converter API - Startup Script   ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found at $VENV_DIR"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check dependencies
echo "✓ Checking dependencies..."
pip install -q -r "$PROJECT_DIR/requirements.txt"

# Create necessary directories
echo "✓ Creating necessary directories..."
mkdir -p "$PROJECT_DIR/uploads"
mkdir -p "$PROJECT_DIR/converted"
mkdir -p "$PROJECT_DIR/logs"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║          API Server Starting...                 ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  Host: $HOST                                  ║"
echo "║  Port: $PORT                                      ║"
echo "║  Docs: http://$HOST:$PORT/docs                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Start the API server
cd "$PROJECT_DIR"
uvicorn api:app --host "$HOST" --port "$PORT" --reload

deactivate
