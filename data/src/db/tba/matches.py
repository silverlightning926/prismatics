from sqlalchemy import (
    Column, String, Integer, Text, Boolean, BIGINT, TIMESTAMP,
    Index, ForeignKey, CheckConstraint, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Match(Base):
    __tablename__ = 'matches'
    __table_args__ = (
        CheckConstraint("comp_level IN ('qm', 'ef', 'qf', 'sf', 'f')", name='chk_comp_level'),
        CheckConstraint("winning_alliance IN ('red', 'blue', '')", name='chk_winning_alliance'),
        {'schema': 'tba'}
    )

    # Primary key and identifiers
    key = Column(String, primary_key=True, comment="TBA match key with format yyyy[EVENT_CODE]_[COMP_LEVEL]m[MATCH_NUMBER]")
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)

    # Match details
    comp_level = Column(Text, nullable=False, comment="Competition level: qm=Qualifications, ef=Elimination Finals, qf=Quarterfinals, sf=Semifinals, f=Finals")
    set_number = Column(Integer, nullable=False)
    match_number = Column(Integer, nullable=False)

    # Timestamps (UNIX timestamps)
    time_scheduled = Column(BIGINT, comment="UNIX timestamp")
    actual_time = Column(BIGINT, comment="UNIX timestamp")
    predicted_time = Column(BIGINT, comment="UNIX timestamp")
    post_result_time = Column(BIGINT, comment="UNIX timestamp")

    # Results
    winning_alliance = Column(Text, default='', comment="red, blue, or empty string")
    score_breakdown = Column(JSONB, comment="Year-specific detailed scoring information stored as JSON")

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="matches")
    alliances = relationship("MatchAlliance", back_populates="match", cascade="all, delete-orphan")
    videos = relationship("MatchVideo", back_populates="match", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Match {self.key}>"


class MatchAlliance(Base):
    __tablename__ = 'match_alliances'
    __table_args__ = (
        UniqueConstraint('match_key', 'alliance_color'),
        CheckConstraint("alliance_color IN ('red', 'blue')", name='chk_alliance_color'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_key = Column(String, ForeignKey('tba.matches.key', ondelete='CASCADE'), nullable=False)
    alliance_color = Column(Text, nullable=False, comment="red or blue")
    score = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    match = relationship("Match", back_populates="alliances")
    teams = relationship("MatchAllianceTeam", back_populates="alliance", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MatchAlliance {self.match_key} {self.alliance_color}>"


class MatchAllianceTeam(Base):
    __tablename__ = 'match_alliance_teams'
    __table_args__ = (
        CheckConstraint("position IN (1, 2, 3)", name='chk_position'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_alliance_id = Column(Integer, ForeignKey('tba.match_alliances.id', ondelete='CASCADE'), nullable=False)
    team_key = Column(String, ForeignKey('tba.teams.key'), nullable=False)
    is_surrogate = Column(Boolean, default=False, comment="Whether this team is playing as a surrogate")
    is_dq = Column(Boolean, default=False, comment="Whether this team was disqualified")
    position = Column(Integer, comment="Robot position (1, 2, or 3) within the alliance")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    alliance = relationship("MatchAlliance", back_populates="teams")
    team = relationship("Team", back_populates="match_alliance_teams")

    def __repr__(self):
        return f"<MatchAllianceTeam {self.team_key} in alliance {self.match_alliance_id}>"


class MatchVideo(Base):
    __tablename__ = 'match_videos'
    __table_args__ = {'schema': 'tba'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_key = Column(String, ForeignKey('tba.matches.key', ondelete='CASCADE'), nullable=False)
    type = Column(Text, nullable=False, comment="youtube, tba, etc.")
    video_key = Column(Text, nullable=False, comment="Video identifier")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    match = relationship("Match", back_populates="videos")

    def __repr__(self):
        return f"<MatchVideo {self.type}:{self.video_key} for {self.match_key}>"


# Create indexes
Index('idx_matches_event_key', Match.event_key)
Index('idx_matches_comp_level', Match.comp_level)
Index('idx_matches_match_number', Match.match_number)
Index('idx_matches_time_scheduled', Match.time_scheduled)
Index('idx_matches_winning_alliance', Match.winning_alliance)

Index('idx_match_alliances_match_key', MatchAlliance.match_key)
Index('idx_match_alliances_alliance_color', MatchAlliance.alliance_color)

Index('idx_match_alliance_teams_match_alliance_id', MatchAllianceTeam.match_alliance_id)
Index('idx_match_alliance_teams_team_key', MatchAllianceTeam.team_key)
Index('idx_match_alliance_teams_is_surrogate', MatchAllianceTeam.is_surrogate)
Index('idx_match_alliance_teams_is_dq', MatchAllianceTeam.is_dq)

Index('idx_match_videos_match_key', MatchVideo.match_key)
Index('idx_match_videos_type', MatchVideo.type)
