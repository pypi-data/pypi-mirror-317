import logging
from importlib.metadata import version

import click

from cagu_toolkit.commands import config, import_data, gpt
from cagu_toolkit.common import CommonException
from cagu_toolkit.common.config import config as conf
from cagu_toolkit.common.logging_config import setup_logging
from cagu_toolkit.service.version import check_version

# 设置日志
setup_logging()

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=version(conf.app_name))
def main():
    """cagu-toolkit"""


# 注册子命令模块
main.add_command(config)
main.add_command(import_data)
main.add_command(gpt)

if __name__ == '__main__':
    try:
        logger.info("Starting cagu-toolkit")
        check_version()
        main()
    except CommonException as ce:
        logger.error("Exception occurred", exc_info=ce)
        click.echo(f"数据异常: {ce.message}", err=True)
    except Exception as e:
        logger.error("Exception occurred", exc_info=e)