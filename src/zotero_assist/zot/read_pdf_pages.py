from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

from PyPDF2 import PdfReader, PageObject


@dataclass
class PdfPages:
    src: Path
    pages: Sequence[PageObject]


def read_pdf_pages(pdf: Path) -> PdfPages:
    with open(pdf, "rb") as f:
        pdf_reader = PdfReader(f)
        return PdfPages(pdf, pdf_reader.pages)
