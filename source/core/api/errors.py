# coding=utf-8
import logging

from source.exts.action_lock import ObjNotFound
from source.core.api import api
from source.models.database import db_session
import flask_principal
from source.exts import marshmallow as mm
from source.helpers import sentry_helpers, languages_helpers, contants

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
               'message': languages_helpers.get(contants.MESSAGES.HTTP_500)
           }, code


@api.errorhandler(mm.ValidationError)
def on_validate_error(e):
    """

    :param mm.ValidationError e:
    :return:
    """
    # e.messages
    _logger.exception(e)
    e.__delattr__('data')
    return on_error(400, str(e.messages))


@api.errorhandler(flask_principal.PermissionDenied)
def on_unauthorized(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(403, languages_helpers.get(contants.MESSAGES.HTTP_403))


@api.errorhandler(NotFound)
def not_found(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(404, str(e) or languages_helpers.get(contants.MESSAGES.HTTP_404))


@api.errorhandler(ObjNotFound)
def action_lock_not_found(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(404, str(e) or languages_helpers.get(contants.MESSAGES.HTTP_404))


@api.errorhandler(BadRequest)
def bad_request(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(400, str(e) or languages_helpers.get(contants.MESSAGES.HTTP_400), e)


@api.errorhandler(ServiceUnavailable)
def service_unavailable(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(503, str(e) or languages_helpers.get(contants.MESSAGES.HTTP_503))


@api.errorhandler
def on_unknown_exception(e):
    sentry_helpers.send_error_to_sentry(e)
    return on_error(500, str(e) or languages_helpers.get(contants.MESSAGES.HTTP_500))


class HandleSpecialError():
    def __init__(self, registers):
        """

        :param Object registers:
        """
        self._registers = registers
        for cls in registers:
            api.errorhandler(cls)(self.error_handler)

    def error_handler(self, e):
        sentry_helpers.send_error_to_sentry(e)
        cls = e.__class__

        handler = self._registers[cls]
        if isinstance(handler, (tuple, list)):
            code, msg = self._registers[cls]
            return on_error(code, msg or str(e))

        if callable(handler):
            rv = handler(e)
            if isinstance(rv, (list, tuple)):
                code, msg = rv
            else:
                code, msg = 400, rv
            return on_error(code, msg or str(e))

        assert False, 'Invalid handler: %s' % handler
