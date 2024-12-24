from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LogisticsChannel(Base):
    __tablename__ = 'logistics_channel'
    id = Column(Integer, primary_key=True)
    provider = Column(String)
    channel = Column(String)
    shipping_method = Column(String)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
