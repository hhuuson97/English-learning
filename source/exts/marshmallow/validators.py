# coding=utf-8
import logging
from marshmallow.validate import *

__author__ = 'Tarzan'
_logger = logging.getLogger(__name__)


# class NotExistOnColumn(Validator):
#
#     default_message = '{value} already exists on {column}'
#
#     def __init__(self, col, message=None):
#         """ Verify for not existing on a column
#
#         :param sqlalchemy.orm.attributes.InstrumentedAttribute col:
#             SQLAlchemy ORM column
#         """
#         self._col = col
#         self._cls = col.class_
#         self.message = message or self.default_message
#
#     def _repr_args(self):
#         return str(self._col)
#
#     def _format_error(self, value):
#         return self.message.format(value=value, column=self._col)
#
#     def __call__(self, val):
#         obj = self._cls.query.filter(self._col == val).first()
#         if obj:
#             raise ValidationError(self._format_error(val))


class ExistOnColumn(Validator):

    default_message = '{value} does not exists on {column}'

    def __init__(self, col, message=None):
        """ Verify for existing on a column

        :param sqlalchemy.orm.attributes.InstrumentedAttribute col:
            SQLAlchemy ORM column
        """
        self._col = col
        self._cls = col.class_
        self.message = message or self.default_message

    def _repr_args(self):
        return str(self._col)

    def _format_error(self, value):
        return self.message.format(value=value, column=self._col)

    def __call__(self, val):
        obj = self._cls.query.filter(self._col == val).first()
        if not obj:
            raise ValidationError(self._format_error(val))


class IsNone(Validator):
    """Chỉ cho phép giá trị None"""
    def __call__(self, value):
        if value is not None:
            raise ValidationError('%s is not None' % value)


class Any(Validator):
    """ Chỉ cần thỏa mãn ít nhất 1 validator, không tính thứ tự
    """
    def __init__(self, *validators):
        """
        :param list[Validator] validators:
        """
        self.validators = validators

    def __call__(self, value):
        if not len(self.validators):
            return

        errors = []
        for validator in self.validators:
            try:
                validator(value)
                break
            except ValidationError as e:
                errors.append(e)
        else:
            assert errors, 'Must have at least 1 error'
            raise errors[0]

#
# class PhoneNumber(Regexp):
#
#     def __init__(self, regex=None, flags=0, error=None):
#         regex = regex or r'^(\+84)?\d+$'
#         super().__init__(regex, flags, error)

class StringIsNotNoneAndNull(Validator):
    """Chỉ cho phép giá trị khác None"""
    def __call__(self, value):
        if value is None or value == "":
            raise ValidationError('%s is None or Null' % value)