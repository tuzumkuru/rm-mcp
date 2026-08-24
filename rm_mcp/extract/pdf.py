"""PDF text extraction."""

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def extract_pdf_pages(pdf_path: Path) -> List[str]:
    """
    Extract text from a PDF, one entry per page.

    The list is aligned with the document's real page numbers: entry 0 is
    page 1, and pages with no text layer are present as empty strings rather
    than skipped, so "page 12" here is page 12 in the PDF.

    Returns an empty list if the file cannot be read.
    """
    try:
        import fitz  # PyMuPDF

        with fitz.open(pdf_path) as doc:
            return [page.get_text().strip() for page in doc]
    except ImportError:
        return []
    except Exception:
        logger.warning("Failed to extract text from %s", pdf_path, exc_info=True)
        return []


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a PDF file as one string with page markers.

    Returns the full text content of the PDF.
    """
    pages = extract_pdf_pages(pdf_path)
    parts = [f"--- Page {n} ---\n{text}" for n, text in enumerate(pages, 1) if text]
    return "\n\n".join(parts)
