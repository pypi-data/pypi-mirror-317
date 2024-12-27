import uuid

from typing import Optional

from datetime import datetime, timedelta
from sqlalchemy import select, Column, Integer, String, DateTime
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """base class"""

    ...


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(64), unique=True)
    access_token = Column(String(32))
    premium_expiration = Column(DateTime)
    last_login = Column(DateTime)


def _create_table(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def add_auth_for_entity(engine: Engine, entity_name: str) -> str:
    _create_table(engine=engine)

    access_token = uuid.uuid4().hex
    premium_expiration = datetime.fromtimestamp(0).strftime("%Y-%m-%d")
    last_login = datetime.fromtimestamp(0).strftime("%Y-%m-%d")
    with Session(engine) as session:
        session.add(
            Auth(
                entity_name=entity_name,
                access_token=access_token,
                premium_expiration=premium_expiration,
                last_login=last_login,
            )
        )
        session.commit()

    return access_token


def get_auth_from_entity(engine: Engine, entity_name: str) -> Optional[str]:
    with Session(engine) as session:
        stmt = select(Auth.access_token).where(Auth.entity_name == entity_name)
        access_token = session.scalar(stmt)

    return access_token


def get_entity_from_auth(engine: Engine, access_token: str) -> tuple[Optional[str], bool]:
    with Session(engine) as session:
        stmt = select(Auth).where(Auth.access_token == access_token)
        auth = session.scalar(stmt)

    if auth is None:
        entity_name, premium = None, False
    else:
        entity_name, premium = auth.entity_name, auth.premium_expiration > datetime.now()

    return entity_name, premium


def refresh_premium(engine: Engine, entity_name: str, days: int) -> datetime:
    with Session(engine) as session:
        stmt = select(Auth).where(Auth.entity_name == entity_name)
        auth = session.scalar(stmt)

        expiration_date = max(auth.premium_expiration, datetime.now()) + timedelta(days=days)
        auth.premium_expiration = expiration_date
        session.commit()

    return expiration_date


def log_last_login(engine: Engine, entity_name: str) -> None:
    with Session(engine) as session:
        stmt = select(Auth).where(Auth.entity_name == entity_name)
        auth = session.scalar(stmt)

        auth.last_login = datetime.now()
        session.commit()
