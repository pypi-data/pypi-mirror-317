import enum
from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

from cagu_toolkit.modal.enum_type_decorator import EnumTypeDecorator

Base = declarative_base()


class EstimationType(enum.Enum):
    SUPPLIER_ESTIMATION = 0  # 供应商预估
    LOGISTICS_GROUP_ESTIMATION = 1  # 物流组预估
    WAREHOUSE_ESTIMATE = 2  # 仓检预估
    SYSTEM_ESTIMATE = 3  # 系统预估

    @classmethod
    def from_string(cls, value: str):
        mapping = {
            "供应商预估": cls.SUPPLIER_ESTIMATION,
            "物流组预估": cls.LOGISTICS_GROUP_ESTIMATION,
            "仓检预估": cls.WAREHOUSE_ESTIMATE,
            "系统预估": cls.SYSTEM_ESTIMATE,
        }
        # 如果字符串存在映射
        if value in mapping:
            return mapping[value]
        else:
            raise ValueError(f"无法找到对应的枚举值: '{value}'")


class SkuFreightEstimation(Base):
    __tablename__ = 'sku_freight_estimation'

    id = Column(BigInteger, primary_key=True)
    sku_id = Column(BigInteger, nullable=False)
    estimation_type = Column(EnumTypeDecorator(EstimationType), nullable=False)
    billing_weight = Column(Integer, nullable=True)
    logistics_channel_id = Column(BigInteger)
    mainline_freight = Column(Integer)
    last_mile_freight = Column(Integer)
    currency_type = Column(String)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
