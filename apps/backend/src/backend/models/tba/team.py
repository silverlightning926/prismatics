from typing import Optional
from pydantic import BaseModel


class Team(BaseModel):
    key: str
    team_number: int
    nickname: str
    name: str
    city: Optional[str]
    state_prov: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    location_name: Optional[str]
    website: Optional[str]
    rookie_year: Optional[int]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            key=data["key"],
            team_number=data["team_number"],
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
