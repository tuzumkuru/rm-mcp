"""EPUB text extraction."""

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def extract_epub_sections(epub_path: Path) -> List[str]:
    """
    Extract text from an EPUB, one entry per content document.

    EPUBs have no fixed pages; the natural unit is the spine's content
    documents (roughly chapters). Empty sections are dropped.

    Returns an empty list if the file cannot be read.
    """
    try:
        from bs4 import BeautifulSoup
        from ebooklib import ITEM_DOCUMENT, epub

        book = epub.read_epub(str(epub_path), options={"ignore_ncx": True})
        sections = []
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                if text:
                    sections.append(text)
        return sections
    except ImportError:
        return []
    except Exception:
        logger.warning("Failed to extract text from %s", epub_path, exc_info=True)
        return []


def extract_text_from_epub(epub_path: Path) -> str:
    """
    Extract text from an EPUB file.

    Returns the full text content of the EPUB.
    """
    return "\n\n".join(extract_epub_sections(epub_path))
