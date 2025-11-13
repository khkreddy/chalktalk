#!/usr/bin/env python3
"""
PDF Abstract Extractor - Basic Version
Extracts abstract sections from PDF files and compiles them into a single text file.

Usage:
    python pdf_abstract_extractor_basic.py <input_directory> [options]

Example:
    python pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers -o abstracts.txt -r
"""

import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed.")
    print("Please run: pip install pdfplumber")
    sys.exit(1)


class PDFAbstractExtractor:
    """Extract abstracts from PDF files."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.processed_files = []
        self.failed_files = []
        self.successful_extractions = 0

    def log(self, message, level="INFO"):
        """Print log message if verbose mode is enabled."""
        if self.verbose or level == "ERROR":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")

    def find_pdf_files(self, directory: str, recursive: bool = False) -> List[Path]:
        """Find all PDF files in the specified directory."""
        directory_path = Path(directory)

        if not directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory}")

        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        if recursive:
            pdf_files = list(directory_path.rglob("*.pdf")) + list(directory_path.rglob("*.PDF"))
        else:
            pdf_files = list(directory_path.glob("*.pdf")) + list(directory_path.glob("*.PDF"))

        # Remove duplicates
        pdf_files = list(set(pdf_files))

        self.log(f"Found {len(pdf_files)} PDF files")
        return sorted(pdf_files)

    def extract_abstract(self, pdf_path: Path) -> Optional[Tuple[str, int]]:
        """
        Extract abstract from a PDF file.
        Returns: (abstract_text, page_number) or None if not found
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Check first 3 pages (most abstracts are on first page)
                max_pages = min(3, len(pdf.pages))

                for page_num in range(max_pages):
                    page = pdf.pages[page_num]
                    text = page.extract_text()

                    if not text:
                        continue

                    # Try to find abstract section
                    abstract = self._find_abstract_in_text(text)
                    if abstract:
                        return (abstract, page_num + 1)

                return None

        except Exception as e:
            self.log(f"Error processing {pdf_path.name}: {str(e)}", "ERROR")
            return None

    def _find_abstract_in_text(self, text: str) -> Optional[str]:
        """
        Find and extract abstract from text using pattern matching.
        """
        # Common patterns for abstract sections
        patterns = [
            # Pattern 1: "Abstract" followed by text until next section
            r'(?i)abstract\s*[:\-]?\s*(.*?)(?=\n\s*(?:introduction|keywords|1\.|I\.|background|key words|\d+\s+introduction))',

            # Pattern 2: "ABSTRACT" in all caps
            r'ABSTRACT\s*[:\-]?\s*(.*?)(?=\n\s*(?:INTRODUCTION|KEYWORDS|1\.|I\.|BACKGROUND|KEY WORDS|\d+\s+INTRODUCTION))',

            # Pattern 3: Abstract section with potential line breaks
            r'(?i)abstract\s*[:\-]?\s*((?:.*\n){1,30}?)(?=\n\s*(?:introduction|keywords|1\.|I\.|background))',

            # Pattern 4: Simple abstract to first numbered section
            r'(?i)abstract\s*[:\-]?\s*(.*?)(?=\n\s*\d+\.)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
            if match:
                abstract = match.group(1).strip()
                # Clean up the abstract
                abstract = self._clean_abstract(abstract)
                # Only return if we have substantial text (at least 50 characters)
                if len(abstract) > 50:
                    return abstract

        return None

    def _clean_abstract(self, text: str) -> str:
        """Clean and format extracted abstract text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove common artifacts
        text = re.sub(r'^\s*[:\-]\s*', '', text)

        # Remove page numbers and headers/footers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

        return text.strip()

    def process_directory(self, directory: str, output_file: str, recursive: bool = False):
        """Process all PDFs in directory and write abstracts to output file."""
        self.log(f"Starting processing of directory: {directory}")
        self.log(f"Output file: {output_file}")
        self.log(f"Recursive: {recursive}")

        # Find all PDF files
        pdf_files = self.find_pdf_files(directory, recursive)

        if not pdf_files:
            print("No PDF files found in the specified directory.")
            return

        # Open output file
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # Write header
            out_f.write("=" * 80 + "\n")
            out_f.write("PDF ABSTRACT CATALOG\n")
            out_f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out_f.write(f"Source Directory: {directory}\n")
            out_f.write(f"Total PDF Files: {len(pdf_files)}\n")
            out_f.write("=" * 80 + "\n\n")

            # Process each PDF
            for idx, pdf_path in enumerate(pdf_files, 1):
                self.log(f"Processing [{idx}/{len(pdf_files)}]: {pdf_path.name}")

                result = self.extract_abstract(pdf_path)

                # Write entry
                out_f.write("=" * 80 + "\n")
                out_f.write(f"FILE: {pdf_path.name}\n")
                out_f.write(f"PATH: {pdf_path.absolute()}\n")
                out_f.write(f"EXTRACTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                if result:
                    abstract, page_num = result
                    out_f.write(f"PAGE: {page_num}\n")
                    out_f.write(f"STATUS: Success\n")
                    out_f.write("=" * 80 + "\n\n")
                    out_f.write(abstract + "\n\n")
                    self.successful_extractions += 1
                    self.processed_files.append(str(pdf_path))
                else:
                    out_f.write(f"PAGE: N/A\n")
                    out_f.write(f"STATUS: Failed - No abstract found or extraction error\n")
                    out_f.write("=" * 80 + "\n\n")
                    out_f.write("[No abstract could be extracted from this file]\n\n")
                    self.failed_files.append(str(pdf_path))

                out_f.write("\n")

            # Write summary
            out_f.write("=" * 80 + "\n")
            out_f.write("EXTRACTION SUMMARY\n")
            out_f.write("=" * 80 + "\n")
            out_f.write(f"Total Files Processed: {len(pdf_files)}\n")
            out_f.write(f"Successful Extractions: {self.successful_extractions}\n")
            out_f.write(f"Failed Extractions: {len(self.failed_files)}\n")
            out_f.write(f"Success Rate: {(self.successful_extractions/len(pdf_files)*100):.1f}%\n")

            if self.failed_files:
                out_f.write("\nFailed Files:\n")
                for failed_file in self.failed_files:
                    out_f.write(f"  - {failed_file}\n")

        # Print summary to console
        print("\n" + "=" * 80)
        print("EXTRACTION COMPLETE")
        print("=" * 80)
        print(f"Total Files Processed: {len(pdf_files)}")
        print(f"Successful Extractions: {self.successful_extractions}")
        print(f"Failed Extractions: {len(self.failed_files)}")
        print(f"Success Rate: {(self.successful_extractions/len(pdf_files)*100):.1f}%")
        print(f"\nOutput saved to: {output_file}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract abstracts from PDF files and compile them into a text file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from current directory
  python pdf_abstract_extractor_basic.py .

  # Extract from Windows path (WSL)
  python pdf_abstract_extractor_basic.py /mnt/c/Users/YourName/Documents/Papers

  # Recursive search with custom output
  python pdf_abstract_extractor_basic.py /path/to/pdfs -o my_abstracts.txt -r -v
        """
    )

    parser.add_argument(
        'input_directory',
        help='Directory containing PDF files (e.g., /mnt/c/Users/YourName/Documents/Papers)'
    )

    parser.add_argument(
        '-o', '--output',
        default='pdf_abstracts.txt',
        help='Output file path (default: pdf_abstracts.txt)'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Search subdirectories recursively'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Create extractor
    extractor = PDFAbstractExtractor(verbose=args.verbose)

    try:
        # Process directory
        extractor.process_directory(
            directory=args.input_directory,
            output_file=args.output,
            recursive=args.recursive
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Partial results may be in output file.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
