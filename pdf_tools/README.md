# PDF Abstract Extractor

Automatically extract abstract sections from PDF files and compile them into a searchable catalog. Perfect for organizing research papers, technical documents, and academic publications on your WSL Linux system.

## Overview

This tool helps you:
- **Organize** your PDF collection systematically
- **Know** what's in each file without opening them
- **Search** through abstracts to find relevant papers quickly
- **Catalog** papers with metadata (filename, path, page number)

## Two Versions Available

### 1. Basic Version (`pdf_abstract_extractor_basic.py`)
**Best for:** Quick setup, simple needs, academic papers with standard formatting

**Features:**
- Fast and lightweight
- Pattern-based extraction
- Text output format
- Easy to understand and modify

**Installation:**
```bash
pip install pdfplumber
```

### 2. Advanced Version (`pdf_abstract_extractor_advanced.py`)
**Best for:** Better accuracy, diverse PDF formats, multiple export options

**Features:**
- Multiple extraction strategies (keyword, position, font analysis, metadata)
- Confidence scoring for each extraction
- Export to TXT, JSON, or CSV formats
- Detailed extraction statistics
- Minimum confidence filtering

**Installation:**
```bash
pip install pdfplumber PyMuPDF
```

Or use the requirements file:
```bash
cd pdf_tools
pip install -r requirements.txt
```

## Quick Start

### For WSL Users (Windows Paths)

Your Windows drives are accessible under `/mnt/` in WSL:
- `C:\Users\YourName\Documents\Papers` → `/mnt/c/Users/YourName/Documents/Papers`
- `D:\Research\PDFs` → `/mnt/d/Research/PDFs`

### Basic Usage

**Extract abstracts from a folder:**
```bash
python pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers
```

This creates `pdf_abstracts.txt` in your current directory.

**Specify output file:**
```bash
python pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers -o my_abstracts.txt
```

**Search subdirectories recursively:**
```bash
python pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents -r
```

**Verbose output to see progress:**
```bash
python pdf_abstract_extractor_basic.py /path/to/pdfs -v
```

### Advanced Usage

**Export as JSON:**
```bash
python pdf_abstract_extractor_advanced.py /path/to/pdfs -o abstracts.json --format json
```

**Export as CSV (great for Excel):**
```bash
python pdf_abstract_extractor_advanced.py /path/to/pdfs -o abstracts.csv --format csv
```

**Only include high-confidence extractions:**
```bash
python pdf_abstract_extractor_advanced.py /path/to/pdfs --min-confidence 0.7 -v
```

**Full example with all options:**
```bash
python pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers \
  --output research_abstracts.json \
  --format json \
  --recursive \
  --verbose \
  --min-confidence 0.6
```

## Command-Line Options

### Common Options (Both Versions)

| Option | Short | Description |
|--------|-------|-------------|
| `input_directory` | (required) | Path to folder containing PDFs |
| `--output` | `-o` | Output file path (default: `pdf_abstracts.txt`) |
| `--recursive` | `-r` | Search subdirectories |
| `--verbose` | `-v` | Show detailed progress |

### Advanced Version Only

| Option | Description |
|--------|-------------|
| `--format {txt,json,csv}` | Output format (default: txt) |
| `--min-confidence 0.0-1.0` | Minimum confidence threshold |

## Output Formats

### Text Format (`.txt`)

```
================================================================================
FILE: paper1.pdf
PATH: /full/path/to/paper1.pdf
EXTRACTED: 2025-11-13 10:30:45
PAGE: 1
STATUS: Success
METHOD: keyword
CONFIDENCE: 0.87
================================================================================

This paper presents a novel approach to machine learning...

================================================================================
```

### JSON Format (`.json`)

```json
{
  "metadata": {
    "generation_date": "2025-11-13T10:30:45",
    "total_files": 50,
    "successful_extractions": 45,
    "success_rate": 90.0
  },
  "abstracts": [
    {
      "filename": "paper1.pdf",
      "filepath": "/path/to/paper1.pdf",
      "page_number": 1,
      "abstract": "This paper presents...",
      "extraction_method": "keyword",
      "confidence": 0.87,
      "file_size_mb": 1.2
    }
  ]
}
```

### CSV Format (`.csv`)

Perfect for importing into Excel or Google Sheets:

| filename | filepath | page_number | abstract | confidence |
|----------|----------|-------------|----------|------------|
| paper1.pdf | /path/... | 1 | This paper... | 0.87 |

## Extraction Methods (Advanced Version)

The advanced version uses multiple strategies:

1. **Keyword-based**: Searches for "Abstract" section headers
2. **Position-based**: Analyzes first page layout
3. **Font-based**: Detects sections by font size changes
4. **Metadata-based**: Checks PDF metadata fields

Each method has a confidence score (0.0 to 1.0) indicating reliability.

