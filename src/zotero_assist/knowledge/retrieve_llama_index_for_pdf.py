from pathlib import Path

import streamlit as st
from langchain import OpenAI
from llama_index import LLMPredictor

from zotero_assist.constants import get_llaman_index_info_for_pdf
from zotero_assist.knowledge.make_index_for_pdf import make_index_for_pdf


def retrieve_llama_index_for_pdf(pdf_file: Path):
    predictor = LLMPredictor(llm=OpenAI(model_name=st.session_state.index_model))
    index_dir, index_cls = get_llaman_index_info_for_pdf(pdf_file)
    print(index_cls)
    index_file = index_dir / "index.json"
    if index_file.exists():
        return index_cls.load_from_disk(index_file.as_posix(), llm_predictor=predictor)
    else:
        with st.spinner("generating index..."):
            return make_index_for_pdf(pdf_file, llm_predictor=predictor)
