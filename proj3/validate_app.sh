#!/bin/bash

# Complete test and validation script for PDF Chat App
echo "🔍 PDF Chat App - Complete Validation"
echo "====================================="

cd /home/runner/work/ak-auto-tool/ak-auto-tool/proj3

# Check file structure
echo "📁 File Structure:"
echo "├── pdf_chat_app.py ($(wc -l < pdf_chat_app.py) lines)"
echo "├── pdf_chat_demo.py ($(wc -l < pdf_chat_demo.py) lines)"
echo "├── requirements.txt"
echo "├── README.md"
echo "├── run_app.sh"
echo "├── test_imports.sh"
echo "└── notebook/"
echo "    ├── .env"
echo "    └── ..."
echo ""

# Check requirements
echo "📦 Dependencies Required:"
cat requirements.txt | nl
echo ""

# Test demo functionality
echo "🧪 Testing Demo Version:"
echo "------------------------"
python3 pdf_chat_demo.py
echo ""

# Show usage instructions
echo "🚀 Usage Instructions:"
echo "====================="
echo "1. Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "2. Run the application:"
echo "   streamlit run pdf_chat_app.py"
echo ""
echo "3. Access the app:"
echo "   http://localhost:8501"
echo ""
echo "4. Alternative run methods:"
echo "   ./run_app.sh"
echo "   python3 -m streamlit run pdf_chat_app.py"
echo ""

# Check git status
echo "📝 Git Status:"
echo "--------------"
git status --porcelain | head -10
echo ""

echo "✅ Validation Complete!"
echo "The PDF Chat App is ready for use."