import datetime
import time

import pytz


def current_date(days=0):
    """
    获取当前日期：XXXX-XX-XX
    days: 0-代表当天，如果要表示前几天，则 > 0 的对应数字即可；如果要表示后几天，则 < 0 的对应数字即可，
    :return: <class 'datetime.date'>
    """
    current_date_ = datetime.date.today() - datetime.timedelta(days=days)
    return current_date_


def current_time():
    """
    获取当前时间：HH:MM:SS
    :return: str
    """
    now_time = datetime.datetime.now()
    delta = datetime.timedelta(days=0)
    n_date = now_time + delta
    current_time_ = n_date.strftime('%H:%M:%S')
    return current_time_


def date_format(area, source_date):
    """
    转换为标准的日期格式 XXXX-XX-XX
    :param area: 地区，用来设置时区的
    :param source_date:
    :return: str
    """
    from datetime import datetime
    try:
        date_str = source_date.split('GMT')[0].strip()
        date_ = '%a %b %d %Y %H:%M:%S'
        dt_ = datetime.strptime(date_str, date_)
        # 设置时区
        tz = pytz.timezone(area)
        dt = tz.localize(dt_)
        result_date = dt.strftime('%Y-%m-%d')
    except ValueError:
        result_date = source_date

    return result_date


def datetime_exchange(source_date):
    """
    转换为标准的日期格式 XXXX-XX-XX HH:MM:SS
    :param source_date:
    :return: str
    """
    if source_date is None:
        return source_date
    elif source_date == datetime.datetime(1970, 1, 1, 8, 0):
        return 0
    else:
        return source_date.strftime('%Y-%m-%d %H:%M:%S')


def date_to_timestamp(date_str: str, time_zone):
    """
        转换为指定日期00点的时间戳
        :param date_str: 指定的日期
        :param time_zone: 时区
        :return: int
    """
    from datetime import datetime
    # 将字符串转换为日期对象
    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # 获取零点
    datetime_with_time_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    # 将字符串解析为 datetime 对象
    naive_datetime = datetime.strptime(datetime_with_time_str, '%Y-%m-%d %H:%M:%S')

    # 设置 UTC 时区
    utc_timezone = pytz.utc

    # 将 naive datetime 转换为 UTC 时间
    utc_datetime = utc_timezone.localize(naive_datetime)

    # 设置的时区
    country_timezone = pytz.timezone(time_zone)

    # 将 UTC 时间转换为时区的时间
    country_datetime = utc_datetime.astimezone(country_timezone)

    # 获取时区时间的时间戳
    country_timestamp = int(country_datetime.timestamp())

    return country_datetime, country_timestamp


def generate_hour_list(max_hour=24):
    """
    生成一个24小时列表
    """
    hour_list = [{'label': f'{i} hour', 'key': i} for i in range(1, max_hour + 1)]
    return hour_list


def datetime_format(day_=0):
    """
    格式化日期%Y%m%d%H%M%S
    return: str
    """
    day_n = int(day_)
    now_ = datetime.datetime.now()
    delta = datetime.timedelta(days=day_n)
    now_date = now_ + delta
    result = now_date.strftime('%Y%m%d%H%M%S')
    return result
