from pydantic import BaseModel


class Etag(BaseModel):
    etag: str
    endpoint: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            etag=data["etag"],
            endpoint=data["endpoint"],
        )
