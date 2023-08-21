# coding=utf-8
import logging
from flask_restx import Namespace
from source.core import api as base_api

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

health_api = Namespace('health', 'Health Check APIs')


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    base_api.api.add_namespace(health_api)


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
