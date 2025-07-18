#!/bin/bash
# Setup script for Google AI Overview Scraper

echo "🚀 Setting up Google AI Overview Scraper..."
echo "============================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the proj2 directory"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

if [ $? -eq 0 ]; then
    echo "✅ Playwright browser installed successfully"
else
    echo "⚠️  Playwright browser installation failed"
    echo "   You can try: python -m playwright install chromium"
fi

# Create outputs directory
echo "📁 Creating outputs directory..."
mkdir -p outputs
echo "✅ Outputs directory created"

# Run validation tests
echo "🧪 Running validation tests..."
python validate.py

if [ $? -eq 0 ]; then
    echo "✅ All validation tests passed!"
else
    echo "❌ Some validation tests failed"
fi

echo ""
echo "============================================="
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Test basic functionality:"
echo "     python scrape_ai.py 'what is machine learning'"
echo ""
echo "  2. Use in your Python code:"
echo "     from google_ai_scraper import get_google_ai_overview"
echo "     result = get_google_ai_overview('your query')"
echo ""
echo "  3. Check examples:"
echo "     python examples.py"
echo ""
echo "📚 Read README.md for detailed usage instructions"