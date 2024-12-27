import uuid

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """base class"""

    ...


class Poster(Base):
    __tablename__ = "poster"

    id = Column(Integer, primary_key=True)
    poster_id = Column(String(32), unique=True)
    paper_id = Column(String(64))
    entity_name = Column(String(64))
    pdf = Column(Text)
    title = Column(Text)
    authors = Column(Text)
    background = Column(Text)
    method = Column(Text)
    experiment = Column(Text)
    result = Column(Text)
    conclusion = Column(Text)


def _create_table(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def add_poster(
    engine: Engine,
    paper_id: str,
    entity_name: str,
    pdf: str,
    title: str,
    authors: str,
    background: str,
    method: str,
    experiment: str,
    result: str,
    conclusion: str,
) -> str:
    _create_table(engine=engine)

    poster_id = uuid.uuid4().hex
    with Session(engine) as session:
        session.add(
            Poster(
                poster_id=poster_id,
                paper_id=paper_id,
                entity_name=entity_name,
                pdf=pdf,
                title=title,
                authors=authors,
                background=background,
                method=method,
                experiment=experiment,
                result=result,
                conclusion=conclusion,
            )
        )
        session.commit()

    return poster_id


def get_poster(engine: Engine, poster_id: str) -> dict | None:

    with Session(engine) as session:
        poster = session.query(Poster).filter(Poster.poster_id == poster_id).first()

    data = (
        {
            "paper_id": poster.paper_id,
            "entity_name": poster.entity_name,
            "pdf": poster.pdf,
            "title": poster.title,
            "authors": poster.authors,
            "background": poster.background,
            "method": poster.method,
            "experiment": poster.experiment,
            "result": poster.result,
            "conclusion": poster.conclusion,
        }
        if poster
        else None
    )

    return data
