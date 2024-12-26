import logging
import os
import subprocess
import time
from importlib.metadata import version

import click
import requests

from cagu_toolkit.common.config import config

logger = logging.getLogger(__name__)


def get_latest_version(package_name):
    """从 PyPI 获取最新版本"""
    try:
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        response.raise_for_status()
        data = response.json()
        v = data['info']['version']
        logger.info(f"Found latest version: {data['info']}")
        return v
    except requests.RequestException:
        return None


def prompt_for_update(package_name, latest_version, current_version):
    """提示用户是否更新"""
    click.echo(f"检测到新版本！当前版本: {current_version}, 最新版本: {latest_version}")
    update = click.confirm('是否更新到最新版本?', default=True)
    if update:
        click.echo("正在更新到最新版本...")
        # 这里可以添加实际的更新逻辑，例如调用 pip 更新
        subprocess.run(['pip', 'install', '--upgrade', package_name])
    else:
        click.echo("保持当前版本。")


def should_check_version():
    """判断是否需要检查版本"""
    if os.path.exists(config.last_check_file):
        with open(config.last_check_file, "r") as f:
            last_check_time = float(f.read().strip())
            logger.info(f"last check time: {last_check_time}")
        current_time = time.time()
        return (current_time - last_check_time) > config.check_version_interval
    return True  # 文件不存在时，强制检查


def update_last_check_time():
    """更新最后检查时间"""
    with open(config.last_check_file, "w") as f:
        f.write(str(time.time()))


def check_version():
    """在执行每个命令前检查版本"""
    logger.info("Starting check version")
    if should_check_version():
        logger.info("Do check version")
        current_version = version(config.app_name)
        latest_version = get_latest_version(config.app_name)
        logger.info(f"Current version: {current_version}, Latest version: {latest_version}")
        if latest_version and latest_version != current_version:
            logger.info("Starting to update version")
            prompt_for_update(config.app_name, latest_version, current_version)
        update_last_check_time()  # 记录检查时间
