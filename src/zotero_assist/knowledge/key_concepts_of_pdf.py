from pathlib import Path

from zotero_assist.constants import get_llaman_index_info_for_pdf
from zotero_assist.knowledge.query_index_for_summary import query_index_for_summary
from zotero_assist.knowledge.retrieve_llama_index_for_pdf import retrieve_llama_index_for_pdf

PROMPT = "List key concepts using markdown bullet-points. Limit yourself to a maximum of 3 items."


def key_concepts_of_pdf(pdf_file: Path) -> str:
    index = retrieve_llama_index_for_pdf(pdf_file)
    response = query_index_for_summary(index, PROMPT)
    (get_llaman_index_info_for_pdf(pdf_file)[0] / "key-concepts.txt").write_text(response)
    return response
