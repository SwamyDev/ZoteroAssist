from pathlib import Path

from langchain import OpenAI
from llama_index import GPTTreeIndex, LLMPredictor

from zotero_assist.constants import get_llaman_index_dir_for_pdf
from zotero_assist.knowledge.make_embedded_docs_from_pages import make_embedded_docs_from_pages
from zotero_assist.zot.read_pdf_pages import read_pdf_pages

SELECTED_MODEL = "text-ada-001"


def make_index_for_pdf(pdf_file: Path) -> GPTTreeIndex:
    llm_predictor = LLMPredictor(llm=OpenAI(model_name=SELECTED_MODEL))
    paper_pages = read_pdf_pages(pdf_file)
    index = GPTTreeIndex(make_embedded_docs_from_pages(paper_pages), llm_predictor=llm_predictor)
    index.save_to_disk(get_llaman_index_dir_for_pdf(pdf_file) / "index.json")
    return index
