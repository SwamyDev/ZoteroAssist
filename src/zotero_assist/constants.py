from pathlib import Path

ZOTERO_DB_FILE = Path.home() / "Zotero/zotero.sqlite"
LLAMA_INDICES_ROOT = Path.home() / ".zotero-assist/llama_indices/"


def get_llaman_index_dir_for_pdf(pdf_file):
    index_dir = LLAMA_INDICES_ROOT / pdf_file.stem
    index_dir.mkdir(parents=True, exist_ok=True)
    return index_dir
