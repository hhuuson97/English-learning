# coding=utf-8
import logging
import flask

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def get_current_headers(key=None, default=None):
    headers = {}
    if flask.has_app_context() and flask.has_request_context():
        headers = flask.request.headers
        if key:
            return headers[key] if key in headers else default
        return headers
    return headers if not key else default


def get_current_cookies(key=None, default=None):
    cookies = {}
    if flask.has_app_context() and flask.has_request_context():
        cookies = flask.request.cookies
        if key:
            return cookies[key] if key in cookies else default
        return cookies
    return cookies if not key else default


def is_ajax_request():
    header = get_current_headers('Content-Type')
    return header and ('form' in header  or 'json' in header)
