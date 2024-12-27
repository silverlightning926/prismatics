from typing import Optional
from pydantic import BaseModel


class Team(BaseModel):
    key: str
    number: int
    nickname: str
    name: str
    city: Optional[str]
    state_prov: Optional[str]
    country: Optional[str]
    website: Optional[str]
    rookie_year: Optional[int]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            key=data["key"],
            number=data["team_number"],
            nickname=data["nickname"],
            name=data["name"],
            city=data.get("city"),
            state_prov=data.get("state_prov"),
            country=data.get("country"),
            lat=data.get("lat"),
            lng=data.get("lng"),
            location_name=data.get("location_name"),
            website=data.get("website"),
            rookie_year=data.get("rookie_year"),
        )
