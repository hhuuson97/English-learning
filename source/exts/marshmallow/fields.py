# coding=utf-8
""" Chứa các công cụ cho việc validate Schema by Marshmallow
"""
import datetime
import logging

import decimal
from marshmallow.fields import *
from . import validators

__author__ = 'Tarzan'
_logger = logging.getLogger(__name__)


class String(String):

    def _deserialize(self, value, attr, data):
        if not isinstance(value, str):
            value = str(value)
        if isinstance(value, str):
            value = value.strip()
            if value.lower() == "null":
                value = None
        return super()._deserialize(value, attr, data)


class PureInteger(Integer):
    default_error_messages = {
        'invalid_type': '({type}){value} Invalid integer value'
    }

    def __init__(self, min=None, max=None, zero_none=False, **kwargs):
        """
        :param min:
        :param max:
        :param bool zero_none: Có convert giá trị 0 sang None hay không?
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.zero_none = zero_none
        if min is None: min = 1;

        if self.zero_none:
            self.validators.append(
                validators.Any(
                    validators.IsNone(),
                    validators.Range(min=min, max=max)
                )
            )
        else:
            self.validators.append(validators.Range(min=min, max=max))

    def _format_num(self, value):
        if value is None:
            return None
        if not isinstance(value, int):
            self.fail('invalid_type', type=type(value), value=value)
        return super()._format_num(value)

    def _deserialize(self, value, attr, data):
        value = super()._deserialize(value, attr, data)
        if self.zero_none and not value:
            value = None
        return value


class UnixTimestamp(PureInteger):
    default_error_messages = {
        'invalid': 'Invalid unix timestamp value {type}({value})',
        'future': '{value} ({iso_time}) is future time. Now is {now}',
    }

    def __init__(self, allow_future=False, **kwargs):
        self.allow_future = allow_future
        super().__init__(**kwargs)

    def _validate(self, value):
        if isinstance(value, datetime.datetime):
            dt = value
            value = int(value.timestamp())
        elif isinstance(value, int):
            dt = datetime.datetime.fromtimestamp(value)
        else:
            self.fail('invalid_type', type=type(value), value=value)

        now = datetime.datetime.now()
        if not self.allow_future and dt > now:
            self.fail('future', value=value, iso_time=dt, now=now.isoformat())

    def _serialize(self, value, attr, obj):
        self._validate(value)
        if isinstance(value, datetime.datetime):
            return int(value.timestamp())
        if isinstance(value, int):
            return value

    def _deserialize(self, value, attr, data):
        value = super()._deserialize(value, attr, data)
        self._validate(value)
        dt = datetime.datetime.fromtimestamp(value)
        return dt


class JsUnixTimestamp(UnixTimestamp):
    def _validate(self, value):
        if isinstance(value, datetime.datetime):
            dt = value
            value = int(value.timestamp())
        elif isinstance(value, int):
            dt = datetime.datetime.fromtimestamp(value / 1000)
        else:
            self.fail('invalid_type', type=type(value), value=value)

        now = datetime.datetime.now()
        if not self.allow_future and dt > now:
            self.fail('future', value=value, iso_time=dt, now=now.isoformat())

    def _deserialize(self, value, attr, data):
        value = PureInteger._deserialize(self, value, attr, data)
        self._validate(value)
        dt = datetime.datetime.fromtimestamp(value / 1000.0)
        return dt


class NotEmptyString(String):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.insert(
            0,
            validators.Length(1)
        )


class EmptyNoneString(String):
    """ String, Nếu empty thì chuyển thành None

    """

    def __init__(self, **kwargs):
        kwargs.setdefault('allow_none', True)
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data):
        val = super()._deserialize(value, attr, data)
        if not val:
            return None
        return val


class MoneyAmount(Integer):
    num_type = decimal.Decimal

    def __init__(self, as_string=False, **kwargs):
        super().__init__(as_string, **kwargs)
        self.validators.insert(0, validators.Range(min=0))

    def _format_num(self, value):
        if value is None:
            return 0
        if not isinstance(value, int):
            value = int(value)
        return super()._format_num(value)

    def _serialize(self, value, attr, obj):
        return int(value)

class DiscountMoneyAmount(Integer):
    num_type = decimal.Decimal

    def __init__(self, as_string=False, **kwargs):
        super().__init__(as_string, **kwargs)
        # self.validators.insert(0, validators.Range(min=0))

    def _format_num(self, value):
        if value is None:
            return 0
        if not isinstance(value, int):
            value = int(value)
        return super()._format_num(value)

    def _serialize(self, value, attr, obj):
        return int(value)

class Email(Email):

    def __init__(self, allow_empty=True, **kwargs):
        self.allow_empty = allow_empty
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data):
        if isinstance(value, str):
            value = value.strip()
        return super()._deserialize(value, attr, data)

    def _validate(self, value):
        if not value and self.allow_empty:
            return
        return super()._validate(value)
