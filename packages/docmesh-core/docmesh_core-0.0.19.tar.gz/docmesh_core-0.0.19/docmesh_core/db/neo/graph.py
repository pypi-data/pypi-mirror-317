from neomodel import db
from neomodel.integration.pandas import to_dataframe


@db.transaction
def list_cite_graph(entity_name: str, n: int | None = None) -> tuple[list[dict], list[dict]]:
    # fetch all read papers
    if n is None:
        query = r"""
            MATCH (e:Entity) -[:read]-> (p:Paper)
            WHERE e.name = $entity_name
            RETURN elementId(p) AS id, p.title AS title
        """
        nodes = to_dataframe(
            db.cypher_query(
                query,
                params={"entity_name": entity_name},
            )
        )
    else:
        query = r"""
            MATCH (e:Entity) -[:read]-> (p:Paper)
            WHERE e.name = $entity_name
            RETURN elementId(p) AS id,
                   p.title AS title,
                   p.reference_count AS reference_count,
                   p.citation_count AS citation_count,
                   p.pdf AS pdf
            LIMIT $n
        """
        nodes = to_dataframe(
            db.cypher_query(
                query,
                params={"entity_name": entity_name, "n": n},
            )
        )

    # fetch all citations
    query = r"""
        MATCH (e0:Entity) -[:read] -> (p0:Paper) -[c:cite]-> (p1:Paper) <-[:read]- (e1:Entity)
        WHERE e0.name = $entity_name
        AND e1.name = $entity_name
        RETURN elementId(c) AS id, elementId(startNode(c)) AS source, elementId(endNode(c)) AS target
    """
    edges = to_dataframe(
        db.cypher_query(
            query,
            params={"entity_name": entity_name},
        )
    )

    # filter all edges that are not in the nodes
    edges = edges[edges["source"].isin(nodes["id"]) & edges["target"].isin(nodes["id"])]

    # convert to dict
    nodes = nodes.to_dict(orient="records")
    edges = edges.to_dict(orient="records")

    return nodes, edges
