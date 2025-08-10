from sqlalchemy import (
    Column, String, Integer, Text, DECIMAL, TIMESTAMP,
    Index, ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from .base import Base

class Alliance(Base):
    __tablename__ = 'alliances'
    __table_args__ = {'schema': 'tba'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)

    # Alliance details
    name = Column(Text, comment="Alliance name like Alliance 1, Alliance 2, etc.")

    # Status information
    status_level = Column(Text, comment="Current competition level (f=Finals, sf=Semifinals, etc.)")
    status_status = Column(Text, comment="Current status: won, eliminated")
    status_playoff_type = Column(Integer)
    status_double_elim_round = Column(Text, comment="Round in double elimination format")

    # Win/Loss record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    current_level_wins = Column(Integer, default=0)
    current_level_losses = Column(Integer, default=0)
    current_level_ties = Column(Integer, default=0)

    # Performance
    playoff_average = Column(DECIMAL(10, 2))

    # Backup substitutions
    backup_in = Column(String, ForeignKey('tba.teams.key'), comment="Team key that was called in as backup")
    backup_out = Column(String, ForeignKey('tba.teams.key'), comment="Team key that was replaced by backup")

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="alliances")
    picks = relationship("AlliancePick", back_populates="alliance", cascade="all, delete-orphan")
    declines = relationship("AllianceDecline", back_populates="alliance", cascade="all, delete-orphan")
    backup_in_team = relationship("Team", foreign_keys=[backup_in])
    backup_out_team = relationship("Team", foreign_keys=[backup_out])

    def __repr__(self):
        return f"<Alliance {self.name} at {self.event_key}>"


class AlliancePick(Base):
    __tablename__ = 'alliance_picks'
    __table_args__ = (
        UniqueConstraint('alliance_id', 'pick_order'),
        UniqueConstraint('alliance_id', 'team_key'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    alliance_id = Column(Integer, ForeignKey('tba.alliances.id', ondelete='CASCADE'), nullable=False)
    team_key = Column(String, ForeignKey('tba.teams.key'), nullable=False)
    pick_order = Column(Integer, nullable=False, comment="Order picked: 1=captain, 2=first pick, 3=second pick, 4=third pick (backup)")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    alliance = relationship("Alliance", back_populates="picks")
    team = relationship("Team", back_populates="alliance_picks")

    def __repr__(self):
        return f"<AlliancePick {self.team_key} pick #{self.pick_order} for alliance {self.alliance_id}>"


class AllianceDecline(Base):
    __tablename__ = 'alliance_declines'
    __table_args__ = (
        UniqueConstraint('alliance_id', 'team_key'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    alliance_id = Column(Integer, ForeignKey('tba.alliances.id', ondelete='CASCADE'), nullable=False)
    team_key = Column(String, ForeignKey('tba.teams.key'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    alliance = relationship("Alliance", back_populates="declines")
    team = relationship("Team", back_populates="alliance_declines")

    def __repr__(self):
        return f"<AllianceDecline {self.team_key} declined alliance {self.alliance_id}>"

# Create indexes
Index('idx_alliances_event_key', Alliance.event_key)
Index('idx_alliances_status_status', Alliance.status_status)
Index('idx_alliances_status_level', Alliance.status_level)

Index('idx_alliance_picks_alliance_id', AlliancePick.alliance_id)
Index('idx_alliance_picks_team_key', AlliancePick.team_key)
Index('idx_alliance_picks_pick_order', AlliancePick.pick_order)

Index('idx_alliance_declines_alliance_id', AllianceDecline.alliance_id)
Index('idx_alliance_declines_team_key', AllianceDecline.team_key)
