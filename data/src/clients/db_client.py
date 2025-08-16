from dotenv import load_dotenv
load_dotenv()

import os

from dataclasses import dataclass, field
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Optional

@dataclass
class _DBConfig():
    connection_string: str = field(init=False)

    def __post_init__(self):
        env_connection_string = os.getenv("DB_CONNECTION_STRING")

        if not env_connection_string or not env_connection_string.strip():
            raise ValueError("DB Connection String Not Found")

        if not isinstance(env_connection_string, str):
            raise TypeError("DB Connection Must Be A String")

        self.connection_string = env_connection_string

class DBClient:
    def __init__(self):
        self.config = _DBConfig()
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self.config.connection_string,
                poolclass=NullPool,
            )
        return self._engine

    @contextmanager
    def get_connection(self):
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            yield conn
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e
        finally:
            conn.close()

    def set_etag(self, endpoint: str, etag: str) -> None:
       with self.get_connection() as conn:
           conn.execute(
               text("""
                   INSERT INTO etags (endpoint, etag)
                   VALUES (:endpoint, :etag)
                   ON CONFLICT (endpoint)
                   DO UPDATE SET
                       etag = EXCLUDED.etag,
                       created_at = CURRENT_TIMESTAMP
               """),
               {
                   "endpoint": endpoint,
                   "etag": etag
               }
           )

    def get_etag(self, endpoint: str) -> Optional[str]:
        with self.get_connection() as conn:
            result = conn.execute(
                text("SELECT etag FROM etags WHERE endpoint = :endpoint"),
                {"endpoint": endpoint}
            )
            row = result.fetchone()
            return row[0] if row else None
