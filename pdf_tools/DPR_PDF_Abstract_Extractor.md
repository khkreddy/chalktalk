# Design Proposal and Requirements (DPR)
## PDF Abstract Extractor Tool

### 1. Project Overview
**Purpose**: Create a Python tool to systematically organize PDF files by extracting abstract sections and cataloging them in a searchable text file.

**Target Environment**: WSL Linux on Windows laptop

### 2. Functional Requirements

#### 2.1 Core Functionality
- **FR-1**: Search a specified directory (and optionally subdirectories) for PDF files
- **FR-2**: Extract text from the "Abstract" section of each PDF file
- **FR-3**: Compile all abstracts into a single text file
- **FR-4**: Tag each abstract entry with:
  - File name
  - Full file path
  - Extraction timestamp
  - Page number where abstract was found (if available)

#### 2.2 User Interface
- **FR-5**: Command-line interface with configurable parameters:
  - Input directory path
  - Output file path
  - Recursive search option
  - Verbose logging option

#### 2.3 Error Handling
- **FR-6**: Handle corrupted or password-protected PDFs gracefully
- **FR-7**: Log files that couldn't be processed
- **FR-8**: Continue processing remaining files if one fails

### 3. Non-Functional Requirements

#### 3.1 Performance
- **NFR-1**: Process at least 10 PDFs per minute on average hardware
- **NFR-2**: Support files up to 100MB in size

#### 3.2 Usability
- **NFR-3**: Clear progress indication during processing
- **NFR-4**: Human-readable output format
- **NFR-5**: Option to output in multiple formats (TXT, JSON, CSV)

#### 3.3 Reliability
- **NFR-6**: Robust error handling to prevent crashes
- **NFR-7**: Verification that output file is successfully written

### 4. Technical Architecture

#### 4.1 Proposed Solutions

##### Solution 1: Basic Extractor (Recommended for Quick Start)
**Dependencies**:
- `PyPDF2` or `pdfplumber` - PDF text extraction
- `pathlib` - Cross-platform path handling
- Standard library modules (os, re, datetime)

**Extraction Strategy**:
- Simple pattern matching for "Abstract" keyword
- Extract text between "Abstract" and next section header
- Works well for academic papers with standard formatting

**Pros**:
- Lightweight, minimal dependencies
- Fast processing
- Easy to understand and modify

**Cons**:
- May miss abstracts with non-standard formatting
- Limited accuracy for complex PDF layouts

##### Solution 2: Advanced Multi-Strategy Extractor (Recommended for Best Results)
**Dependencies**:
- `pdfplumber` - Better text extraction with layout awareness
- `PyMuPDF (fitz)` - Advanced PDF parsing
- `regex` - Enhanced pattern matching
- `nltk` (optional) - Natural language processing for abstract detection

**Extraction Strategy**:
- Multiple detection methods:
  1. Keyword-based: "Abstract", "ABSTRACT", "Summary"
  2. Position-based: Text in specific page regions (first 1-2 pages)
  3. Font-based: Detect section headers by font size/style
  4. Structure-based: Parse PDF metadata and bookmarks
- Fallback mechanism if primary method fails
- Confidence scoring for extracted text

**Pros**:
- Higher accuracy across different PDF formats
- Better handling of complex layouts
- Multiple fallback strategies

**Cons**:
- More dependencies to install
- Slightly slower processing
- More complex code

##### Solution 3: AI-Powered Extractor (Future Enhancement)
**Dependencies**:
- Solutions 1 or 2 as base
- OpenAI API or local LLM for intelligent extraction
- Can identify abstracts even without clear section markers

### 5. Output Format Specification

#### 5.1 Text Output Format
```
================================================================================
FILE: filename.pdf
PATH: /full/path/to/filename.pdf
EXTRACTED: 2025-11-13 10:30:45
PAGE: 1
STATUS: Success
================================================================================

[Abstract text content here...]

================================================================================
```

#### 5.2 JSON Output Format (Optional)
```json
{
  "extraction_date": "2025-11-13T10:30:45",
  "total_files": 50,
  "successful": 45,
  "failed": 5,
  "abstracts": [
    {
      "filename": "paper1.pdf",
      "filepath": "/path/to/paper1.pdf",
      "page_number": 1,
      "abstract": "Text content...",
      "extraction_method": "keyword",
      "confidence": 0.95
    }
  ]
}
```

### 6. Implementation Plan

#### Phase 1: Basic Implementation
1. Implement directory traversal
2. Implement basic abstract extraction
3. Create output file with metadata
4. Add error handling and logging

#### Phase 2: Enhanced Features
1. Implement multiple extraction strategies
2. Add output format options (TXT, JSON, CSV)
3. Improve pattern matching accuracy
4. Add configuration file support

#### Phase 3: Advanced Features
1. Add GUI option (optional)
2. Implement caching to avoid re-processing
3. Add search functionality in generated catalog
4. Generate statistics and summary reports

### 7. Usage Examples

#### Basic Usage:
```bash
python pdf_abstract_extractor.py /path/to/pdfs -o abstracts.txt
```

#### Advanced Usage:
```bash
python pdf_abstract_extractor.py /path/to/pdfs \
  --output abstracts.txt \
  --format json \
  --recursive \
  --verbose \
  --log errors.log
```

### 8. Testing Strategy
- Test with various PDF formats (scanned, text-based, mixed)
- Test with different paper types (academic, technical reports, books)
- Test error conditions (corrupted files, no abstracts, etc.)
- Performance testing with large directories (100+ PDFs)

### 9. Dependencies Installation
```bash
# Basic solution
pip install PyPDF2 pdfplumber

# Advanced solution
pip install pdfplumber PyMuPDF regex

# Optional NLP features
pip install nltk
```

### 10. Future Enhancements
- Web interface for easier use
- Database backend for better searching
- Duplicate detection
- Automatic categorization based on abstract content
- Integration with reference managers (Zotero, Mendeley)
- OCR support for scanned PDFs
- Multi-language support

### 11. Deliverables
1. **DPR Document** (this file)
2. **pdf_abstract_extractor_basic.py** - Simple, reliable solution
3. **pdf_abstract_extractor_advanced.py** - Full-featured solution
4. **requirements.txt** - Python dependencies
5. **README.md** - User guide and examples

### 12. Timeline Estimate
- Basic Solution: 2-3 hours
- Advanced Solution: 4-6 hours
- Testing and Documentation: 1-2 hours

### 13. Success Criteria
- Successfully extract abstracts from at least 80% of standard academic PDFs
- Process 100 PDFs in under 15 minutes
- Generate well-formatted, searchable output file
- Zero crashes during normal operation
- Clear error messages for problematic files
