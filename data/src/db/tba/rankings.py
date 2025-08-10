from sqlalchemy import (
    Column, String, Integer, TIMESTAMP, DECIMAL, ARRAY,
    Index, ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from .base import Base

class Ranking(Base):
    __tablename__ = 'rankings'
    __table_args__ = (
        UniqueConstraint('event_key', 'team_key'),
        UniqueConstraint('event_key', 'rank'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)
    team_key = Column(String, ForeignKey('tba.teams.key'), nullable=False)

    # Ranking details
    rank = Column(Integer, nullable=False, comment="Team rank at the event (1 = first place)")
    matches_played = Column(Integer, nullable=False)
    qual_average = Column(Integer, comment="Average match score during qualifications (year-specific)")

    # Win/Loss record
    wins = Column(Integer, nullable=False, default=0)
    losses = Column(Integer, nullable=False, default=0)
    ties = Column(Integer, nullable=False, default=0)
    dq = Column(Integer, nullable=False, default=0, comment="Number of times team was disqualified")

    # Additional statistics
    extra_stats = Column(ARRAY(DECIMAL), default=[], comment="Array of additional TBA-calculated statistics")
    sort_orders = Column(ARRAY(DECIMAL), default=[], comment="Array of year-specific ranking criteria values")

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="rankings")
    team = relationship("Team", back_populates="rankings")

    def __repr__(self):
        return f"<Ranking {self.team_key} rank {self.rank} at {self.event_key}>"


class RankingExtraStatsInfo(Base):
    __tablename__ = 'ranking_extra_stats_info'
    __table_args__ = (
        UniqueConstraint('event_key', 'array_position'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    precision_digits = Column(Integer, default=0, comment="Number of decimal places for this statistic")
    array_position = Column(Integer, nullable=False, comment="Index position in the extra_stats array")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="ranking_extra_stats_info")

    def __repr__(self):
        return f"<RankingExtraStatsInfo {self.name} at position {self.array_position}>"


class RankingSortOrderInfo(Base):
    __tablename__ = 'ranking_sort_order_info'
    __table_args__ = (
        UniqueConstraint('event_key', 'array_position'),
        {'schema': 'tba'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_key = Column(String, ForeignKey('tba.events.key', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    precision_digits = Column(Integer, default=0, comment="Number of decimal places for this statistic")
    array_position = Column(Integer, nullable=False, comment="Index position in the sort_orders array")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    event = relationship("Event", back_populates="ranking_sort_order_info")

    def __repr__(self):
        return f"<RankingSortOrderInfo {self.name} at position {self.array_position}>"


# Create indexes
Index('idx_rankings_event_key', Ranking.event_key)
Index('idx_rankings_team_key', Ranking.team_key)
Index('idx_rankings_rank', Ranking.rank)
Index('idx_rankings_wins_losses', Ranking.wins, Ranking.losses)
Index('idx_rankings_matches_played', Ranking.matches_played)

Index('idx_ranking_extra_stats_info_event_key', RankingExtraStatsInfo.event_key)
Index('idx_ranking_sort_order_info_event_key', RankingSortOrderInfo.event_key)
