from sqlalchemy import (
    Column, String, Integer, Text, Date, DECIMAL, TIMESTAMP,
    Index, ForeignKey, func, ARRAY
)
from sqlalchemy.orm import relationship
from .base import Base

class District(Base):
    __tablename__ = 'districts'
    __table_args__ = {'schema': 'tba'}

    key = Column(String, primary_key=True, comment="Format: yyyy + district abbreviation")
    abbreviation = Column(Text, nullable=False)
    display_name = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    events = relationship("Event", back_populates="district")

    def __repr__(self):
        return f"<District {self.key}: {self.display_name}>"


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'schema': 'tba'}

    # Primary key and basic info
    key = Column(String, primary_key=True, comment="TBA event key with format yyyy[EVENT_CODE]")
    name = Column(Text, nullable=False)
    event_code = Column(Text, nullable=False)
    event_type = Column(Integer, nullable=False)
    event_type_string = Column(Text, nullable=False)

    # District and parent relationships
    district_key = Column(String, ForeignKey('tba.districts.key'))
    parent_event_key = Column(String, ForeignKey('tba.events.key'))

    # Location information
    city = Column(Text)
    state_prov = Column(Text)
    country = Column(Text)
    address = Column(Text)
    postal_code = Column(Text)
    gmaps_place_id = Column(Text)
    gmaps_url = Column(Text)
    lat = Column(DECIMAL(10, 8))
    lng = Column(DECIMAL(11, 8))
    location_name = Column(Text)
    timezone = Column(Text)

    # Date and scheduling
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    week = Column(Integer, comment="Week relative to first official season event, zero-indexed")

    # Event details
    short_name = Column(Text)
    website = Column(Text)
    first_event_id = Column(Text)
    first_event_code = Column(Text)
    division_keys = Column(ARRAY(Text), default=[], comment="Array of division event keys for championship events")
    playoff_type = Column(Integer, comment="Playoff format type")
    playoff_type_string = Column(Text)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    district = relationship("District", back_populates="events")
    parent_event = relationship("Event", remote_side=[key], backref="divisions")
    webcasts = relationship("EventWebcast", back_populates="event", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="event", cascade="all, delete-orphan")
    rankings = relationship("Ranking", back_populates="event", cascade="all, delete-orphan")
    alliances = relationship("Alliance", back_populates="event", cascade="all, delete-orphan")
    ranking_extra_stats_info = relationship("RankingExtraStatsInfo", back_populates="event", cascade="all, delete-orphan")
    ranking_sort_order_info = relationship("RankingSortOrderInfo", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event {self.key}: {self.name}>"


class EventWebcast(Base):
    __tablename__ = 'event_webcasts'
    __table_args__ = {'schema': 'tba'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)
    type = Column(Text, nullable=False, comment="Webcast provider: youtube, twitch, ustream, iframe, etc.")
    channel = Column(Text, nullable=False)
    date = Column(Date)
    file = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="webcasts")

    def __repr__(self):
        return f"<EventWebcast {self.event_key} on {self.type}>"


# Create indexes
Index('idx_districts_year', District.year)
Index('idx_districts_abbreviation', District.abbreviation)

Index('idx_events_year', Event.year)
Index('idx_events_event_type', Event.event_type)
Index('idx_events_week', Event.week)
Index('idx_events_country_state', Event.country, Event.state_prov)
Index('idx_events_start_date', Event.start_date)
Index('idx_events_district_key', Event.district_key)
Index('idx_events_parent_event_key', Event.parent_event_key)
Index('idx_events_division_keys', Event.division_keys, postgresql_using='gin')

Index('idx_event_webcasts_event_key', EventWebcast.event_key)
Index('idx_event_webcasts_type', EventWebcast.type)
