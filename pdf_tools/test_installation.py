#!/usr/bin/env python3
"""
Test script to verify PDF Abstract Extractor installation
Run this to check if all dependencies are correctly installed
"""

import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("=" * 60)
    print("PDF Abstract Extractor - Installation Test")
    print("=" * 60)
    print()

    errors = []

    # Test basic Python modules
    print("Testing standard library modules...")
    try:
        import os, sys, argparse, re, json, csv
        from pathlib import Path
        from datetime import datetime
        from typing import List, Dict, Tuple, Optional
        from dataclasses import dataclass
        from enum import Enum
        print("✓ Standard library modules: OK")
    except ImportError as e:
        print(f"✗ Standard library error: {e}")
        errors.append("Standard library")

    print()

    # Test pdfplumber
    print("Testing pdfplumber...")
    try:
        import pdfplumber
        print(f"✓ pdfplumber version: {pdfplumber.__version__}")
    except ImportError:
        print("✗ pdfplumber: NOT INSTALLED")
        print("  Install with: pip3 install pdfplumber")
        errors.append("pdfplumber")

    print()

    # Test PyMuPDF
    print("Testing PyMuPDF (fitz)...")
    try:
        import fitz
        print(f"✓ PyMuPDF version: {fitz.__version__}")
    except ImportError:
        print("✗ PyMuPDF: NOT INSTALLED")
        print("  Install with: pip3 install PyMuPDF")
        errors.append("PyMuPDF")

    print()
    print("=" * 60)

    if not errors:
        print("✓ ALL TESTS PASSED!")
        print()
        print("Your installation is complete and ready to use.")
        print()
        print("Next steps:")
        print("1. Place some PDF files in a test directory")
        print("2. Run the basic extractor:")
        print("   python3 pdf_abstract_extractor_basic.py /path/to/pdfs -v")
        print()
        print("3. Or run the advanced extractor:")
        print("   python3 pdf_abstract_extractor_advanced.py /path/to/pdfs -v")
        print()
        return True
    else:
        print(f"✗ {len(errors)} ERROR(S) FOUND")
        print()
        print("Missing modules:", ", ".join(errors))
        print()
        print("To fix, run:")
        print("  pip3 install pdfplumber PyMuPDF")
        print()
        print("Or use the requirements file:")
        print("  pip3 install -r requirements.txt")
        print()
        return False

    print("=" * 60)

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
