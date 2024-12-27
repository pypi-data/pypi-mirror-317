from neomodel import db

from docmesh_core.db.neo.base import Venue
from docmesh_core.db.neo.collection import get_collection


class VenueNotFound(Exception):
    def __init__(self, venue_name: str, *args):
        message = f"Cannot find venue {venue_name}."
        super().__init__(message, *args)


def get_venue(venue_name: str) -> Venue:
    if (venue := Venue.nodes.get_or_none(name=venue_name)) is None:
        raise VenueNotFound(venue_name)

    return venue


@db.transaction
def add_venue(venue_name: str) -> Venue:
    venue: Venue = Venue.create_or_update({"name": venue_name})[0]
    return venue


@db.transaction
def add_collection_to_venue(collection_name: str, venue_name: str) -> None:
    collection = get_collection(collection_name)
    venue = get_venue(venue_name)

    if not venue.collections.is_connected(collection):
        venue.collections.connect(collection)
