from pydantic import BaseModel
from typing import Optional
from json import dumps
from datetime import datetime


class Video(BaseModel):
    match_key: str
    key: str
    type: str

    @classmethod
    def from_dict(cls, match_key: str, data: dict):
        return cls(
            match_key=match_key,
            key=data.get("key"),
            type=data.get("type"),
        )


class AllianceTeam(BaseModel):
    key: str
    team_key: str
    alliance_key: str
    surrogate: bool
    disqualified: bool

    @classmethod
    def from_dict(
        cls,
        team_key: str,
        alliance: str,
        match_key: str,
        surrogate: bool,
        disqualified: bool,
    ):
        return cls(
            key=f"{match_key}_{team_key}",
            team_key=team_key,
            alliance_key=f"{match_key}_{alliance}",
            surrogate=surrogate,
            disqualified=disqualified,
        )


class Alliance(BaseModel):
    key: str
    match_key: str
    color: str
    score: int
    score_breakdown: Optional[dict]
    teams: list[AllianceTeam]

    @classmethod
    def from_dict(
        cls,
        match_key: str,
        color: str,
        alliance_data: dict,
        score_breakdown: Optional[dict],
    ):
        return cls(
            key=f"{match_key}_{color}",
            match_key=match_key,
            color=color,
            score=alliance_data.get("score"),
            score_breakdown=(
                score_breakdown.get(color, None) if score_breakdown else None
            ),
            teams=[
                AllianceTeam.from_dict(
                    team_key,
                    color,
                    match_key,
                    surrogate=team_key in alliance_data.get("surrogate_team_keys", []),
                    disqualified=team_key in alliance_data.get("dq_team_keys", []),
                )
                for team_key in list(
                    set(
                        alliance_data.get("team_keys", [])
                        + alliance_data.get("surrogate_team_keys", [])
                        + alliance_data.get("dq_team_keys", [])
                    )
                )
            ],
        )


class Match(BaseModel):
    key: str
    comp_level: str
    set_number: int
    match_number: int
    winning_alliance: Optional[str]
    event_key: str
    alliances: list[Alliance]
    time: Optional[str]
    actual_time: Optional[str]
    predicted_time: Optional[str]
    post_result_time: Optional[str]
    videos: list[Video]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            key=data.get("key"),
            comp_level=data.get("comp_level"),
            set_number=data.get("set_number"),
            match_number=data.get("match_number"),
            winning_alliance=data.get("winning_alliance"),
            event_key=data.get("event_key"),
            alliances=[
                Alliance.from_dict(
                    data.get("key"),
                    color,
                    alliance_data,
                    data.get("score_breakdown"),
                )
                for color, alliance_data in data.get("alliances").items()
            ],
            time=(
                datetime.fromtimestamp(data.get("time")).isoformat()
                if data.get("time")
                else None
            ),
            actual_time=(
                datetime.fromtimestamp(data.get("actual_time")).isoformat()
                if data.get("actual_time")
                else None
            ),
            predicted_time=(
                datetime.fromtimestamp(data.get("predicted_time")).isoformat()
                if data.get("predicted_time")
                else None
            ),
            post_result_time=(
                datetime.fromtimestamp(data.get("post_result_time")).isoformat()
                if data.get("post_result_time")
                else None
            ),
            videos=[
                Video.from_dict(match_key=data.get("key"), data=video)
                for video in data.get("videos", [])
            ],
        )
