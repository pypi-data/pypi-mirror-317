from datetime import datetime

import click
from tabulate import tabulate

from cagu_toolkit.common.config_manager import load_config, save_config


@click.group()
def config():
    """配置管理"""
    pass


@config.command()
def add():
    """创建配置"""
    click.echo("请输入数据库配置信息：")
    host = click.prompt("主机", type=str, default="127.0.0.1")
    port = click.prompt("端口", type=int, default=3306)
    username = click.prompt("用户名", type=str)
    password = click.prompt("密码", type=str, hide_input=True)
    database = click.prompt("数据库名称", type=str)
    profile = click.prompt("给你的环境起一个名字吧", type=str, default="default")

    new_config = {
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'database': database,
        'create_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    conf = load_config()
    conf[profile] = new_config
    save_config(conf)

    click.echo(f"配置 {profile} 已保存！")


@config.command()
def list():
    """列出所有配置"""
    conf = load_config()
    if not conf:
        click.echo("没有找到任何配置。", err=True)
        return
    click.echo("当前配置列表：")
    data = []
    for profile, details in conf.items():
        data.append([profile, details['create_at']])
    tab = tabulate(data, ['环境', '创建时间'])
    click.echo(f"{tab}")


@config.command()
@click.argument("profile", type=str)
def get(profile):
    """查看配置"""
    conf = load_config()
    if not conf:
        click.echo("没有找到任何配置。", err=True)
        return
    current_conf = conf[profile]
    for key, value in current_conf.items():
        click.echo(f"{key}: {value}")


@config.command()
@click.argument("profile", type=str)
def delete(profile):
    """查看配置"""
    conf = load_config()
    if not conf:
        click.echo("没有找到任何配置。", err=True)
        return
    current_conf = conf[profile]
    if not current_conf:
        click.echo(f"没有找到 {profile} 配置", err=True)
    del conf[profile]
    save_config(conf)
    click.echo(f"删除 {profile} 配置成功")
