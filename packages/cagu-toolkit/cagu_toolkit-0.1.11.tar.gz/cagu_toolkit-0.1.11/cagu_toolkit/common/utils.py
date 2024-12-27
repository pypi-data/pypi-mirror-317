import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from cagu_toolkit.common import CommonException


def plus_months(date: datetime, months: int) -> datetime:
    return date + relativedelta(months=+months)


len_value_pattern = re.compile(r'^(\d+(\.\d+)?(-\d+(\.\d+)?)?)$|^(\d+(\.\d+)?(\|\d+(\.\d+)?)*)$')
num_pattern = re.compile(r'^\d+(\.\d+)?$')


def check_len_value(value) -> None:
    """
    检查长度的值是否符合规范
    """
    if not (value and isinstance(value, str)):
        return

    # 检查字符串是否匹配基本格式
    match = re.match(len_value_pattern, value)
    if match:
        # 如果包含 "-"，确保前面的数字小于后面的数字
        if '-' in value:
            parts = value.split('-')
            if any(not is_num(part) for part in parts):
                raise CommonException(f"{value}，非数字格式")
            if len(parts) == 2 and int(parts[0]) >= int(parts[1]):
                raise CommonException(f"{value}，范围值必须前者小于后者")

        # 如果包含 "|", 确保是合法的枚举格式
        if '|' in value:
            parts = value.split('|')
            if any(not is_num(part) for part in parts):
                raise CommonException(f"{value}，非数字格式")
    else:
        raise CommonException(f"无法识别{value}")


def is_num(value) -> bool:
    match = re.match(num_pattern, value)
    if match:
        return True
    return False
