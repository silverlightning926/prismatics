from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pytz


class Division(BaseModel):
    parent_event_key: str
    division_event_key: str


class Webcast(BaseModel):
    event_key: str
    type: str
    channel: str
    date: Optional[str]
    file: Optional[str]

    @classmethod
    def from_dict(
        cls,
        data: dict,
        event_key: str,
        timezone: pytz.timezone,
    ) -> "Webcast":
        return cls(
            event_key=event_key,
            type=data.get("type"),
            channel=data.get("channel"),
            date=(
                datetime.strptime(
                    data.get("date"),
                    "%Y-%m-%d",
                )
                .replace(tzinfo=timezone)
                .isoformat()
                if data.get("date")
                else None
            ),
            file=data.get("file"),
        )


class District(BaseModel):
    key: str
    abbreviation: str
    display_name: str
    year: int

    @classmethod
    def from_dict(cls, data: dict) -> "District":
        return cls(
            key=data.get("key"),
            abbreviation=data.get("abbreviation"),
            display_name=data.get("display_name"),
            year=data.get("year"),
        )


class Event(BaseModel):
    key: str
    name: str
    event_code: str
    event_type: str
    district: Optional[District]
    city: Optional[str]
    state_prov: Optional[str]
    country: Optional[str]
    start_date: str
    end_date: str
    year: int
    short_name: Optional[str]
    week: Optional[int]
    address: Optional[str]
    postal_code: Optional[str]
    gmaps_url: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    location_name: Optional[str]
    website: Optional[str]
    webcasts: list[Webcast]
    division: Optional[Division]
    playoff_type: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            key=data.get("key"),
            name=data.get("name"),
            event_code=data.get("event_code"),
            event_type=data.get("event_type_string"),
            district=(
                District.from_dict(data.get("district"))
                if data.get("district")
                else None
            ),
            city=data.get("city"),
            state_prov=data.get("state_prov"),
            country=data.get("country"),
            start_date=datetime.strptime(
                data.get("start_date"),
                "%Y-%m-%d",
            )
            .replace(tzinfo=pytz.timezone(data.get("timezone")))
            .isoformat(),
            end_date=datetime.strptime(
                data.get("end_date"),
                "%Y-%m-%d",
            )
            .replace(tzinfo=pytz.timezone(data.get("timezone")))
            .isoformat(),
            year=data.get("year"),
            short_name=data.get("short_name"),
            week=data.get("week"),
            address=data.get("address"),
            postal_code=data.get("postal_code"),
            gmaps_url=data.get("gmaps_url"),
            lat=data.get("lat"),
            lng=data.get("lng"),
            location_name=data.get("location_name"),
            website=data.get("website"),
            webcasts=[
                Webcast.from_dict(
                    webcast,
                    event_key=data.get("key"),
                    timezone=pytz.timezone(data.get("timezone")),
                )
                for webcast in data.get("webcasts", [])
            ],
            division=(
                Division(
                    parent_event_key=data.get("parent_event_key"),
                    division_event_key=data.get("key"),
                )
                if data.get("parent_event_key")
                else None
            ),
            playoff_type=data.get("playoff_type_string"),
        )
