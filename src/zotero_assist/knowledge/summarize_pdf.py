from pathlib import Path

from zotero_assist.constants import get_llama_index_info_for_pdf
from zotero_assist.knowledge.query_index_for_summary import query_index_for_summary
from zotero_assist.knowledge.retrieve_llama_index_for_pdf import retrieve_llama_index_for_pdf

PROMPT = "Give a detailed summary of the text and the most important concepts."


def summarize_pdf(pdf_file: Path) -> str:
    index = retrieve_llama_index_for_pdf(pdf_file)
    response = query_index_for_summary(index, PROMPT)
    (get_llama_index_info_for_pdf(pdf_file)[0] / "summary.txt").write_text(response)
    return response
