import base64
import time

import streamlit as st
from pathlib import Path

from llama_index import GPTTreeIndex

from zotero_assist.constants import get_llaman_index_dir_for_pdf
from zotero_assist.knowledge.summarize_pdf import summarize_pdf


class Content:
    def __init__(self, column):
        self.column = column

    def show_summary(self, pdf_file: Path) -> None:
        index_dir = get_llaman_index_dir_for_pdf(pdf_file)
        summary_file = index_dir / "summary.txt"
        if summary_file.exists():
            self.column.markdown(summary_file.read_text())
        else:
            with self.column:
                with st.spinner("Summarizing..."):
                    summary = summarize_pdf(pdf_file)
            self.column.markdown(summary)

    def show_pdf(self, pdf_file: Path) -> None:
        base64_pdf = base64.b64encode(pdf_file.read_bytes()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="800">'
        self.column.markdown(pdf_display, unsafe_allow_html=True)
