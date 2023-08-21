# coding=utf-8
import logging
import flask
from flask_login import current_user
import copy
import json as _json
from source.models.database import db_session
from source.models.http_log import HttpLog
from source.helpers.http_helpers import get_client_ip

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def handle_save_request(type_log=None, save_type=None):
    if flask.has_app_context():
        request = flask.request
        headers = request.headers
        cookies = request.cookies

        try:
            body = request.json
        except:
            body = None
        try:
            param = request.args
        except:
            param = None

        url = request.path

        header = {}
        try:
            header = dict(copy.deepcopy(cookies))
            if 'Authorization' in headers:
                header['Authorization'] = headers['Authorization']
            if 'Content-Type' in headers:
                header['Content-Type'] = headers['Content-Type']
            if 'User-Agent' in headers:
                header['User-Agent'] = headers['User-Agent']
            if 'HTTP_USER_AGENT' in headers:
                header['HTTP_USER_AGENT'] = headers['HTTP_USER_AGENT']
            if 'Accept' in headers:
                header['Accept'] = headers['Accept']
        except Exception as e:
            _logger.info('Get headers:', e)

        client_ip = None
        try:
            client_ip = get_client_ip()
        except Exception as e:
            _logger.info('Get clientIp:', e)
        return _save_log(
            cls=HttpLog,
            url=url,
            body=body,
            param=param,
            header=header,
            user_id=current_user.user_id if current_user and hasattr(current_user, 'user_id') else None,
            type=type_log,
            method=request.method,
            client_ip=client_ip,
            uri_pattern=str(request.url_rule)
        )
    return None


def save_http(url=None, type=None, header=None, body=None, param=None, **kwargs):
    return _save_log(HttpLog, url, type, header, body, param, **kwargs)


def _save_log(cls, url=None, type=None, header=None, body=None, param=None, **kwargs):
    request_log = None
    try:
        request_log = cls()
        request_log.url = url
        request_log.body = _json.dumps(body) if body else None
        request_log.header = _json.dumps(header) if header else None
        request_log.param = _json.dumps(param) if param else None
        request_log.user_id = kwargs.get('user_id')
        request_log.response = _json.dumps(kwargs.get('response')) if kwargs.get('response') else None
        request_log.method = kwargs.get('method')
        request_log.user_agent = kwargs.get('user_agent') or (header.get('User-Agent') if header else None)
        request_log.client_ip = kwargs.get('client_ip')
        request_log.uri_pattern = kwargs.get('uri_pattern')
        request_log.type = type
        db_session.add(request_log)
        db_session.commit()
    except Exception as ex:
        _logger.error(ex)

    return request_log


def update_log(cls, id, response):
    try:
        if id and response:
            rq = cls.query.filter(cls.id == id).first()
            rq.update(response)
    except Exception as ex:
        _logger.error(ex)
