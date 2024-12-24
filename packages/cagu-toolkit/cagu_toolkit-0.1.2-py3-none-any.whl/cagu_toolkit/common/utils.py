from datetime import datetime

from dateutil.relativedelta import relativedelta


def plus_months(date: datetime, months: int) -> datetime:
    return date + relativedelta(months=+months)
