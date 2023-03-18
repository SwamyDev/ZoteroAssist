from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock

import pytest

ZOTERO_STORAGE_TEMPLATE = "Zotero/storage/{item_hash}"


@pytest.fixture(autouse=True)
def mock_path_home(monkeypatch, tmp_path):
    path = tmp_path / "home/testor"
    monkeypatch.setattr('pathlib.Path.home', MagicMock(return_value=path))
    return path


@pytest.fixture(autouse=True)
def create_test_pdfs(mock_path_home):
    for h, name in [('h4sh', "some.pdf"), ("another_hash", "another.pdf")]:
        pdf = mock_path_home / ZOTERO_STORAGE_TEMPLATE.format(item_hash=h) / name
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.touch(exist_ok=True)


def resolve_collection_files(collection: Dict) -> Dict:
    return {collection_name: {'items': resolve_items(collection['items'])}
            for collection_name, collection in collection.items()}


def resolve_items(items: List) -> List:
    return [Path.home() / ZOTERO_STORAGE_TEMPLATE.format(item_hash=i) / get_first_pdf(i) for i in items]


def get_first_pdf(item_hash: str) -> Path:
    item_dir = Path.home() / ZOTERO_STORAGE_TEMPLATE.format(item_hash=item_hash)
    return next(item_dir.glob("*.pdf"))


def test_empty_dict_for_empty_input():
    assert resolve_collection_files({}) == {}


def test_single_collection_with_no_items():
    assert resolve_collection_files({'collection': {'items': []}}) == {'collection': {'items': []}}


def test_single_collection_with_one_item():
    assert resolve_collection_files({'collection': {'items': ['h4sh']}}) == {
        'collection': {'items': [Path.home() / 'Zotero/storage/h4sh/some.pdf']}}


def test_single_collection_with_multiple_items():
    assert resolve_collection_files({'collection': {'items': ['h4sh', 'another_hash']}}) == {
        'collection': {'items': [
            Path.home() / 'Zotero/storage/h4sh/some.pdf',
            Path.home() / 'Zotero/storage/another_hash/another.pdf'
        ]}}
