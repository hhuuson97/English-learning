# coding=utf-8
import logging
from source.models.database import db_session

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class Unauthorized(Exception):
    pass


class NotFound(Exception):
    pass


class BadRequest(Exception):
    pass


class ServiceUnavailable(Exception):
    pass


def on_error(code, message, error=None):
    db_session.rollback()
    errors = None
    try:
        if error:
            if hasattr(error, 'data'):
                if 'errors' in error.data:
                    errors = [itm for itm in error.data['errors']]
                    # message = MSG_MISSING_REQUIRED_FIELD + ": " + ",".join(msg_field)
    except Exception as e:
        print('handle_generic_exception', e)

    return {
               'code': code,
               'errors': errors,
               'message': message
           }, code

# Handle for api v1
# @web_v1_api.errorhandler(mm.ValidationError)
# def on_validate_error(e):
#     """
#     :param mm.ValidationError e:
#     :return:
#     """
#     _logger.exception(e)
#     e.__delattr__('data')
#    return on_error(400, str(e.messages))
