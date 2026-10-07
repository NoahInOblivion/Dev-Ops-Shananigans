from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


def _engine(url: str):
    args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=args)


engine = _engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
