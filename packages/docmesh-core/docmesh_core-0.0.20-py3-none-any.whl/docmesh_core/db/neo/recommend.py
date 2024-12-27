from pandas.core.frame import DataFrame

from neomodel import db
from neomodel.integration.pandas import to_dataframe


@db.transaction
def recommend_similar_papers(entity_name: str, paper_id: str, n: int) -> DataFrame:
    query = r"""
        MATCH (p0:Paper)
        WHERE p0.paper_id = $paper_id
        CALL db.index.vector.queryNodes('vector_embedding_te3l', $n, p0.embedding_te3l)
        YIELD node AS p, score
        WHERE NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf, score
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name, "paper_id": paper_id, "n": n},
        )
    )

    return df


@db.transaction
def recommend_semantic_papers(entity_name: str, semantic_embedding: list[float], n: int) -> DataFrame:
    query = r"""
        CALL db.index.vector.queryNodes('vector_embedding_te3l', $n, $semantic_embedding)
        YIELD node AS p, score
        WHERE NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf, score
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name, "semantic_embedding": semantic_embedding, "n": n},
        )
    )

    return df


@db.transaction
def recommend_follows_papers(entity_name: str, n: int) -> DataFrame:
    query = r"""
        MATCH (e1:Entity) -[:follow]-> (:Entity) -[r:read]-> (p:Paper)
        WHERE e1.name = $entity_name
        AND NOT EXISTS {
            (p) <-[:read]- (e2:Entity)
            WHERE e2.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY r.read_time, p.citation_count DESC
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
def recommend_influential_papers(entity_name: str, date_time: str, n: int) -> DataFrame:
    query = r"""
        MATCH (p:Paper)
        WHERE p.publication_date >= DATETIME($date_time).epochSeconds
        AND NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY p.citation_count DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name, "date_time": date_time, "n": n},
        )
    )

    return df
