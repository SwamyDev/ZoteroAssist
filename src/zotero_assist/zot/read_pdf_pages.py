from pathlib import Path
from typing import List

from PyPDF2 import PdfReader


def read_pdf_pages(pdf: Path) -> List[str]:
    with open(pdf, "rb") as f:
        pdf_reader = PdfReader(f)
        pages = []
        for page in pdf_reader.pages:
            pages.append(page.extract_text())
        return pages
