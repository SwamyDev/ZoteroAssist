import pytest
import sqlite3

from zotero_assist.zot.fetch_collection import fetch_collection


@pytest.fixture
def zotero_db_conn(tmp_path):
    db_path = tmp_path / 'test_db.sqlite'
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def sample_collections():
    return [
        (1, 'Collection 1', None),
        (2, 'Collection 2', None),
        (3, 'Subcollection 1 of Collection 1', 1),
        (4, 'Subcollection 2 of Collection 1', 1),
    ]


@pytest.fixture
def sample_items():
    return [
        (1, 'abc'),
        (2, 'def'),
        (3, 'ghi'),
    ]


@pytest.fixture
def sample_collection_items():
    return [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 3),
    ]


@pytest.fixture(autouse=True)
def zotero_db(zotero_db_conn, sample_collections, sample_items, sample_collection_items):
    cursor = zotero_db_conn.cursor()
    create_zotero_tables(cursor)
    add_to_zotero_db(cursor, sample_collections, sample_items, sample_collection_items)
    zotero_db_conn.commit()


def create_zotero_tables(cursor):
    cursor.execute('''CREATE TABLE collections
                 (id INTEGER PRIMARY KEY, name TEXT, parentCollectionID INTEGER)''')
    cursor.execute('''CREATE TABLE items
                 (id INTEGER PRIMARY KEY, key TEXT)''')
    cursor.execute('''CREATE TABLE collectionItems
                 (collectionID INTEGER, itemID INTEGER, FOREIGN KEY(collectionID) REFERENCES collections(id), FOREIGN KEY(itemID) REFERENCES items(id))''')


def add_to_zotero_db(cursor, zotero_collections, zotero_items, collection_items):
    cursor.executemany("INSERT INTO collections VALUES (?, ?, ?)", zotero_collections)
    cursor.executemany("INSERT INTO items VALUES (?, ?)", zotero_items)
    cursor.executemany("INSERT INTO collectionItems VALUES (?, ?)", collection_items)


def test_get_collection_item_keys(zotero_db_conn):
    result = fetch_collection(zotero_db_conn)
    assert result == {
        'Collection 1': {
            'collections': {
                'Subcollection 1 of Collection 1': {'items': ['ghi']},
                'Subcollection 2 of Collection 1': {'items': ['ghi']},
            },
            'items': ['abc']
        },
        'Collection 2': {
            'items': ['def']
        }
    }
