# PDF Abstract Extractor - Complete Execution Guide

This guide provides detailed step-by-step instructions for running the PDF Abstract Extractor on your WSL Linux system.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Understanding Windows Paths in WSL](#understanding-windows-paths-in-wsl)
4. [Running the Tools](#running-the-tools)
5. [Real-World Examples](#real-world-examples)
6. [Viewing Results](#viewing-results)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Check Your Environment

Open your WSL terminal and run:

```bash
# Check Python version (should be 3.7+)
python3 --version

# Check pip
pip3 --version

# Navigate to the tools directory
cd /home/user/chalktalk/pdf_tools
```

If Python is not installed:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to the directory
cd /home/user/chalktalk/pdf_tools

# Run the setup script
./setup.sh
```

### Option 2: Manual Installation

```bash
# Navigate to the directory
cd /home/user/chalktalk/pdf_tools

# Install dependencies
pip3 install -r requirements.txt

# Or install individually
pip3 install pdfplumber PyMuPDF
```

### Verify Installation

```bash
# Run the test script
python3 test_installation.py
```

You should see:
```
✓ ALL TESTS PASSED!
Your installation is complete and ready to use.
```

---

## Understanding Windows Paths in WSL

In WSL, your Windows drives are mounted under `/mnt/`:

| Windows Path | WSL Path |
|-------------|----------|
| `C:\Users\John\Documents\Papers` | `/mnt/c/Users/John/Documents/Papers` |
| `D:\Research\PDFs` | `/mnt/d/Research/PDFs` |
| `C:\Downloads` | `/mnt/c/Downloads` |

### Testing Path Access

```bash
# List contents of a Windows directory from WSL
ls /mnt/c/Users/YourName/Documents

# Check if PDFs are accessible
ls /mnt/c/Users/YourName/Documents/Papers/*.pdf
```

**Replace `YourName` with your actual Windows username!**

---

## Running the Tools

### Basic Version (Recommended for First-Time Users)

#### Syntax
```bash
python3 pdf_abstract_extractor_basic.py <directory> [options]
```

#### Options
- `-o, --output <file>` : Output file path (default: `pdf_abstracts.txt`)
- `-r, --recursive` : Search subdirectories
- `-v, --verbose` : Show detailed progress

#### Simple Examples

**1. Process PDFs in current directory:**
```bash
python3 pdf_abstract_extractor_basic.py .
```

**2. Process a specific Windows folder:**
```bash
python3 pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers
```

**3. With custom output file:**
```bash
python3 pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers \
  -o my_research_abstracts.txt
```

**4. Search subdirectories with verbose output:**
```bash
python3 pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers \
  -r -v
```

---

### Advanced Version (Best Accuracy & More Features)

#### Syntax
```bash
python3 pdf_abstract_extractor_advanced.py <directory> [options]
```

#### Options
- `-o, --output <file>` : Output file path
- `--format {txt,json,csv}` : Output format (default: txt)
- `-r, --recursive` : Search subdirectories
- `-v, --verbose` : Show detailed progress
- `--min-confidence <0.0-1.0>` : Minimum confidence threshold

#### Advanced Examples

**1. Basic usage with verbose output:**
```bash
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers -v
```

**2. Export to JSON (great for programming):**
```bash
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  -o research_abstracts.json \
  --format json \
  -r -v
```

**3. Export to CSV (open in Excel):**
```bash
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  -o research_abstracts.csv \
  --format csv \
  -r
```

**4. Only high-confidence extractions:**
```bash
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  --min-confidence 0.7 \
  -v
```

**5. Complete workflow - generate all formats:**
```bash
# Text format for reading
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  -o abstracts.txt --format txt -r

# JSON format for programming
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  -o abstracts.json --format json -r

# CSV format for Excel
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  -o abstracts.csv --format csv -r
```

---

## Real-World Examples

### Example 1: Single Directory

**Scenario:** You have PDFs in `C:\Users\John\Documents\ResearchPapers`

```bash
cd /home/user/chalktalk/pdf_tools

python3 pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/John/Documents/ResearchPapers \
  -o research_catalog.txt \
  -v
```

**Output:**
```
[2025-11-13 10:30:45] INFO: Starting processing of directory: /mnt/c/Users/John/Documents/ResearchPapers
[2025-11-13 10:30:45] INFO: Found 25 PDF files
[2025-11-13 10:30:46] INFO: Processing [1/25]: paper1.pdf
[2025-11-13 10:30:47] INFO: Processing [2/25]: paper2.pdf
...
================================================================================
EXTRACTION COMPLETE
================================================================================
Total Files Processed: 25
Successful Extractions: 22
Failed Extractions: 3
Success Rate: 88.0%
```

### Example 2: Nested Directories

**Scenario:** Your papers are organized in subdirectories:
```
C:\Research\
  ├── MachineLearning\
  ├── NeuralNetworks\
  └── ComputerVision\
```

```bash
python3 pdf_abstract_extractor_advanced.py \
  /mnt/c/Research \
  -o all_research.json \
  --format json \
  --recursive \
  --verbose
```

### Example 3: Filter by Confidence

**Scenario:** Only want high-quality extractions

```bash
python3 pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/John/Documents/Papers \
  -o high_quality_abstracts.txt \
  --min-confidence 0.8 \
  -r -v
```

### Example 4: Large Collection

**Scenario:** 500+ PDFs, want to process in background

```bash
# Run in background and save output to log
nohup python3 pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/John/Documents/AllPapers \
  -o complete_catalog.json \
  --format json \
  --recursive \
  --verbose > extraction.log 2>&1 &

# Check progress
tail -f extraction.log

# Find the process
ps aux | grep pdf_abstract_extractor

# Kill if needed
kill <process_id>
```

---

## Viewing Results

### Text Output (`.txt`)

```bash
# View in terminal
cat pdf_abstracts.txt

# View with pagination
less pdf_abstracts.txt

# Search for specific term
grep -i "machine learning" pdf_abstracts.txt

# Open in Windows Notepad from WSL
notepad.exe pdf_abstracts.txt
```

### JSON Output (`.json`)

```bash
# View formatted JSON
python3 -m json.tool abstracts.json | less

# Search JSON
cat abstracts.json | grep -i "neural"

# Open in Windows with default JSON viewer
explorer.exe abstracts.json
```

**Quick Python script to search JSON:**
```python
import json

with open('abstracts.json') as f:
    data = json.load(f)

# Search for keyword
keyword = "machine learning"
for abstract in data['abstracts']:
    if keyword.lower() in abstract['abstract'].lower():
        print(f"\nFile: {abstract['filename']}")
        print(f"Confidence: {abstract['confidence']}")
        print(f"Abstract: {abstract['abstract'][:200]}...")
```

### CSV Output (`.csv`)

```bash
# Open in Excel from WSL
excel.exe abstracts.csv

# Or copy to Windows Downloads folder
cp abstracts.csv /mnt/c/Users/YourName/Downloads/

# View first 10 rows in terminal
head -n 10 abstracts.csv
```

---

## Troubleshooting

### Problem 1: "No module named 'pdfplumber'"

**Solution:**
```bash
pip3 install pdfplumber PyMuPDF
```

### Problem 2: "Permission denied"

**Solution:**
```bash
# Make scripts executable
chmod +x pdf_abstract_extractor_basic.py
chmod +x pdf_abstract_extractor_advanced.py

# Or run with python3 explicitly
python3 pdf_abstract_extractor_basic.py /path/to/pdfs
```

### Problem 3: "Directory does not exist"

**Cause:** Wrong path format

**Solution:**
```bash
# WRONG (Windows format):
python3 pdf_abstract_extractor_basic.py C:\Users\John\Documents\Papers

# CORRECT (WSL format):
python3 pdf_abstract_extractor_basic.py /mnt/c/Users/John/Documents/Papers

# Verify path exists first:
ls /mnt/c/Users/John/Documents/Papers
```

### Problem 4: "No PDF files found"

**Solution:**
```bash
# Check if PDFs are in the directory
ls /mnt/c/Users/YourName/Documents/Papers/*.pdf

# Make sure you're using -r for subdirectories
python3 pdf_abstract_extractor_basic.py /path/to/pdfs -r -v

# Check file permissions
ls -la /mnt/c/Users/YourName/Documents/Papers/
```

### Problem 5: Low Success Rate

**Solutions:**

1. **Use Advanced Version:**
```bash
python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -v
```

2. **Check PDF Types:**
```bash
# Some PDFs might be scanned images, not text
file /path/to/pdfs/*.pdf
```

3. **Check Failed Files:**
Look at the summary output to see which files failed and why.

### Problem 6: Script Runs But No Output File

**Solution:**
```bash
# Check current directory
pwd

# Specify full output path
python3 pdf_abstract_extractor_basic.py /path/to/pdfs \
  -o /home/user/chalktalk/pdf_tools/output.txt

# Check if file was created
ls -la *.txt
```

### Problem 7: "Killed" or "Out of Memory"

**Cause:** Processing too many large PDFs

**Solution:**
```bash
# Process in smaller batches
python3 pdf_abstract_extractor_basic.py /path/to/pdfs/batch1 -o batch1.txt
python3 pdf_abstract_extractor_basic.py /path/to/pdfs/batch2 -o batch2.txt

# Combine results later
cat batch1.txt batch2.txt > combined.txt
```

---

## Quick Reference Commands

### Installation
```bash
cd /home/user/chalktalk/pdf_tools
pip3 install -r requirements.txt
python3 test_installation.py
```

### Basic Extraction
```bash
python3 pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers -v
```

### Advanced Extraction (Recommended)
```bash
python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers -r -v
```

### Export to JSON
```bash
python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -o output.json --format json -r
```

### Export to CSV (Excel)
```bash
python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -o output.csv --format csv -r
```

### High Confidence Only
```bash
python3 pdf_abstract_extractor_advanced.py /path/to/pdfs --min-confidence 0.8 -v
```

---

## Getting Help

### View Built-in Help
```bash
# Basic version help
python3 pdf_abstract_extractor_basic.py --help

# Advanced version help
python3 pdf_abstract_extractor_advanced.py --help
```

### Check Versions
```bash
python3 --version
pip3 list | grep pdfplumber
pip3 list | grep PyMuPDF
```

---

## Next Steps

1. **Test with a small directory first:**
   ```bash
   python3 pdf_abstract_extractor_advanced.py /path/to/test/folder -v
   ```

2. **Process your full collection:**
   ```bash
   python3 pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
     -o research_catalog.json --format json -r -v
   ```

3. **Open results in your preferred tool:**
   - Text files: Any text editor
   - JSON files: VS Code, programming scripts
   - CSV files: Excel, Google Sheets

Happy organizing! 🎉
