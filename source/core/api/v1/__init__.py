# coding=utf-8
import functools
import logging
from werkzeug import exceptions as _excs
import flask_login

import flask_restx as _fr
import uuid as _uuid
from flask_restx import Namespace
from source.models.user import UserRole
from source.helpers import languages_helpers, contants
from source.core import api as base_api

web_v1_api = Namespace('v1', 'Api version 1')

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    base_api.api.add_namespace(web_v1_api)


class BaseApi(base_api.BaseApi):
    # Custom handle here
    pass


class BaseResource(base_api.BaseResource):
    # Custom handle here
    pass


class BaseLogRequestLogResource(base_api.BaseLogRequestLogResource):
    # Custom handle here
    pass


class BaseLogRequestLogApi(base_api.BaseLogRequestLogApi):
    # Custom handle here
    pass


class BaseTransactionsLogResource(base_api.BaseTransactionsLogResource):
    pass


def wrap_data(namespace):
    uuid = _uuid.uuid1()

    return base_api.api.model(
        'Data-%s' % uuid, {
            'code': _fr.fields.Integer(),
            'data': _fr.fields.Nested(namespace),
            'message': _fr.fields.String()
        }
    )


def token_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            e = _excs.Unauthorized(
                description=languages_helpers.get(contants.MESSAGES.HTTP_401)
            )
            e.data = {
                'code': e.code,
                'message': e.description,
            }
            raise e
        return fn(*args, **kwargs)

    return wrapper


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not flask_login.current_user.is_authenticated \
                or flask_login.current_user.role_id == UserRole.disabled or not flask_login.current_user.is_active:
            e = _excs.Unauthorized(
                description=languages_helpers.get(contants.MESSAGES.HTTP_401)
            )
            e.data = {
                'code': e.code,
                'message': e.description,
            }
            raise e
        return fn(*args, **kwargs)

    return wrapper


from . import exception
from . import request
from . import response

