from pathlib import Path
from unittest.mock import MagicMock

import pytest

from zotero_assist.zot.resolve_collection_files import ZOTERO_STORAGE_TEMPLATE, MissingPDFError, \
    resolve_collection_files


@pytest.fixture(autouse=True)
def mock_path_home(monkeypatch, tmp_path):
    path = tmp_path / "home/testor"
    monkeypatch.setattr('pathlib.Path.home', MagicMock(return_value=path))
    return path


@pytest.fixture(autouse=True)
def create_test_pdfs(mock_path_home):
    for h, name in [("h4sh", "some.pdf"),
                    ("another_hash", "another.pdf"),
                    ("yet_another_hash", "some.pdf"),
                    ("col2h1", "some.pdf"),
                    ("col2h2", "some.pdf")]:
        pdf = mock_path_home / ZOTERO_STORAGE_TEMPLATE.format(item_hash=h) / name
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.touch(exist_ok=True)
    (mock_path_home / ZOTERO_STORAGE_TEMPLATE.format(item_hash='missing_pdf')).mkdir(parents=True, exist_ok=True)


def test_empty_dict_for_empty_input():
    assert resolve_collection_files({}) == {}


def test_single_collection_with_no_items():
    assert resolve_collection_files({'collection 1': {'items': []}}) == {'collection 1': {'items': []}}


def test_single_collection_with_one_item():
    assert resolve_collection_files({'collection 1': {'items': ['h4sh']}}) == {
        'collection 1': {'items': [Path.home() / 'Zotero/storage/h4sh/some.pdf']}}


def test_single_collection_with_multiple_items():
    assert resolve_collection_files({'collection 1': {'items': ['h4sh', 'another_hash']}}) == {
        'collection 1': {'items': [
            Path.home() / 'Zotero/storage/h4sh/some.pdf',
            Path.home() / 'Zotero/storage/another_hash/another.pdf'
        ]}}


def test_single_collection_with_missing_pdf():
    with pytest.raises(MissingPDFError):
        assert resolve_collection_files({'collection': {'items': ['missing_pdf']}})


def test_collections_with_sub_collections_and_items():
    assert resolve_collection_files({
        'collection 1': {
            'items': ['h4sh'],
            'collections': {
                'sub collection of collection 1': {
                    'collections': {
                        'sub-sub collection of collection 1': {
                            'items': ['another_hash']
                        }
                    }
                }
            }
        },
        'collection 2': {
            'items': ['col2h1', 'col2h2']
        }
    }) == {
               'collection 1': {
                   'items': [Path.home() / 'Zotero/storage/h4sh/some.pdf'],
                   'collections': {
                       'sub collection of collection 1': {
                           'collections': {
                               'sub-sub collection of collection 1': {
                                   'items': [Path.home() / 'Zotero/storage/another_hash/another.pdf']
                               }
                           }
                       }
                   }
               },
               'collection 2': {
                   'items': [Path.home() / 'Zotero/storage/col2h1/some.pdf',
                             Path.home() / 'Zotero/storage/col2h2/some.pdf']
               }
           }
