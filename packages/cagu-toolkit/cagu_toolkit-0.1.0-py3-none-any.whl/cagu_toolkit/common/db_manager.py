from functools import wraps
from typing import Callable, Any
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from cagu_toolkit.common.context import get_context
from cagu_toolkit.common.config_manager import load_config

import logging

logger = logging.getLogger(__name__)

def create_engine_from_config(profile: str):
    config = load_config()
    db_config = config.get(profile)
    if not db_config:
        raise ValueError(f"未找到环境为 {profile} 的配置。")

    user = db_config['username']
    password = quote(db_config['password'])
    host = db_config['host']
    port = db_config['port']
    database = db_config['database']

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
        connect_args={"charset": "utf8mb4"},
        pool_size=5,
        # echo=True
        logging_name='cagu_toolkit_db'
    )
    return engine


def get_session(profile: str) -> Session:
    engine = create_engine_from_config(profile)
    return sessionmaker(bind=engine)()


# 装饰器实现
def transactional(func: Callable) -> Callable:
    """
    通用事务管理装饰器
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session: Session = kwargs.get('session')
        if not session:
            profile = get_context()
            session = get_session(profile)
        try:
            kwargs['session'] = session  # 将 session 注入到目标函数中
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            logger.error("db exception", exc_info=e)
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
