from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger, nullable=True)
    name = Column(String)
    description = Column(String)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
