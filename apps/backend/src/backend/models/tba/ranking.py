from pydantic import BaseModel


class Ranking(BaseModel):
    event_key: str
    team_key: str
    rank: int

    @classmethod
    def from_dict(cls, data: dict, event_key: str) -> "Ranking":
        return cls(
            event_key=event_key,
            team_key=data["team_key"],
            rank=data["rank"],
        )
