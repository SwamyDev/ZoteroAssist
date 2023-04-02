from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from PyPDF2 import PdfReader


@dataclass
class PdfPages:
    src: Path
    pages: Sequence[str]


def read_pdf_pages(pdf: Path) -> PdfPages:
    with open(pdf, "rb") as f:
        pdf_reader = PdfReader(f)
        return PdfPages(pdf, [p.extract_text() for p in pdf_reader.pages])
