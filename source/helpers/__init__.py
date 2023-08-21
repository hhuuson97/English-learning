import logging

# coding = utf-8
import datetime
import decimal
import enum
import json as _json
import logging
import random
import string
import time
import unicodedata

import json
from dateutil import parser
from sqlalchemy import inspect

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    """Customized flask JSON Encoder"""

    def default(self, o):
        from source import models as m
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, decimal.Decimal):
            if o == o.to_integral_value():
                return int(o)
            else:
                return float(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat(sep=' ')
        if isinstance(o, enum.Enum):
            return o.value
        if isinstance(o, tuple):
            return list(o)
        if isinstance(o, m.db.Model):
            return o.to_dict
        return super().default(o)


_default_json_encoder = JSONEncoder()
json_encode = _default_json_encoder.encode


def json_decode(s):
    """ Decode a json string
    :param str s: the JSON encoded string
    :rtype: mixed
    """
    return _json.loads(s)


def random_str(len, words=string.ascii_letters + string.digits):
    return ''.join([random.choice(words) for i in range(len)])


def random_str_with_time(len, words=string.ascii_letters + string.digits, sep='.'):
    return '%s%s%s' % (time.time(), sep, random_str(len, words))


def reformat_dict(data):
    """

    :param dict:
    :return:
    """
    if not isinstance(data, dict):
        return data
    formated_data = {}
    for key in data:
        formated_key = key
        if isinstance(key, (bytes, bytearray)):
            formated_key = key.decode('utf-8')
        if isinstance(data[key], dict):
            formated_data[formated_key] = reformat_dict(data[key])
        elif isinstance(data[key], (bytes, bytearray)):
            formated_data[formated_key] = data[key].decode('utf-8')
        else:
            formated_data[formated_key] = data[key]
    return formated_data


def rabbitmq_basic_properties_to_dict(properties):
    """ Convert RabbitMQ Basic Properties to Dict
    :param pika.spec.BasicProperties properties:
    :rtype dict:
    """
    if isinstance(properties, dict):
        return reformat_dict(properties)
    return {
        'content_type': properties.content_type,
        'content_encoding': properties.content_encoding,
        'headers': properties.headers,
        'delivery_mode': properties.delivery_mode,
        'priority': properties.priority,
        'correlation_id': properties.correlation_id,
        'reply_to': properties.reply_to,
        'expiration': properties.expiration,
        'message_id': properties.message_id,
        'timestamp': properties.timestamp,
        'type': properties.type,
        'user_id': properties.user_id,
        'app_id': properties.app_id,
        'cluster_id': properties.cluster_id,
    }


def saobj_to_dict(obj):
    """ Convert sqlalchemy object into a dict

    :param obj obj: sqlalchemy object
    :return: dict with key-values is column list
    :rtype: dict[str, mixed]
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def ensure_datetime(val):
    """ Đảm bảo giá trị đầu ra là datetime.datetime. Giá trị đầu vào có thể là:

        * datetime.datetime
        * str: là biểu diễn dạng int của unixtimestamp
        * int: unix timestamp

    :param str|int|datetime val: giá trị cần convert
    :rtype: datetime.datetime
    """
    if not val:
        return None
    if isinstance(val, datetime.datetime):
        return val
    if isinstance(val, (str)):
        val = int(val)
    assert isinstance(val, int), "Undetectable type for datetime.datetime"

    return datetime.datetime.fromtimestamp(val)


def iso_801_to_datetime(iso_801):
    if not iso_801:
        return None
    return datetime.datetime.strptime(iso_801, "%Y-%m-%dT%H:%M:%S.%fZ")


def str_to_datetime(str):
    if not str:
        return None

    return parser.parse(str)


def datetime_2_unixtimestamp(dt, int_type=True):
    """ Return unix timestamp from datetime

    :param datetime.datetime dt: datetime
    :rtype: int
    """
    ut = time.mktime(dt.timetuple())
    if int_type:
        ut = int(ut)
    return ut


def remove_accents(text, is_uri=False):
    if not text:
        return text

    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    return str(text).replace(' ', '') if is_uri else str(text)

