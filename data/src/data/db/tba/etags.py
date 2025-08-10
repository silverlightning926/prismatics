from sqlalchemy import Column, String, TIMESTAMP, func
from .base import Base

class ETag(Base):
    __tablename__ = 'etags'
    __table_args__ = {'schema': 'tba'}

    endpoint = Column(String, primary_key=True)
    etag = Column(String, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
