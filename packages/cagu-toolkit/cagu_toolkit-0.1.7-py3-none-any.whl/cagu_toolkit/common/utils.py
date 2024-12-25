from datetime import datetime
import re

from dateutil.relativedelta import relativedelta

from cagu_toolkit.common import CommonException


def plus_months(date: datetime, months: int) -> datetime:
    return date + relativedelta(months=+months)


def check_len_value(value):
    """
    检查长度的值是否符合规范
    """
    # 正则表达式：匹配 "1-10"、"1"、"1|10" 或 "100-200" 格式
    pattern = r'^\d+(-\d+)?(\|\d+)?$'

    # 检查字符串是否匹配基本格式
    match = re.match(pattern, value)
    if match:
        # 如果包含 "-"，确保前面的数字小于后面的数字
        if '-' in value:
            parts = value.split('-')
            if any(not part.isdigit() for part in parts):
                raise CommonException(f"{value}，非数字格式")
            if len(parts) == 2 and int(parts[0]) >= int(parts[1]):
                raise CommonException(f"{value}，范围值必须前者小于后者")

        # 如果包含 "|", 确保是合法的枚举格式
        if '|' in value:
            parts = value.split('|')
            if any(not part.isdigit() for part in parts):
                raise CommonException(f"{value}，非数字格式")
    else:
        raise CommonException(f"{value}")