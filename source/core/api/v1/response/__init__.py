# coding=utf-8
import enum
import json
import logging

import flask_restx as fr

from source.core.api import api

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class EnumValue(fr.fields.String):
    def format(self, enum_type):
        if isinstance(enum_type, enum.Enum):
            return enum_type.value

        return


class MoneyValue(fr.fields.String):
    def format(self, value):
        value_arr = list(str(int(value)))
        value_arr.reverse()
        return_val = ""
        count = 0
        for v in value_arr:
            if count > 0 and count / 3 == count // 3:
                return_val = '.' + return_val
            return_val = v + return_val
            count += 1
        return return_val


class UserNameValue(fr.fields.String):
    _max_name_len = 0

    def __init__(self, max_name_len=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_name_len = max_name_len or 0

    def format(self, value):
        return " ".join((value or "").split(" ")[-self._max_name_len:])


class ValidJsonField(fr.fields.Raw):
    def format(self, value):
        try:
            if value is None:
                return value
            data = json.loads(value)
            if not isinstance(data, (dict, tuple)) and data is not None and (
                    isinstance(data, str) and (data.startswith('{') or data.startswith('['))):
                data = json.loads(data)
            return data
        except Exception as e:
            print("Parse json field error %s" % str(e))
        return value

    def _serialize(self, value, attr, obj):
        try:
            if value is None:
                return {}
            data = json.loads(value)
            return data
        except Exception as e:
            pass
        return value

GENERAl = api.model(
    'GeneralResponse', {
        'code': fr.fields.Integer(description='HTTP code'),
        'message': fr.fields.String()
    }
)
