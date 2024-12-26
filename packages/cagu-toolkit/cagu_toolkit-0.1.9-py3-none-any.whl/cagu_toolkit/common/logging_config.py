import logging

from cagu_toolkit.common.config import config


def setup_logging():
    """设置全局日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s %(filename)s:%(lineno)d - %(message)s",
        handlers=[
            logging.FileHandler(config.log_file)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured.")
