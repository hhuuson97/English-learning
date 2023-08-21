# coding=utf-8
import logging

__author__ = 'VuTNT'

_logger = logging.getLogger(__name__)


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    from . import login_manager, cache_manager, jinja2, authz

    cache_manager.init_app(app, **kwargs)
    login_manager.init_app(app, **kwargs)
    jinja2.init_app(app, **kwargs)
    authz.init_app(app)
