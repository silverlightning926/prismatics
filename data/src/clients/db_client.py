from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass, field
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.tba import Base

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

        self.engine = create_engine(
            self.config.connection_string,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=False
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def setup_database(self, base=Base, drop_existing=False):
        schemas = {table.schema for table in base.metadata.tables.values() if table.schema}

        with self.engine.connect() as conn:
            for schema in schemas:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            conn.commit()

        if drop_existing:
            base.metadata.drop_all(self.engine)

        base.metadata.create_all(self.engine)
