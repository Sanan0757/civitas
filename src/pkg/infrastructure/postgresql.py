from typing import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, uri: str):
        self._engine = create_engine(uri)
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=False)

    def get_session(self) -> Generator[Session, Any, None]:
        """
        Returns a generator that yields a SQLAlchemy session. This session should be used for all database interactions within the current request context.
        """
        with self._session_maker() as session:
            yield session
