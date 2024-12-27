from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(BigInteger, primary_key=True)
    biz_code = Column(String)
    delivery_code = Column(String)
    leaf_category_id = Column(BigInteger)
    name = Column(String)
    design_theme = Column(String)
    supplier_id = Column(BigInteger)
    brand_id = Column(BigInteger)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
