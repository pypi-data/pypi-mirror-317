import pandas as pd
from sqlalchemy.orm import Session
from tqdm import tqdm

from cagu_toolkit.common import transactional
from cagu_toolkit.common.utils import *
from cagu_toolkit.modal import Category, LogisticsChannel, Supplier, ExchangeRate, Sku, Product, SkuFreightEstimation, \
    EstimationType


def _load_excel(file_path: str) -> pd.DataFrame:
    """
    加载 Excel 文件并筛选所需列
    """
    try:
        df = pd.read_excel(file_path)
        print(f"成功加载 Excel 文件: {file_path}")
        if df.empty:
            raise CommonException("Excel 文件为空")
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
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


def _import_data(excel_file: str, description, process_row_func):
    df = _load_excel(excel_file)
    _process_with_progress(df, process_row_func, description)


@transactional
def import_categories(excel_file: str, session: Session = None):
    """
    导入类目
    """
    cache = {}  # 初始化缓存

    def process_row(row):
        parent_id = None
        for level in range(4):
            category_name = row.iloc[level]
            if pd.isna(category_name):
                return
            key = (category_name, parent_id)
            if key in cache:
                # 如果缓存命中，直接获取 ID
                parent_id = cache[key]
            else:
                category = session.query(Category).filter_by(name=category_name, parent_id=parent_id).first()
                if not category:
                    category = Category(
                        name=category_name,
                        parent_id=parent_id,
                        description=f"{['一', '二', '三', '四'][level]}级类目"
                    )
                session.add(category)
                session.flush()
                cache[key] = category.id
                parent_id = category.id

    _import_data(excel_file, '导入类目', process_row)


@transactional
def import_logistics_channels(excel_file: str, session: Session = None):
    """
    导入物流渠道
    0: 物流渠道
    1: 物流商
    2: 运输方式
    """

    def process_row(row):
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

    _import_data(excel_file, '导入物流渠道', process_row)


@transactional
def import_suppliers(excel_file: str, session: Session = None):
    """
    导入供应商
    """

    def process_row(row):
        name = row.iloc[0]
        code = row.iloc[1]
        description = row.iloc[2]
        supplier = session.query(Supplier).filter_by(code=code).first()
        if supplier:
            return
        supplier = Supplier(name=name, code=code, description=description)
        session.add(supplier)

    _import_data(excel_file, '导入供应商', process_row)


@transactional
def import_exchange_rates(session: Session = None):
    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1)
    for i in range(24):
        rate = ExchangeRate(batch_id=1, currency_from="CNY", currency_to="JPY", exchange_rate=220000,
                            conversion_time=plus_months(first_day_of_month, i),
                            create_time=plus_months(now, i), update_time=plus_months(now, i))
        session.add(rate)


@transactional
def import_spus(excel_file: str, session: Session = None):
    """
    导入spu
    """

    def process_row(row):
        product = session.query(Product).filter_by(biz_code=row.iloc[0]).first()
        if not product:
            categories = [row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6]]
            first_category = session.query(Category).filter_by(name=row.iloc[3], parent_id=None).first()
            if not first_category:
                raise CommonException(f"所属一级品类不存在: {categories}:{row.iloc[3]}")
            leaf_category_id = first_category.id

            if pd.notna(row.iloc[4]):
                # 如果二级类目不为空
                second_category = session.query(Category).filter_by(name=row.iloc[4],
                                                                    parent_id=first_category.id).first()
                if not second_category:
                    raise CommonException(f"所属二级品类不存在: {categories}:{row.iloc[4]}")
                leaf_category_id = second_category.id

                if pd.notna(row.iloc[5]):
                    # 如果三级类目不为空
                    third_category = session.query(Category).filter_by(name=row.iloc[5],
                                                                       parent_id=second_category.id).first()
                    if not third_category:
                        raise CommonException(f"所属三级品类不存在: {categories}:{row.iloc[5]}")
                    leaf_category_id = third_category.id

                    if pd.notna(row.iloc[6]):
                        # 如果四级类目不为空
                        fourth_category = session.query(Category).filter_by(name=row.iloc[6],
                                                                            parent_id=third_category.id).first()
                        if not fourth_category:
                            raise CommonException(f"所属四级品类不存在: {categories}:{row.iloc[6]}")
                        leaf_category_id = fourth_category.id
            supplier = session.query(Supplier).filter_by(name=row.iloc[13]).first()
            if not supplier:
                raise CommonException(f"供应商查不到: {row.iloc[13]}")

            product = Product(biz_code=row.iloc[0],
                              name=row.iloc[1],
                              leaf_category_id=leaf_category_id,
                              supplier_id=supplier.id)
            session.add(product)
            session.flush()
        sku = session.query(Sku).filter_by(biz_code=row.iloc[2]).first()
        if sku:
            return
        product_length_range = row.iloc[7]
        check_len_value(product_length_range)
        product_width_range = row.iloc[8]
        check_len_value(product_width_range)
        product_height_range = row.iloc[9]
        check_len_value(product_height_range)

        sku = Sku(product_id=product.id,
                  biz_code=row.iloc[2],
                  product_length_range=product_length_range,
                  product_width_range=product_width_range,
                  product_height_range=product_height_range,
                  length_unit=row.iloc[10],
                  net_weight=row.iloc[11],
                  weight_unit=row.iloc[12],
                  purchase_price=row.iloc[14] * 100,
                  currency_type=row.iloc[15])
        session.add(sku)

    _import_data(excel_file, '导入spu', process_row)


@transactional
def import_sku_freight_estimation(excel_file: str, session: Session = None):
    def process_row(row):
        if pd.isna(row.iloc[0]):
            return
        sku = session.query(Sku).filter_by(biz_code=row.iloc[0]).first()
        if not sku:
            raise CommonException(f"未知SKU: {row.iloc[0]}")
        logistics_channel = session.query(LogisticsChannel).filter_by(provider=row.iloc[11],
                                                                      channel=row.iloc[10]).first()
        if not logistics_channel:
            raise CommonException(f"未知物流渠道：{row.iloc[10]}-{row.iloc[11]}")

        estimation_type = EstimationType.from_string(row.iloc[1])
        estimation = (session.query(SkuFreightEstimation)
                      .filter_by(sku_id=sku.id, estimation_type=estimation_type)).first()
        if not estimation:
            estimation = SkuFreightEstimation(
                sku_id=sku.id,
                estimation_type=estimation_type,
                logistics_channel_id=logistics_channel.id,
                mainline_freight=row.iloc[13] * 100,
                last_mile_freight=row.iloc[14] * 100,
                currency_type=row.iloc[16]
            )
            session.add(estimation)

    _import_data(excel_file, '导入运费预估', process_row)
