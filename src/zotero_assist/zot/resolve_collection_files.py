from pathlib import Path
from typing import Dict, List

ZOTERO_STORAGE_TEMPLATE = "Zotero/storage/{item_hash}"


class MissingPDFError(RuntimeError):
    ...


def resolve_collection_files(collection: Dict) -> Dict:
    return {collection_name: _resolve_collection_node(collection) for collection_name, collection in collection.items()}


def _resolve_collection_node(collection: Dict) -> Dict:
    if 'items' in collection:
        collection['items'] = _resolve_items(collection['items'])
    if 'collections' in collection:
        collection['collections'] = resolve_collection_files(collection['collections'])
    return collection


def _resolve_items(items: List) -> List:
    return [Path.home() / ZOTERO_STORAGE_TEMPLATE.format(item_hash=i) / _get_first_pdf(i) for i in items]


def _get_first_pdf(item_hash: str) -> Path:
    item_dir = Path.home() / ZOTERO_STORAGE_TEMPLATE.format(item_hash=item_hash)
    try:
        return next(item_dir.glob("*.pdf"))
    except StopIteration:
        raise MissingPDFError(f"No PDF found in the item folder for item hash {item_hash}.")
