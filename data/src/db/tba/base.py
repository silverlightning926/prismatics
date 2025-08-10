from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema='tba')
Base = declarative_base(metadata=metadata)
