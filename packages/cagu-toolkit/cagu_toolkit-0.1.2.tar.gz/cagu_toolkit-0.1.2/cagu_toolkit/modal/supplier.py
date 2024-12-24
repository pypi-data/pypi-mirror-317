from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)