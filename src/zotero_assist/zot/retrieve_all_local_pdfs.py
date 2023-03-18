from pathlib import Path


def retrieve_all_local_pdfs():
    zot_storage = Path.home() / "Zotero/storage"
    return [pdf for pdf in zot_storage.glob("**/*.pdf")]