## Tips for Best Results

### 1. Organize Your PDFs First
```bash
# Good structure
/mnt/c/Users/YourName/Research/
  ├── MachineLearning/
  ├── NeuralNetworks/
  └── ComputerVision/
```

### 2. Test on a Small Sample First
```bash
# Test with non-recursive search first
python pdf_abstract_extractor_basic.py /path/to/pdfs -v

# Then use recursive if needed
python pdf_abstract_extractor_basic.py /path/to/pdfs -r -v
```

### 3. Check Failed Extractions
The tool logs which files failed. Common reasons:
- Scanned PDFs (image-based, not text)
- Password-protected PDFs
- Non-standard formatting
- No abstract section

### 4. Use JSON for Programmatic Access
```python
import json

with open('abstracts.json') as f:
    data = json.load(f)

for abstract in data['abstracts']:
    if abstract['confidence'] > 0.8:
        print(f"{abstract['filename']}: {abstract['abstract'][:100]}...")
```

### 5. Use CSV for Spreadsheet Analysis
Open the CSV in Excel to:
- Sort by confidence
- Filter by filename
- Search abstracts
- Add your own notes/tags

## Troubleshooting

### "Module not found" Error
```bash
# Install dependencies
pip install pdfplumber PyMuPDF
```

### Permission Denied on Windows Paths
```bash
# Make sure path is correct
ls /mnt/c/Users/YourName/Documents/Papers

# Check if you can read the files
ls -la /mnt/c/Users/YourName/Documents/Papers/*.pdf
```

### Low Success Rate
Try the advanced version:
```bash
python pdf_abstract_extractor_advanced.py /path/to/pdfs -v
```

### Very Large Directories
Process in batches:
```bash
# Process one subdirectory at a time
python pdf_abstract_extractor_basic.py /path/to/pdfs/subfolder1 -o batch1.txt
python pdf_abstract_extractor_basic.py /path/to/pdfs/subfolder2 -o batch2.txt
```

## Example Workflow

### Complete organization workflow:

```bash
# 1. Navigate to the pdf_tools directory
cd /path/to/chalktalk/pdf_tools

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test on a small folder
python pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/TestPapers -v

# 4. Process your full library
python pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/YourName/Documents/Research \
  --output research_catalog.json \
  --format json \
  --recursive \
  --verbose \
  --min-confidence 0.6

# 5. Also create a text version for easy reading
python pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/YourName/Documents/Research \
  --output research_catalog.txt \
  --format txt \
  --recursive

# 6. Create a CSV for Excel
python pdf_abstract_extractor_advanced.py \
  /mnt/c/Users/YourName/Documents/Research \
  --output research_catalog.csv \
  --format csv \
  --recursive
```

Now you have:
- `research_catalog.json` - For programmatic access
- `research_catalog.txt` - For reading
- `research_catalog.csv` - For Excel analysis

## Performance

**Typical performance on average hardware:**
- Basic version: ~15-20 PDFs per minute
- Advanced version: ~10-15 PDFs per minute
- 100 PDFs: ~5-10 minutes
- 1000 PDFs: ~1-2 hours

**Factors affecting speed:**
- PDF file size
- PDF complexity (scanned vs text)
- Number of pages
- Disk speed (SSD vs HDD)

## Files in This Package

```
pdf_tools/
├── DPR_PDF_Abstract_Extractor.md    # Design proposal and requirements
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
├── pdf_abstract_extractor_basic.py  # Simple version
└── pdf_abstract_extractor_advanced.py  # Full-featured version
```

## Support and Customization

### Need OCR Support?
For scanned PDFs, you can add OCR capabilities. See the commented-out dependencies in `requirements.txt`.

### Want Different Output?
Both scripts are well-commented and easy to modify. Key functions:
- `_find_abstract_in_text()` - Modify extraction patterns
- `_clean_abstract()` - Adjust text cleaning
- `_export_*()` - Change output format

### Adding New Extraction Strategies
In the advanced version, add your own strategy:
```python
def _extract_by_custom_method(self, pdf_path: Path):
    # Your custom logic here
    pass

# Add to strategies list in extract_abstract()
```

## License

This tool is provided as-is for organizing your personal PDF collection.

## Feedback

Found a bug or have a suggestion? The scripts are designed to be modified for your specific needs.

---

**Quick Reference Card:**

```bash
# Simplest usage
python pdf_abstract_extractor_basic.py /path/to/pdfs

# Best accuracy
python pdf_abstract_extractor_advanced.py /path/to/pdfs -r -v

# Export to Excel
python pdf_abstract_extractor_advanced.py /path/to/pdfs -o results.csv --format csv -r

# High confidence only
python pdf_abstract_extractor_advanced.py /path/to/pdfs --min-confidence 0.7 -v
```

Happy organizing!
