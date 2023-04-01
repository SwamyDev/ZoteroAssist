from pathlib import Path

from zotero_assist.constants import get_llaman_index_dir_for_pdf
from zotero_assist.knowledge.retrieve_llama_index_for_pdf import retrieve_llama_index_for_pdf

PROMPT = "List the core concepts of this paper using bullet-points, and then explain them in detail."


def summarize_pdf(pdf_file: Path) -> str:
    index = retrieve_llama_index_for_pdf(pdf_file)
    response = index.query(PROMPT, mode="summarize").response
    (get_llaman_index_dir_for_pdf(pdf_file) / "summary.txt").write_text(response)
    return response
