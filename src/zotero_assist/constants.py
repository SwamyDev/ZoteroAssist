import streamlit as st

from pathlib import Path

from llama_index import GPTVectorStoreIndex, GPTTreeIndex

ZOTERO_DB_FILE = Path.home() / "Zotero/zotero.sqlite"
LLAMA_INDICES_ROOT = Path.home() / ".zotero-assist/llama_indices/"
INDEX_TYPE_TO_CLS = {
    'vector': GPTVectorStoreIndex,
    'tree': GPTTreeIndex,
}


def get_llaman_index_info_for_pdf(pdf_file):
    index_type = st.session_state.index_type
    index_model = st.session_state.index_model
    index_cls = INDEX_TYPE_TO_CLS[index_type]

    index_dir = LLAMA_INDICES_ROOT / pdf_file.stem / index_type / index_model
    index_dir.mkdir(parents=True, exist_ok=True)
    return index_dir, index_cls
