from sqlalchemy import Column, String, Integer

from .base import Base
from config import TABLE_NAME


class Record(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    photo_id = Column(String)
    description = Column(String)

