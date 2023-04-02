from pathlib import Path

from llama_index import GPTTreeIndex, LLMPredictor

from zotero_assist.constants import get_llama_index_info_for_pdf
from zotero_assist.knowledge.make_embedded_docs_from_pages import make_embedded_docs_from_pages
from zotero_assist.zot.read_pdf_pages import read_pdf_pages

SELECTED_MODEL = "text-ada-001"


def make_index_for_pdf(pdf_file: Path, llm_predictor: LLMPredictor) -> GPTTreeIndex:
    paper_pages = read_pdf_pages(pdf_file)
    index_file, index_cls = get_llama_index_info_for_pdf(pdf_file)
    index = index_cls(make_embedded_docs_from_pages(paper_pages), llm_predictor=llm_predictor)
    index.save_to_disk(index_file / "index.json")
    return index
