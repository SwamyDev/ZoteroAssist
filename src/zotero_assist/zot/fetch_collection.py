def fetch_collection(conn):
    collections = {}

    def get_items(collection_id):
        query = "SELECT items.key FROM items JOIN collectionItems ON items.id=collectionItems.itemID WHERE collectionItems.collectionID=?"
        return [row[0] for row in conn.execute(query, (collection_id,))]

    def get_collections(parent_collection_id=None):
        query = "SELECT id, name FROM collections WHERE parentCollectionID=?"
        sub_collections = {}
        for row in conn.execute(query, (parent_collection_id,)):
            sub_collection_id, sub_collection_name = row
            items = get_items(sub_collection_id)
            if items:
                sub_collections[sub_collection_name] = {"items": items}
            sub_collections.update(get_collections(sub_collection_id))
        return sub_collections

    for row in conn.execute("SELECT id, name FROM collections WHERE parentCollectionID IS NULL"):
        collection_id, collection_name = row
        items = get_items(collection_id)
        sub_collections = get_collections(collection_id)
        if sub_collections:
            collections[collection_name] = {"collections": sub_collections, "items": items}
        else:
            collections[collection_name] = {"items": items}

    return collections
