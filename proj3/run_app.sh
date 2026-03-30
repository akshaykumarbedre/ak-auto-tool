#!/bin/bash

# Simple run script for the PDF Chat App
echo "🚀 Starting PDF Chat App..."

cd /home/runner/work/ak-auto-tool/ak-auto-tool/proj3

# Check if we're in the right directory
if [ ! -f "pdf_chat_app.py" ]; then
    echo "❌ Error: pdf_chat_app.py not found in current directory"
    exit 1
fi

# Try to run the app
echo "📄 Attempting to run Streamlit app..."
echo "🔗 If successful, the app will be available at http://localhost:8501"
echo ""

# Try different ways to run streamlit
if command -v streamlit &> /dev/null; then
    streamlit run pdf_chat_app.py
elif python3 -m streamlit --help &> /dev/null; then
    python3 -m streamlit run pdf_chat_app.py
else
    echo "⚠️  Streamlit not found. Installing dependencies first..."
    echo "📦 You may need to run: pip install streamlit"
    echo "🔧 Then try: streamlit run pdf_chat_app.py"
fi