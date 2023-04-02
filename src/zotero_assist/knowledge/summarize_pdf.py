from pathlib import Path

from zotero_assist.constants import get_llaman_index_info_for_pdf
from zotero_assist.knowledge.query_index_for_summary import query_index_for_summary
from zotero_assist.knowledge.retrieve_llama_index_for_pdf import retrieve_llama_index_for_pdf

PROMPT = "tl;dr but highlight key concepts."


def summarize_pdf(pdf_file: Path) -> str:
    index = retrieve_llama_index_for_pdf(pdf_file)
    response = query_index_for_summary(index, PROMPT)
    (get_llaman_index_info_for_pdf(pdf_file)[0] / "summary.txt").write_text(response)
    return response
