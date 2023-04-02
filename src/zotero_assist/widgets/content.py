import streamlit as st
from PyPDF2 import PdfReader

from zotero_assist.constants import get_llama_index_info_for_pdf
from zotero_assist.knowledge.key_concepts_of_pdf import key_concepts_of_pdf
from zotero_assist.knowledge.summarize_pdf import summarize_pdf


class Content:
    def __init__(self, session):
        self.session = session

    def show_summary(self) -> None:
        pdf_file = self.session['selected_pdf']
        index_dir = get_llama_index_info_for_pdf(pdf_file)[0]

        key_concepts_file = index_dir / "key-concepts.txt"
        if key_concepts_file.exists():
            st.markdown(key_concepts_file.read_text())
        else:
            with st.spinner("Finding key concepts..."):
                key_concepts = key_concepts_of_pdf(pdf_file)
            st.markdown(key_concepts)

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
