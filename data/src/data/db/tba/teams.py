from sqlalchemy import Column, String, Integer, Text, DECIMAL, TIMESTAMP, Index, func
from sqlalchemy.orm import relationship
from .base import Base

class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'schema': 'tba'}

    # Primary key
    key = Column(String, primary_key=True, comment="TBA team key with format frcXXXX")

    # Team information
    team_number = Column(Integer, nullable=False, unique=True, comment="Official team number issued by FIRST")
    nickname = Column(Text, comment="Team nickname provided by FIRST")
    name = Column(Text, comment="Official long name registered with FIRST")
    school_name = Column(Text, comment="Name of team school or affiliated group")

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

    # Additional information
    website = Column(Text)
    rookie_year = Column(Integer, comment="First year the team officially competed")
    motto = Column(Text)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships (will be populated when other models reference this)
    rankings = relationship("Ranking", back_populates="team", cascade="all, delete-orphan")
    match_alliance_teams = relationship("MatchAllianceTeam", back_populates="team")
    alliance_picks = relationship("AlliancePick", back_populates="team")
    alliance_declines = relationship("AllianceDecline", back_populates="team")

    def __repr__(self):
        return f"<Team {self.key}: {self.nickname}>"


# Create indexes
Index('idx_teams_team_number', Team.team_number)
Index('idx_teams_country_state', Team.country, Team.state_prov)
Index('idx_teams_rookie_year', Team.rookie_year)
Index('idx_teams_city', Team.city)
