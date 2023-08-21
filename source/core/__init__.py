# coding=utf-8
import logging
from flask import render_template
from source.helpers import languages_helpers, contants, http_helpers

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    from . import api, admin, common
    from .common.urls import init_common_api_url
    # Treat - Fix me
    init_common_api_url()

    common.init_app(app, **kwargs)
    api.init_app(app, **kwargs)
    admin.init_app(app, **kwargs)

    @app.errorhandler(404)
    def page_not_found(e):
        if http_helpers.is_ajax_request():
            return {
                       "code": 404,
                       "message": languages_helpers.get(contants.MESSAGES.HTTP_404)
                   }, 404
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def _forbidden(e):
        if http_helpers.is_ajax_request():
            return {
                       "code": "403",
                       "message": languages_helpers.get(contants.MESSAGES.HTTP_403)
                   }, 403
        return render_template("403.html"), 403
