import pandas as pd
from sqlalchemy.orm import Session
from tqdm import tqdm

from cagu_toolkit.common import transactional
from cagu_toolkit.common.exceptions import CommonException
from cagu_toolkit.common.utils import *
from cagu_toolkit.modal import Category, LogisticsChannel, Supplier, ExchangeRate, Sku, Product, SkuFreightEstimation, \
    EstimationType


def _load_excel(file_path: str, usecols: list[int] = None) -> pd.DataFrame:
    """
    加载 Excel 文件并筛选所需列
    """
    try:
        # noinspection PyTypeChecker
        df = pd.read_excel(file_path, usecols=usecols)
        print(f"成功加载 Excel 文件: {file_path}")
        if df.empty:
            raise CommonException("Excel 文件为空")
        return df
    except CommonException as e:
        raise e
    except Exception as e:
        raise CommonException(f"无法读取 Excel 文件 {file_path}") from e


def _process_with_progress(df: pd.DataFrame, process_row, description: str):
    """
    遍历 DataFrame 并显示进度条
    """
    with tqdm(total=len(df), desc=description, unit="行", dynamic_ncols=True) as bar:
        for index, row in df.iterrows():
            process_row(row)
            bar.update(1)


def _get_or_create(session, model, filter_conditions, create_data):
    """
    获取或创建一个数据库实体
    """
    instance = session.query(model).filter_by(**filter_conditions).first()
    if not instance:
        instance = model(**create_data)
        session.add(instance)
    return instance


def _import_data(excel_file: str, description, columns: list, process_row_func, session: Session):
    df = _load_excel(excel_file, usecols=columns or {})

    def process_row(row):
        process_row_func(row, session)

    _process_with_progress(df, process_row, description)


def process_category_row(row, session: Session):
    parent_id = None
    for level in range(4):
        category_name = row.iloc[level]
        if pd.isna(category_name):
            return
        category = _get_or_create(session, Category,
                                  {'name': category_name, 'parent_id': parent_id},
                                  {'name': category_name, 'parent_id': parent_id,
                                   'description': f"{['一', '二', '三', '四'][level]}级类目"})
        parent_id = category.id


@transactional
def import_categories(excel_file: str, session: Session = None):
    """
    导入类目
    """
    _import_data(excel_file, '导入类目', [0, 1, 2, 3], process_category_row, session)


def process_logistics_channel_row(row, session: Session):
    if pd.isna(row.iloc[0]):
        return
    channel = session.query(LogisticsChannel).filter_by(channel=row.iloc[0], provider=row.iloc[1]).first()
    if not channel:
        channel = LogisticsChannel(
            provider=row.iloc[1],
            channel=row.iloc[0],
            shipping_method=row.iloc[2]
        )
        session.add(channel)


@transactional
def import_logistics_channels(excel_file: str, session: Session = None):
    """
    导入物流渠道
    0: 物流渠道
    1: 物流商
    2: 运输方式
    """
    _import_data(excel_file, '导入物流渠道', [0, 1, 2], process_logistics_channel_row, session)


def process_supplier_row(row, session: Session):
    name = row.iloc[0]
    code = row.iloc[1]
    description = row.iloc[2]
    supplier = session.query(Supplier).filter_by(name=name).first()
    if supplier:
        return
    supplier = Supplier(name=name, code=code, description=description)
    session.add(supplier)


@transactional
def import_suppliers(excel_file: str, session: Session = None):
    """
    导入供应商
    """
    _import_data(excel_file, '导入供应商', [0, 1, 2], process_supplier_row, session)


@transactional
def import_exchange_rates(session: Session = None):
    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1)
    for i in range(24):
        rate = ExchangeRate(batch_id=1, currency_from="CNY", currency_to="JPY", exchange_rate=220000,
                            conversion_time=plus_months(first_day_of_month, i),
                            create_time=plus_months(now, i), update_time=plus_months(now, i))
        session.add(rate)


def process_spu_row(row, session: Session):
    product = session.query(Product).filter_by(biz_code=row.iloc[0]).first()
    if product:
        return
    first_category = session.query(Category).filter_by(name=row.iloc[3], parent_id=None).first()
    if not first_category:
        raise CommonException(f"所属一级品类不存在: {row.iloc[3]}")
    second_category = session.query(Category).filter_by(name=row.iloc[4], parent_id=first_category.id).first()
    if not second_category:
        raise CommonException(f"所属二级品类不存在: {row.iloc[4]}")
    third_category = session.query(Category).filter_by(name=row.iloc[5], parent_id=second_category.id).first()
    if not third_category:
        raise CommonException(f"所属三级品类不存在: {row.iloc[5]}")
    fourth_category = session.query(Category).filter_by(name=row.iloc[6], parent_id=third_category.id).first()
    if not fourth_category:
        raise CommonException(f"所属四级品类不存在: {row.iloc[6]}")
    supplier = session.query(Supplier).filter_by(name=row.iloc[13]).first()
    if not supplier:
        raise CommonException(f"供应商查不到: {row.iloc[13]}")

    product = Product(biz_code=row.iloc[0],
                      name=row.iloc[1],
                      leaf_category_id=fourth_category.id,
                      supplier_id=supplier.id)
    session.add(product)
    session.flush()
    sku = session.query(Sku).filter_by(biz_code=row.iloc[2]).first()
    if sku:
        return
    sku = Sku(product_id=product.id,
              biz_code=row.iloc[2],
              product_length_range=row.iloc[7],
              product_width_range=row.iloc[8],
              product_height_range=row.iloc[9],
              length_unit=row.iloc[10],
              net_weight=row.iloc[11],
              weight_unit=row.iloc[12],
              purchase_price=row.iloc[14] * 100,
              currency_type=row.iloc[15])
    session.add(sku)


@transactional
def import_spus(excel_file: str, session: Session = None):
    """
    导入spu
    """
    _import_data(excel_file, '导入spu', {}, process_spu_row, session)


def process_freight_estimation_row(row, session: Session):
    if pd.isna(row.iloc[0]):
        return
    sku = session.query(Sku).filter_by(biz_code=row.iloc[0]).first()
    if not sku:
        raise CommonException(f"未知SKU: {row.iloc[0]}")
    logistics_channel = session.query(LogisticsChannel).filter_by(provider=row.iloc[11],
                                                                  channel=row.iloc[10]).first()
    if not logistics_channel:
        raise CommonException(f"未知物流渠道：{row.iloc[10]}-{row.iloc[11]}")

    estimation = SkuFreightEstimation(
        sku_id=sku.id,
        estimation_type=EstimationType.from_string(row.iloc[1]),
        logistics_channel_id=logistics_channel.id,
        mainline_freight=row.iloc[13] * 100,
        last_mile_freight=row.iloc[14] * 100,
        currency_type=row.iloc[16]
    )
    session.add(estimation)


@transactional
def import_sku_freight_estimation(excel_file: str, session: Session = None):
    _import_data(excel_file, '导入运费预估', None, process_freight_estimation_row, session)
