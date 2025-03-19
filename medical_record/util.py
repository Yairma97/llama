from datetime import datetime

from dateutil.relativedelta import relativedelta


def calculate_age(birthdate: str) -> str:
    """
    根据生日计算年龄。
    :param birthdate: 生日日期，格式为 "YYYY-MM-DD"
    :return: 年龄
    """
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = relativedelta(today, birthdate).years
    return str(age)
