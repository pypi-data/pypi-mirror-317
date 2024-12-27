from neomodel import db

from docmesh_core.db.neo.base import Collection
from docmesh_core.db.neo.paper import get_paper


class CollectionNotFound(Exception):
    def __init__(self, collection_name: str, *args):
        message = f"Cannot find collection {collection_name}."
        super().__init__(message, *args)


def get_collection(collection_name: str) -> Collection:
    if (collection := Collection.nodes.get_or_none(name=collection_name)) is None:
        raise CollectionNotFound(collection_name)

    return collection


@db.transaction
def add_collection(collection_name: str) -> Collection:
    collection: Collection = Collection.create_or_update({"name": collection_name})[0]
    return collection


@db.transaction
def add_paper_to_collection(paper_id: str, collection_name: str) -> None:
    paper = get_paper(paper_id)
    collection = get_collection(collection_name)

    if not collection.papers.is_connected(paper):
        collection.papers.connect(paper)
