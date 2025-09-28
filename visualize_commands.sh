#!/bin/bash

echo "========================================"
echo "AIPPLY API VISUALIZATION COMMANDS"
echo "========================================"

echo ""
echo "1. Running Code Structure Analysis..."
python3 visualize_code.py

echo ""
echo "2. Creating Directory Tree..."
tree -a

echo ""
echo "3. Showing File Sizes..."
find . -name "*.py" -exec ls -lh {} \; | awk '{print $9 ": " $5}'

echo ""
echo "4. Running FastAPI Documentation..."
echo "Starting FastAPI server for interactive docs..."
echo "Visit: http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
python3 main.py
