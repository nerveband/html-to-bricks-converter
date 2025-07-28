#!/bin/bash

# HTML to Bricks Builder JSON Converter - Startup Script
# This script sets up the environment and starts the Streamlit application

echo "🧱 HTML to Bricks Builder JSON Converter"
echo "========================================="

# Set the API key
export CEREBRAS_API_KEY="csk-rd5w454692pm56vwkwykvffprvdwhkrjcjmtycn958x3k82j"

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "
import streamlit
import cerebras.cloud.sdk
import pyperclip
print('✅ All dependencies are available')
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Dependencies missing. Installing..."
    pip install -r requirements.txt
fi

echo "🚀 Starting Streamlit application..."
echo "💡 Tip: The app will open in your default web browser"
echo "🔗 Manual URL: http://localhost:8501"
echo ""

# Start the Streamlit app
streamlit run bricks_converter.py --server.port=8501 --server.address=localhost