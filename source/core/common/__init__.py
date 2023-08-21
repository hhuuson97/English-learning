# coding=utf-8
import logging

import flask

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

common_api = flask.Blueprint('app_customer', __name__)


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    app.register_blueprint(common_api)

