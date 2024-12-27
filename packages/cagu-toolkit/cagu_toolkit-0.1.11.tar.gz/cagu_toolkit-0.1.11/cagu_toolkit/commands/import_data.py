import click

from cagu_toolkit.common.context import set_context
from cagu_toolkit.service import data_importer as di


@click.group(name='import')
@click.option('--profile', '-p', required=True, type=str, help="请指定环境", default='default')
def import_data(profile):
    """数据导入"""
    click.echo(f"使用环境: {profile}")
    set_context(profile)
    pass


@import_data.command(name='exchange-rate')
def command_exchange_rate():
    """导入汇率数据"""
    di.import_exchange_rates()
    click.echo("汇率数据已成功导入！")


@import_data.command(name='category')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定Excel文件路径"
)
def command_category(file):
    """导入类目数据"""
    di.import_categories(excel_file=file)
    click.echo("类目数据已成功导入！")


@import_data.command(name='logistics-channel')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定Excel文件路径"
)
def import_logistics_channel(file):
    """导入物流渠道数据"""
    di.import_logistics_channels(excel_file=file)
    click.echo("物流渠道数据已成功导入！")


@import_data.command(name='supplier')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定Excel文件路径"
)
def import_supplier(file):
    """导入供应商"""
    di.import_suppliers(excel_file=file)
    click.echo("供应商数据已成功导入")


@import_data.command(name='spu')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定Excel文件路径"
)
def import_spu(file):
    """导入产品、SKU数据"""
    di.import_spus(excel_file=file)
    click.echo("产品、SKU数据已成功导入")


@import_data.command(name='estimation')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定Excel文件路径"
)
def import_product(file):
    """导入运费预估样本数据"""
    di.import_sku_freight_estimation(excel_file=file)
    click.echo("运费预估样本数据已成功导入")
