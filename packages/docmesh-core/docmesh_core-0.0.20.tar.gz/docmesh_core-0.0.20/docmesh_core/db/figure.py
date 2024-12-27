from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """base class"""

    ...


class Figure(Base):
    __tablename__ = "figure"

    id = Column(Integer, primary_key=True)
    paper_id = Column(String(64), unique=True)
    figures = Column(JSON)


def _create_table(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def add_figures(engine: Engine, paper_id: str, figures: list[str]) -> None:
    _create_table(engine=engine)
    with Session(engine) as session:
        session.add(Figure(paper_id=paper_id, figures=figures))
        session.commit()


def get_figures(engine: Engine, paper_id: str) -> list[str] | None:
    with Session(engine) as session:
        figures = session.query(Figure).filter(Figure.paper_id == paper_id).first()

    return figures.figures if figures else None
