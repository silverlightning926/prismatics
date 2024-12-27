from pydantic import BaseModel


class Etag(BaseModel):
    etag: str
    endpoint: str
