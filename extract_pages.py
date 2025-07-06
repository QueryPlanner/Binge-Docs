#!/usr/bin/env python3

import sys
import argparse
import fitz  # PyMuPDF

def extract_pages_from_pdf(pdf_path, start_page, end_page=None):
    """Extract text from PDF page range and output to stdout for piping."""
    try:
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        
        if start_page < 1 or start_page > total_pages:
            print(f"Error: Invalid start page {start_page}. PDF has {total_pages} pages.", file=sys.stderr)
            sys.exit(1)
        
        if end_page is None:
            end_page = total_pages
        elif end_page > total_pages:
            end_page = total_pages
        
        print(f"Extracting pages {start_page} to {end_page} from {pdf_path}...", file=sys.stderr)
        
        # Convert to 0-based indexing
        start_page -= 1
        end_page -= 1
        
        extracted_text = []
        for page_num in range(start_page, end_page + 1):
            try:
                page = doc[page_num]
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    extracted_text.append(text)
            except Exception as e:
                print(f"Warning: Error extracting page {page_num + 1}: {str(e)}", file=sys.stderr)
                continue
        
        # Output to stdout for piping
        full_text = '\n'.join(extracted_text)
        print(full_text)
        
        doc.close()
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF pages for piping to kokoro-tts")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("start_page", type=int, help="Page number to start reading from (1-based)")
    parser.add_argument("--end-page", type=int, help="Page number to stop reading at (optional)")
    
    args = parser.parse_args()
    
    extract_pages_from_pdf(args.pdf_path, args.start_page, args.end_page)

if __name__ == "__main__":
    main() 