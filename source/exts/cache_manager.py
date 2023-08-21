# coding=utf-8
import logging
import flask_caching

__author__ = 'Link'
_logger = logging.getLogger(__name__)

cache = flask_caching.Cache()


def init_app(app, **kwargs):
    cache.init_app(app)
