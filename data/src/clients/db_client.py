from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass, field
import os

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
