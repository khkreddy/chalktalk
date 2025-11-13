#!/bin/bash
# Quick Start Interactive Script for PDF Abstract Extractor

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║    PDF Abstract Extractor - Quick Start Guide             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Function to pause and wait for user
pause() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Function to run a command with explanation
run_command() {
    echo "Running: $1"
    echo "───────────────────────────────────────────────────────────"
    eval "$1"
    local exit_code=$?
    echo "───────────────────────────────────────────────────────────"
    return $exit_code
}

# Step 1: Check Python
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION is installed"
else
    echo "✗ Python 3 not found!"
    echo ""
    echo "Please install Python 3:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip"
    exit 1
fi
pause

# Step 2: Check dependencies
echo "Step 2: Checking required libraries..."
run_command "python3 test_installation.py"
if [ $? -ne 0 ]; then
    echo ""
    echo "Dependencies need to be installed."
    read -p "Install now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_command "pip3 install pdfplumber PyMuPDF"
        echo ""
        echo "Installation complete! Running test again..."
        run_command "python3 test_installation.py"
    else
        echo "Please install dependencies manually:"
        echo "  pip3 install pdfplumber PyMuPDF"
        exit 1
    fi
fi
pause

# Step 3: Get PDF directory
echo "Step 3: Locate your PDF files"
echo ""
echo "Where are your PDF files located?"
echo ""
echo "Examples:"
echo "  - /mnt/c/Users/YourName/Documents/Papers"
echo "  - /mnt/c/Downloads"
echo "  - /home/user/documents/pdfs"
echo ""
read -p "Enter the full path to your PDF directory: " PDF_DIR

if [ ! -d "$PDF_DIR" ]; then
    echo ""
    echo "✗ Directory not found: $PDF_DIR"
    echo ""
    echo "Tips for Windows paths in WSL:"
    echo "  Windows: C:\\Users\\John\\Documents\\Papers"
    echo "  WSL:     /mnt/c/Users/John/Documents/Papers"
    echo ""
    exit 1
fi

# Check for PDFs
PDF_COUNT=$(find "$PDF_DIR" -maxdepth 1 -iname "*.pdf" 2>/dev/null | wc -l)
if [ $PDF_COUNT -eq 0 ]; then
    echo ""
    echo "⚠ No PDF files found in: $PDF_DIR"
    echo ""
    read -p "Search subdirectories? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PDF_COUNT=$(find "$PDF_DIR" -iname "*.pdf" 2>/dev/null | wc -l)
        echo "Found $PDF_COUNT PDF files (including subdirectories)"
        RECURSIVE="-r"
    else
        echo "No PDFs to process. Exiting."
        exit 1
    fi
else
    echo "✓ Found $PDF_COUNT PDF files in this directory"
    RECURSIVE=""
fi
pause

# Step 4: Choose version
echo "Step 4: Choose extraction method"
echo ""
echo "1) Basic Version (Fast, simple)"
echo "2) Advanced Version (Best accuracy, more features) [RECOMMENDED]"
echo ""
read -p "Choose option (1 or 2): " -n 1 -r
echo ""

case $REPLY in
    1)
        SCRIPT="pdf_abstract_extractor_basic.py"
        echo "Selected: Basic Version"
        ;;
    2)
        SCRIPT="pdf_abstract_extractor_advanced.py"
        echo "Selected: Advanced Version"
        ;;
    *)
        echo "Invalid option. Using Advanced Version."
        SCRIPT="pdf_abstract_extractor_advanced.py"
        ;;
esac
pause

# Step 5: Choose output format (for advanced only)
OUTPUT_FORMAT=""
if [ "$SCRIPT" = "pdf_abstract_extractor_advanced.py" ]; then
    echo "Step 5: Choose output format"
    echo ""
    echo "1) Text (.txt) - Easy to read"
    echo "2) JSON (.json) - For programming"
    echo "3) CSV (.csv) - For Excel/spreadsheets"
    echo ""
    read -p "Choose option (1, 2, or 3): " -n 1 -r
    echo ""

    case $REPLY in
        1)
            OUTPUT_FILE="pdf_abstracts.txt"
            OUTPUT_FORMAT="--format txt"
            ;;
        2)
            OUTPUT_FILE="pdf_abstracts.json"
            OUTPUT_FORMAT="--format json"
            ;;
        3)
            OUTPUT_FILE="pdf_abstracts.csv"
            OUTPUT_FORMAT="--format csv"
            ;;
        *)
            OUTPUT_FILE="pdf_abstracts.txt"
            OUTPUT_FORMAT="--format txt"
            ;;
    esac
else
    OUTPUT_FILE="pdf_abstracts.txt"
fi
pause

# Step 6: Run extraction
echo "Step 6: Running extraction..."
echo ""
echo "Processing PDFs from: $PDF_DIR"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "This may take a few minutes depending on the number of files..."
echo ""

COMMAND="python3 $SCRIPT \"$PDF_DIR\" -o \"$OUTPUT_FILE\" $RECURSIVE $OUTPUT_FORMAT -v"

echo "Command: $COMMAND"
echo ""
pause

eval $COMMAND

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                   EXTRACTION COMPLETE!                     ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Output saved to: $OUTPUT_FILE"
    echo ""
    echo "View results:"

    if [[ $OUTPUT_FILE == *.txt ]]; then
        echo "  cat $OUTPUT_FILE"
        echo "  less $OUTPUT_FILE"
        echo "  notepad.exe $OUTPUT_FILE"
    elif [[ $OUTPUT_FILE == *.json ]]; then
        echo "  python3 -m json.tool $OUTPUT_FILE | less"
        echo "  code $OUTPUT_FILE"
    elif [[ $OUTPUT_FILE == *.csv ]]; then
        echo "  excel.exe $OUTPUT_FILE"
        echo "  cat $OUTPUT_FILE"
    fi

    echo ""
    read -p "Open output file now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ $OUTPUT_FILE == *.txt ]]; then
            less "$OUTPUT_FILE"
        elif [[ $OUTPUT_FILE == *.json ]]; then
            python3 -m json.tool "$OUTPUT_FILE" | less
        elif [[ $OUTPUT_FILE == *.csv ]]; then
            cat "$OUTPUT_FILE" | less
        fi
    fi
else
    echo ""
    echo "✗ Extraction failed. Please check the error messages above."
fi

echo ""
echo "Thank you for using PDF Abstract Extractor!"
echo ""
