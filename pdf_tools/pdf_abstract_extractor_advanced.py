#!/usr/bin/env python3
"""
PDF Abstract Extractor - Advanced Version
Multi-strategy extraction with better accuracy and JSON/CSV export options.

Usage:
    python pdf_abstract_extractor_advanced.py <input_directory> [options]

Example:
    python pdf_abstract_extractor_advanced.py /mnt/c/Users/YourName/Documents/Papers -o abstracts.json --format json -r
"""

import os
import sys
import argparse
import re
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import pdfplumber
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    print("Please run: pip install pdfplumber PyMuPDF")
    sys.exit(1)


class ExtractionMethod(Enum):
    """Methods used for extracting abstracts."""
    KEYWORD_BASED = "keyword"
    POSITION_BASED = "position"
    FONT_BASED = "font"
    METADATA_BASED = "metadata"
    FALLBACK = "fallback"


@dataclass
class AbstractEntry:
    """Data structure for an extracted abstract."""
    filename: str
    filepath: str
    page_number: Optional[int]
    abstract: str
    extraction_method: str
    confidence: float
    extraction_date: str
    file_size_mb: float
    status: str


class AdvancedPDFAbstractExtractor:
    """Advanced PDF abstract extractor with multiple strategies."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.abstracts: List[AbstractEntry] = []
        self.failed_files: List[str] = []

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

        pdf_files = list(set(pdf_files))
        self.log(f"Found {len(pdf_files)} PDF files")
        return sorted(pdf_files)

    def extract_abstract(self, pdf_path: Path) -> Optional[Tuple[str, int, ExtractionMethod, float]]:
        """
        Extract abstract using multiple strategies.
        Returns: (abstract_text, page_number, method, confidence) or None
        """
        strategies = [
            self._extract_by_keyword,
            self._extract_by_position,
            self._extract_by_font_analysis,
            self._extract_by_metadata,
        ]

        for strategy in strategies:
            try:
                result = strategy(pdf_path)
                if result:
                    return result
            except Exception as e:
                self.log(f"Strategy {strategy.__name__} failed for {pdf_path.name}: {e}", "DEBUG")
                continue

        return None

    def _extract_by_keyword(self, pdf_path: Path) -> Optional[Tuple[str, int, ExtractionMethod, float]]:
        """Extract abstract using keyword-based pattern matching."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                max_pages = min(3, len(pdf.pages))

                for page_num in range(max_pages):
                    page = pdf.pages[page_num]
                    text = page.extract_text()

                    if not text:
                        continue

                    # Enhanced patterns with better matching
                    patterns = [
                        # Academic paper format
                        r'(?i)abstract\s*[:\-—]?\s*(.*?)(?=\n\s*(?:introduction|keywords?|key\s+words?|1\s*\.|I\s*\.|background|\d+\s+introduction))',

                        # All caps format
                        r'ABSTRACT\s*[:\-—]?\s*(.*?)(?=\n\s*(?:INTRODUCTION|KEYWORDS?|KEY\s+WORDS?|1\s*\.|I\s*\.|BACKGROUND))',

                        # With section numbering
                        r'(?i)(?:0\.?\s*)?abstract\s*[:\-—]?\s*(.*?)(?=\n\s*(?:1\.?\s*introduction|keywords?))',

                        # Simple pattern with numbered sections
                        r'(?i)abstract\s*[:\-—]?\s*((?:.*\n?){1,50}?)(?=\n\s*(?:\d+\s*\.|keywords?|introduction))',
                    ]

                    for pattern in patterns:
                        match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
                        if match:
                            abstract = self._clean_abstract(match.group(1))
                            if len(abstract) > 50 and len(abstract) < 5000:
                                confidence = self._calculate_confidence(abstract, "keyword")
                                return (abstract, page_num + 1, ExtractionMethod.KEYWORD_BASED, confidence)

            return None

        except Exception as e:
            self.log(f"Keyword extraction failed: {e}", "DEBUG")
            return None

    def _extract_by_position(self, pdf_path: Path) -> Optional[Tuple[str, int, ExtractionMethod, float]]:
        """Extract abstract based on position (typically top of first page after title)."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) == 0:
                    return None

                page = pdf.pages[0]
                text = page.extract_text()

                if not text:
                    return None

                # Split into paragraphs
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

                # Look for abstract-like paragraph in first few paragraphs
                for idx, para in enumerate(paragraphs[:5]):
                    # Skip very short paragraphs (likely title/authors)
                    if len(para) < 100:
                        continue

                    # Check if it contains typical abstract characteristics
                    if self._is_likely_abstract(para):
                        abstract = self._clean_abstract(para)
                        confidence = self._calculate_confidence(abstract, "position")
                        return (abstract, 1, ExtractionMethod.POSITION_BASED, confidence * 0.8)  # Lower confidence

            return None

        except Exception as e:
            self.log(f"Position-based extraction failed: {e}", "DEBUG")
            return None

    def _extract_by_font_analysis(self, pdf_path: Path) -> Optional[Tuple[str, int, ExtractionMethod, float]]:
        """Extract abstract by analyzing font sizes to find section headers."""
        try:
            doc = fitz.open(pdf_path)

            for page_num in range(min(3, len(doc))):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]

                abstract_found = False
                abstract_text = []
                current_font_size = None

                for block in blocks:
                    if "lines" not in block:
                        continue

                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            font_size = span["size"]

                            # Look for "Abstract" header
                            if re.search(r'\babstract\b', text, re.IGNORECASE):
                                abstract_found = True
                                current_font_size = font_size
                                continue

                            # If we found abstract header, collect text until font size changes significantly
                            if abstract_found:
                                # Stop if we hit a new section header (larger font)
                                if font_size > current_font_size * 1.1:
                                    break

                                abstract_text.append(text)

                                # Stop if we have enough text
                                if len(' '.join(abstract_text)) > 2000:
                                    break

                        if abstract_found and len(abstract_text) > 10:
                            break

                if abstract_text:
                    abstract = self._clean_abstract(' '.join(abstract_text))
                    if len(abstract) > 50:
                        confidence = self._calculate_confidence(abstract, "font")
                        doc.close()
                        return (abstract, page_num + 1, ExtractionMethod.FONT_BASED, confidence)

            doc.close()
            return None

        except Exception as e:
            self.log(f"Font-based extraction failed: {e}", "DEBUG")
            return None

    def _extract_by_metadata(self, pdf_path: Path) -> Optional[Tuple[str, int, ExtractionMethod, float]]:
        """Extract abstract from PDF metadata or bookmarks."""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata

            # Some PDFs include abstract in metadata
            if metadata and 'subject' in metadata and metadata['subject']:
                subject = metadata['subject'].strip()
                if len(subject) > 50:
                    confidence = self._calculate_confidence(subject, "metadata")
                    doc.close()
                    return (subject, 1, ExtractionMethod.METADATA_BASED, confidence * 0.7)

            doc.close()
            return None

        except Exception as e:
            self.log(f"Metadata extraction failed: {e}", "DEBUG")
            return None

    def _is_likely_abstract(self, text: str) -> bool:
        """Heuristic to determine if text is likely an abstract."""
        # Check for common abstract characteristics
        indicators = [
            len(text) > 100 and len(text) < 3000,  # Reasonable length
            text.count('.') > 2,  # Multiple sentences
            not text.startswith('©'),  # Not copyright notice
            not re.search(r'^\d+$', text),  # Not just numbers
            not re.search(r'^[A-Z\s,]+$', text),  # Not all caps (likely title/authors)
        ]

        return sum(indicators) >= 4

    def _calculate_confidence(self, text: str, method: str) -> float:
        """Calculate confidence score for extracted abstract."""
        score = 0.5  # Base score

        # Length check
        if 150 < len(text) < 2000:
            score += 0.2
        elif 100 < len(text) < 3000:
            score += 0.1

        # Sentence structure
        sentences = text.count('.')
        if 3 <= sentences <= 15:
            score += 0.15

        # Contains common academic words
        academic_words = ['study', 'research', 'paper', 'present', 'propose', 'method', 'result', 'conclude']
        if any(word in text.lower() for word in academic_words):
            score += 0.1

        # Method-specific adjustments
        if method == "keyword":
            score += 0.05
        elif method == "metadata":
            score -= 0.1

        return min(1.0, score)

    def _clean_abstract(self, text: str) -> str:
        """Clean and format extracted abstract text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove common artifacts
        text = re.sub(r'^\s*[:\-—]\s*', '', text)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

        # Remove hyphenation at line breaks
        text = re.sub(r'-\s+', '', text)

        return text.strip()

    def process_directory(self, directory: str, output_file: str, output_format: str = 'txt',
                          recursive: bool = False, min_confidence: float = 0.0):
        """Process all PDFs in directory and export results."""
        self.log(f"Starting processing of directory: {directory}")
        self.log(f"Output file: {output_file}")
        self.log(f"Format: {output_format}")

        pdf_files = self.find_pdf_files(directory, recursive)

        if not pdf_files:
            print("No PDF files found in the specified directory.")
            return

        # Process each PDF
        for idx, pdf_path in enumerate(pdf_files, 1):
            self.log(f"Processing [{idx}/{len(pdf_files)}]: {pdf_path.name}")

            try:
                file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
                result = self.extract_abstract(pdf_path)

                if result and result[3] >= min_confidence:
                    abstract, page_num, method, confidence = result
                    entry = AbstractEntry(
                        filename=pdf_path.name,
                        filepath=str(pdf_path.absolute()),
                        page_number=page_num,
                        abstract=abstract,
                        extraction_method=method.value,
                        confidence=confidence,
                        extraction_date=datetime.now().isoformat(),
                        file_size_mb=round(file_size_mb, 2),
                        status="Success"
                    )
                    self.abstracts.append(entry)
                else:
                    entry = AbstractEntry(
                        filename=pdf_path.name,
                        filepath=str(pdf_path.absolute()),
                        page_number=None,
                        abstract="[No abstract could be extracted]",
                        extraction_method="none",
                        confidence=0.0,
                        extraction_date=datetime.now().isoformat(),
                        file_size_mb=round(file_size_mb, 2),
                        status="Failed"
                    )
                    self.abstracts.append(entry)
                    self.failed_files.append(str(pdf_path))

            except Exception as e:
                self.log(f"Error processing {pdf_path.name}: {e}", "ERROR")
                self.failed_files.append(str(pdf_path))

        # Export results
        if output_format == 'txt':
            self._export_text(output_file)
        elif output_format == 'json':
            self._export_json(output_file)
        elif output_format == 'csv':
            self._export_csv(output_file)

        self._print_summary(len(pdf_files))

    def _export_text(self, output_file: str):
        """Export results as formatted text file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PDF ABSTRACT CATALOG (Advanced Extraction)\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Entries: {len(self.abstracts)}\n")
            f.write("=" * 80 + "\n\n")

            for entry in self.abstracts:
                f.write("=" * 80 + "\n")
                f.write(f"FILE: {entry.filename}\n")
                f.write(f"PATH: {entry.filepath}\n")
                f.write(f"PAGE: {entry.page_number if entry.page_number else 'N/A'}\n")
                f.write(f"STATUS: {entry.status}\n")
                f.write(f"METHOD: {entry.extraction_method}\n")
                f.write(f"CONFIDENCE: {entry.confidence:.2f}\n")
                f.write(f"SIZE: {entry.file_size_mb} MB\n")
                f.write(f"EXTRACTED: {entry.extraction_date}\n")
                f.write("=" * 80 + "\n\n")
                f.write(entry.abstract + "\n\n\n")

            # Summary
            successful = sum(1 for e in self.abstracts if e.status == "Success")
            f.write("=" * 80 + "\n")
            f.write("EXTRACTION SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total Files: {len(self.abstracts)}\n")
            f.write(f"Successful: {successful}\n")
            f.write(f"Failed: {len(self.abstracts) - successful}\n")
            f.write(f"Success Rate: {(successful/len(self.abstracts)*100):.1f}%\n")

    def _export_json(self, output_file: str):
        """Export results as JSON file."""
        successful = sum(1 for e in self.abstracts if e.status == "Success")

        data = {
            "metadata": {
                "generation_date": datetime.now().isoformat(),
                "total_files": len(self.abstracts),
                "successful_extractions": successful,
                "failed_extractions": len(self.abstracts) - successful,
                "success_rate": round(successful / len(self.abstracts) * 100, 2) if self.abstracts else 0
            },
            "abstracts": [asdict(entry) for entry in self.abstracts]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _export_csv(self, output_file: str):
        """Export results as CSV file."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if not self.abstracts:
                return

            fieldnames = list(asdict(self.abstracts[0]).keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.abstracts:
                writer.writerow(asdict(entry))

    def _print_summary(self, total_files: int):
        """Print extraction summary to console."""
        successful = sum(1 for e in self.abstracts if e.status == "Success")

        print("\n" + "=" * 80)
        print("EXTRACTION COMPLETE")
        print("=" * 80)
        print(f"Total Files Processed: {total_files}")
        print(f"Successful Extractions: {successful}")
        print(f"Failed Extractions: {total_files - successful}")
        if total_files > 0:
            print(f"Success Rate: {(successful/total_files*100):.1f}%")

        if successful > 0:
            avg_confidence = sum(e.confidence for e in self.abstracts if e.status == "Success") / successful
            print(f"Average Confidence: {avg_confidence:.2f}")

            # Method breakdown
            methods = {}
            for entry in self.abstracts:
                if entry.status == "Success":
                    methods[entry.extraction_method] = methods.get(entry.extraction_method, 0) + 1

            print("\nExtraction Methods Used:")
            for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True):
                print(f"  {method}: {count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced PDF Abstract Extractor with multiple extraction strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with text output
  python pdf_abstract_extractor_advanced.py /path/to/pdfs

  # JSON output with recursive search
  python pdf_abstract_extractor_advanced.py /mnt/c/Users/Name/Papers -o abstracts.json --format json -r

  # CSV output with confidence filter
  python pdf_abstract_extractor_advanced.py . -o results.csv --format csv --min-confidence 0.7 -v
        """
    )

    parser.add_argument('input_directory', help='Directory containing PDF files')
    parser.add_argument('-o', '--output', default='pdf_abstracts.txt', help='Output file path')
    parser.add_argument('--format', choices=['txt', 'json', 'csv'], default='txt',
                        help='Output format (default: txt)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Search subdirectories')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--min-confidence', type=float, default=0.0,
                        help='Minimum confidence threshold (0.0-1.0, default: 0.0)')

    args = parser.parse_args()

    extractor = AdvancedPDFAbstractExtractor(verbose=args.verbose)

    try:
        extractor.process_directory(
            directory=args.input_directory,
            output_file=args.output,
            output_format=args.format,
            recursive=args.recursive,
            min_confidence=args.min_confidence
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        import traceback
        if args.verbose:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
