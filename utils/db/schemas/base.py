from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData


Base = declarative_base()

MetaBase = declarative_base(metadata=MetaData())