import json

from sqlalchemy import select, asc, Column, Integer, Text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """base class"""

    ...


class Message(Base):
    __tablename__ = "message_store"

    id = Column(Integer, primary_key=True)
    entity_name = Column(Text)
    session_id = Column(Text)
    message = Column(Text)


def _create_table(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def format_message(message: str) -> dict[str, str]:
    message = json.loads(message)
    # format into openai api format
    # {"role": "xxx", "content": "xxx"}
    formatted_message = {"role": message["type"], "content": message["data"]["content"]}
    return formatted_message


def get_messages(engine: Engine, entity_name: str, session_id: str) -> list[dict[str, str]]:
    with Session(engine) as session:
        stmt = (
            select(Message)
            .where(
                Message.entity_name == entity_name,
                Message.session_id == session_id,
            )
            .order_by(asc(Message.id))
        )
        messages = session.scalars(stmt)

        if messages is not None:
            messages = [format_message(message.message) for message in messages]

        return messages
