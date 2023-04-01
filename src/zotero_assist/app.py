from pathlib import Path
from typing import Sequence

import streamlit as st
from PyPDF2 import PdfReader

from zotero_assist.result import Result
from zotero_assist.zot.retrieve_all_local_pdfs import retrieve_all_local_pdfs

st.title('Zotero Assist')

ZOTERO_DB_FILE = Path.home() / "Zotero/zotero.sqlite"


@st.cache_data
def get_all_zotero_pdfs() -> Sequence[Path]:
    return retrieve_all_local_pdfs()


@st.cache_data
def get_available_summary_for(pdf_file: Path) -> str:
    return (zotero_info_subject(pdf_file) or
            pdf_first_page_abstract(pdf_file) or
            Result.ok("No summary found.")).unwrap()


def zotero_info_subject(pdf_file: Path) -> Result[str]:
    zt_info_file = pdf_file.parent / ".zotero-ft-info"
    if zt_info_file.exists():
        zt_infos = zt_info_file.read_text().splitlines()
        for line in zt_infos:
            line_split = line.split(':')
            if line_split[0].strip() == 'Subject':
                return Result.ok(line_split[1].strip())
    return Result.error("No Zotero info subject found")


def pdf_first_page_abstract(pdf_file: Path) -> Result[str]:
    first_page_lines = PdfReader(pdf_file).pages[0].extract_text()
    for line in first_page_lines:
        if line.lower().startswith('abstract'):
            return Result.ok(line)
    return Result.error("No abstract found in pdf")


def add_zotero_pdfs(filenames: Sequence[Path]) -> None:
    for file in filenames:
        with st.expander(file.stem):
            st.write(get_available_summary_for(file))


pdf_filenames = get_all_zotero_pdfs()

with st.sidebar:
    add_zotero_pdfs(pdf_filenames[:2])
