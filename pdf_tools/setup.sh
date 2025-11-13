#!/bin/bash
# PDF Abstract Extractor - Installation and Test Script
# Run this script to install dependencies and test the tools

echo "================================================"
echo "PDF Abstract Extractor - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3:"
    echo "  sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

echo ""
echo "Installing dependencies..."
pip3 install pdfplumber PyMuPDF --quiet

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Installation failed. Try manually:"
    echo "  pip3 install pdfplumber PyMuPDF"
    exit 1
fi

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Usage Examples:"
echo ""
echo "1. Basic extraction (simple):"
echo "   python3 pdf_abstract_extractor_basic.py /path/to/pdfs"
echo ""
echo "2. Advanced extraction (best accuracy):"
echo "   python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -v"
echo ""
echo "3. Export to JSON:"
echo "   python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -o output.json --format json"
echo ""
echo "4. Export to CSV (for Excel):"
echo "   python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -o output.csv --format csv"
echo ""
echo "For Windows paths in WSL, use /mnt/c/ format:"
echo "   python3 pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers"
echo ""
echo "================================================"
echo "Ready to use!"
echo "================================================"
