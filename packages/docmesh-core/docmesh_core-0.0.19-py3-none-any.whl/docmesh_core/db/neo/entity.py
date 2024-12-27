from pandas.core.frame import DataFrame

from neomodel import db
from neomodel.integration.pandas import to_dataframe

from docmesh_core.db.neo.base import Entity
from docmesh_core.db.neo.paper import get_paper, Paper
from docmesh_core.db.neo.venue import get_venue, Venue
from docmesh_core.db.neo.utils import nodelist_to_dataframe


class DuplicateEntity(Exception):
    def __init__(self, entity_name: str, *args):
        message = f"Entity {entity_name} already exists, please change the name."
        super().__init__(message, *args)


class EntityNotFound(Exception):
    def __init__(self, entity_name: str, *args):
        message = f"Cannot find entity {entity_name}."
        super().__init__(message, *args)


def get_entity(entity_name: str) -> Entity:
    if (entity := Entity.nodes.get_or_none(name=entity_name)) is None:
        raise EntityNotFound(entity_name)

    return entity


@db.transaction
def add_entity(entity_name: str) -> Entity:
    if Entity.nodes.get_or_none(name=entity_name) is not None:
        raise DuplicateEntity(entity_name)

    entity = Entity(name=entity_name).save()
    return entity


@db.transaction
def follow_entity(follower_name: str, follow_name: str) -> None:
    follower_entity = get_entity(follower_name)
    followed_entity = get_entity(follow_name)

    if not follower_entity.follows.is_connected(followed_entity):
        follower_entity.follows.connect(followed_entity)


@db.transaction
def list_follows(entity_name: str) -> DataFrame:
    entity = get_entity(entity_name)
    follows: list[Entity] = entity.follows.all()
    return nodelist_to_dataframe(follows)


@db.transaction
def list_followers(entity_name: str) -> DataFrame:
    entity = get_entity(entity_name)
    followers: list[Entity] = entity.followers.all()
    return nodelist_to_dataframe(followers)


@db.transaction
def list_popular_entities(n: int) -> DataFrame:
    query = r"""
        MATCH (e:Entity)
        RETURN e.name AS name,
        COUNT {
            (:Entity) -[:follow]-> (e)
        } AS num_followers,
        COUNT {
            (e) -[:read]-> (:Paper)
        } AS num_reads
        ORDER BY num_followers DESC, num_reads DESC
        LIMIT $n
    """
    df = to_dataframe(
        db.cypher_query(
            query=query,
            params={"n": n},
        )
    )

    return df


@db.transaction
def subscribe_venue(entity_name: str, venue_name: str) -> None:
    entity = get_entity(entity_name)
    venue = get_venue(venue_name)

    if not entity.subscriptions.is_connected(venue):
        entity.subscriptions.connect(venue)


@db.transaction
def list_subscriptions(entity_name: str) -> DataFrame:
    entity = get_entity(entity_name)
    subscriptions: list[Venue] = entity.subscriptions.all()
    return nodelist_to_dataframe(subscriptions)


@db.transaction
def is_paper_read(entity_name: str, paper_id: str) -> bool:
    entity = get_entity(entity_name)
    paper = get_paper(paper_id)

    return entity.reads.is_connected(paper)


@db.transaction
def is_paper_in_list(entity_name: str, paper_id: str) -> bool:
    entity = get_entity(entity_name)
    paper = get_paper(paper_id)

    return entity.lists.is_connected(paper)


@db.transaction
def mark_paper_read(entity_name: str, paper_id: str) -> None:
    entity = get_entity(entity_name)
    paper = get_paper(paper_id)

    if entity.lists.is_connected(paper):
        entity.lists.disconnect(paper)

    if not entity.reads.is_connected(paper):
        entity.reads.connect(paper)


@db.transaction
def save_paper_list(entity_name: str, paper_id: str) -> None:
    entity = get_entity(entity_name)
    paper = get_paper(paper_id)

    if not entity.lists.is_connected(paper):
        entity.lists.connect(paper)


@db.transaction
def list_reading_list(entity_name: str) -> DataFrame:
    entity = get_entity(entity_name)
    reading_list: list[Paper] = entity.lists.all()
    return nodelist_to_dataframe(reading_list)


@db.transaction
def list_latest_reading_papers(entity_name: str, n: int) -> DataFrame:
    query = r"""
        MATCH (e:Entity) -[r:read]-> (p:Paper)
        WHERE e.name = $entity_name
        RETURN p.paper_id AS paper_id, p.title AS title
        ORDER BY r.read_time DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name, "n": n},
        )
    )

    return df


@db.transaction
def list_recent_reading_papers(entity_name: str, date_time: str) -> DataFrame:
    query = r"""
        MATCH (e:Entity) -[r:read]-> (p:Paper)
        WHERE e.name = $entity_name
        AND r.read_time > (DATETIME($date_time)).epochSeconds
        RETURN p.paper_id AS paper_id, p.title AS title
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name, "date_time": date_time},
        )
    )

    return df


@db.transaction
def list_entity_info(entity_name: str, num_weeks: int) -> DataFrame:
    query = r"""
        MATCH (e:Entity) -[r:read]-> (p:Paper)
        WHERE e.name = $entity_name
        AND r.read_time > (DATETIME() - DURATION({weeks: $num_weeks})).epochSeconds
        RETURN e.name AS name,
        COUNT {
            (:Entity) -[:follow]-> (e)
        } AS num_followers,
        COUNT {
            (e) -[:follow]-> (:Entity)
        } AS num_follows,
        COUNT(p) AS num_readings,
        COLLECT(p.title) AS papers
    """
    df = to_dataframe(
        db.cypher_query(
            query=query,
            params={"entity_name": entity_name, "num_weeks": num_weeks},
        )
    )

    return df
