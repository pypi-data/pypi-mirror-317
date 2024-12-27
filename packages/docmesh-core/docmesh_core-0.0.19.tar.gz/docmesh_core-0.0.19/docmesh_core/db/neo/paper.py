from typing import Optional
from pandas.core.frame import DataFrame

from neomodel import db
from neomodel.integration.pandas import to_dataframe

from docmesh_core.db.neo.base import Paper
from docmesh_core.utils.semantic_scholar import get_paper_details, get_references


class PaperNotFound(Exception):
    def __init__(self, paper: str, *args):
        message = f"Cannot find paper {paper}."
        super().__init__(message, *args)


class PDFNotFound(Exception):
    def __init__(self, paper: str, *args):
        message = f"Cannot find pdf of paper {paper}."
        super().__init__(message, *args)


def get_paper(paper: str) -> Paper:
    paper_by_id = Paper.nodes.get_or_none(paper_id=paper)
    paper_by_title = Paper.nodes.get_or_none(title=paper)

    if paper_by_id is None and paper_by_title is None:
        raise PaperNotFound(paper)

    return paper_by_id if paper_by_title is None else paper_by_title


def _get_papers_helper(paper: str) -> Optional[Paper]:
    try:
        paper = get_paper(paper)
    except PaperNotFound:
        paper = None

    return paper


def get_papers(papers: list[str]) -> list[Optional[Paper]]:
    papers = [_get_papers_helper(paper) for paper in papers]
    return papers


@db.transaction
def _add_paper_references(paper: DataFrame, references: Optional[DataFrame] = None) -> Paper:
    paper: Paper = Paper.create_or_update(*paper.to_dict(orient="records"))[0]

    if references is not None:
        references: list[Paper] = Paper.create_or_update(*references.to_dict(orient="records"))

        for reference in references:
            if not paper.references.is_connected(reference):
                paper.references.connect(reference)

    return paper


def add_paper(paper_id: str) -> Paper:
    paper = get_paper_details([paper_id])

    references_ids = get_references(paper_id)
    if len(references_ids) == 0:
        references = None
    else:
        references = get_paper_details(references_ids)

    paper = _add_paper_references(paper, references)
    return paper


@db.transaction
def update_papers(papers: DataFrame) -> list[Paper]:
    papers = Paper.create_or_update(*papers.to_dict(orient="records"))
    return papers


@db.transaction
def list_unembedded_papers(n: int) -> DataFrame:
    query = r"""
        MATCH (p:Paper)
        WHERE p.embedding_te3l IS NULL
        RETURN p.paper_id AS paper_id, p.title AS title, p.abstract AS abstract, p.summary AS summary
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"n": n},
        ),
    )

    return df
