# coding=utf-8
import logging
from datetime import datetime

import pytz
from dateutil import tz

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def date_str_to_zone_obj(date_str, format_str='%d/%m/%Y %H:%M:%S', in_timezone="UTC", out_timezone="Asia/Ho_Chi_Minh",
                         output_format_str=None):
    if not date_str:
        return None
    dt = datetime.strptime(date_str, format_str)
    local = pytz.timezone(in_timezone)
    local_dt = local.localize(dt, is_dst=None)
    out_dt = local_dt.astimezone(pytz.timezone(out_timezone))
    if output_format_str:
        return out_dt.strftime(output_format_str)
    return out_dt


def date_str_to_utc_obj(date_str, format_str='%d/%m/%Y %H:%M:%S', timezone="Asia/Ho_Chi_Minh", output_format_str=None):
    if not date_str:
        return None
    dt = datetime.strptime(date_str, format_str)
    local = pytz.timezone(timezone)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    if output_format_str:
        return utc_dt.strftime(output_format_str)
    return utc_dt


def datetime_to_utc(current_datetime, current_timezone="UTC"):
    local = pytz.timezone(current_timezone)
    local_dt = local.localize(current_datetime, is_dst=None)
    return local_dt.astimezone(tz.tzutc())


def datetime_utc_to_zone_time(utc_datetime, to_zone=None):
    if not to_zone:
        to_zone = tz.tzlocal()
    else:
        to_zone = pytz.timezone(to_zone)
    return utc_datetime.astimezone(to_zone)


def format_db_time_to_user_time(db_time, format_str=None, timezone="Asia/Ho_Chi_Minh"):
    if not db_time:
        return ""
    if not format_str:
        format_str = '%Y-%m-%d %H:%M:%S'
    db_time = datetime_to_utc(db_time)
    return_time = datetime_utc_to_zone_time(db_time, timezone)
    return return_time.strftime(format_str)


def get_unix_timestamp(timezone="UTC"):
    return int(datetime.now(tz=pytz.timezone(timezone)).timestamp())


def current_tz_date(timezone="Asia/Ho_Chi_Minh"):
    return datetime_utc_to_zone_time(datetime.utcnow(), timezone)
