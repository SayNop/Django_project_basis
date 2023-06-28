import time
from datetime import datetime, timedelta
# these function return type: datetime, timestamp, str


date_format_str = '%Y-%m-%d'
time_format_str = '%Y-%m-%d %H:%M:%S'


# return the day before target day
def before_date(days, start_time=None):
    """
    return the day before target day
    :param days: interval days
    :param start_time: datetime obj
    :return: datetime obj
    """
    if not start_time:
        start_time = datetime.today() - timedelta(days=days)

    return start_time - timedelta(days=days)


def str2datetime(date_str, format_str=time_format_str):
    """
    str to datetime
    :param date_str: time str
    :param format_str: time str format
    :return: datetime obj
    """
    return datetime.strptime(date_str, format_str)


def datetime2str(d, format_str=time_format_str):
    """
    datetime to str
    :param d: datetime obj
    :param format_str: time str format
    :return: time str
    """
    return datetime.strftime(d, format_str)


def str2timestamp(date_str, format_str=time_format_str):
    """
    str to timestamp
    :param date_str: time str
    :param format_str: time str format
    :return: timestamp(number)
    """
    return time.mktime(time.strptime(date_str, format_str))


def datetime2timestamp(date):
    """
    datetime to timestamp
    :param date: datetime obj
    :return: timestamp(number)
    """
    return datetime.timestamp(date)


def timestamp2datetime(timestamp):
    """
    timestamp to datetime
    :param timestamp: timestamp(number)
    :return: datetime obj
    """
    return datetime.fromtimestamp(timestamp)


def timestamp2str(timestamp, format_str=time_format_str):
    """
    timestamp to str
    :param timestamp: timestamp(number)
    :param format_str: time str format
    :return: time str
    """
    return time.strftime(format_str, time.localtime(timestamp))
