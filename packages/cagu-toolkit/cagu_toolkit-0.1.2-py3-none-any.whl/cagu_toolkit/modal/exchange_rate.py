from datetime import datetime

from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExchangeRate(Base):
    __tablename__ = 'exchange_rate'
    id = Column(BigInteger, primary_key=True)
    batch_id = Column(Integer, nullable=False)
    currency_from = Column(String, nullable=False)
    currency_to = Column(String, nullable=False)
    conversion_time = Column(DateTime, nullable=False)
    exchange_rate = Column(BigInteger, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)