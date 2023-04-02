import base64
import time
from typing import Dict

import streamlit as st
from pathlib import Path

from PyPDF2 import PdfReader
from llama_index import GPTTreeIndex

from zotero_assist.constants import get_llaman_index_dir_for_pdf
from zotero_assist.knowledge.summarize_pdf import summarize_pdf


class Content:
    def __init__(self, session):
        self.session = session

    def show_summary(self) -> None:
        pdf_file = self.session['selected_pdf']
        index_dir = get_llaman_index_dir_for_pdf(pdf_file)
        summary_file = index_dir / "summary.txt"
        if summary_file.exists():
            st.markdown(summary_file.read_text())
        else:
            with st.spinner("Summarizing..."):
                summary = summarize_pdf(pdf_file)
            st.markdown(summary)

    def show_pdf(self) -> None:
        if 'query' in self.session:
            query = self.session['query']
            pdf_file = self.session['selected_pdf']
            pdf_pages = PdfReader(pdf_file).pages
            st.subheader("Summary of query source:")
            st.write(query['source'])
            st.subheader("Queried PDF page:")
            st.write(pdf_pages[query['page_idx']].extract_text())
