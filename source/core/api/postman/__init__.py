# coding=utf-8
import logging
from flask_restx import Namespace
from source.core import api as base_api

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

postman_v1_api = Namespace('postman', 'Postman Collection v1 APIs')


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    base_api.api.add_namespace(postman_v1_api)


class BaseApi(base_api.BaseApi):
    # Custom handle here
    pass


class BaseResource(base_api.BaseResource):
    # Custom handle here
    pass


class BaseLogRequestLogResource(BaseResource):
    # Custom handle here
    pass


class BaseLogRequestLogApi(base_api.BaseApi):
    # Custom handle here
    pass
