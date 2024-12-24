from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Sku(Base):
    __tablename__ = 'sku'
    id = Column(BigInteger, primary_key=True)
    product_id = Column(BigInteger)
    biz_code = Column(String)
    material = Column(String)
    color = Column(String)
    other_spec = Column(String)
    product_length_range = Column(String)
    product_width_range = Column(String)
    product_height_range = Column(String)
    length_unit = Column(String)
    gross_weight = Column(Integer)
    net_weight = Column(Integer)
    weight_unit = Column(String)
    purchase_price = Column(BigInteger)
    cost_price = Column(BigInteger)
    selling_price = Column(BigInteger)
    currency_type = Column(String)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
