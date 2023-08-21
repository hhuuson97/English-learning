# coding=utf-8
import logging

import jwt
from flask import current_app
from sqlalchemy import or_, and_

from source.helpers import string_helpers, languages_helpers, time_helpers, http_helpers
from source.helpers.contants import COOKIE_KEY, MESSAGES
from source.models.user import User, UserRole

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def check_user_login(username=None, password=None, user_id=None):
    enc_pass = string_helpers.hash_password(password)
    check = User.query.filter(
        or_(
            and_(
                User.username.isnot(None),
                User.username == username
            ),
            and_(
                User.email.isnot(None),
                User.email == username
            ),
            and_(
                User.id.isnot(None),
                User.id == user_id
            ),
        ),
        User.role_id != UserRole.disabled,
        User.password == enc_pass
    ).first()
    return check


def user_login(username=None, password=None, fcm_token=None):
    """
    Xử lý đăng nhập của một user với username và mật khẩu
    :param username:
    :param password:
    :param fcm_token:
    :return:
    """
    check = check_user_login(username, password)
    if check:
        actions = [] if check.password else ["update_password_social"]
        return {
                   # "access_token": gen_jwt_user_token(check, action=actions),
                   "user": check.to_dict,
                   "action": actions
               }, None
    return None, languages_helpers.get(MESSAGES.LOGIN_WRONG_INFO)


def user_logout(access_token=None):
    if not access_token:
        access_token = http_helpers.get_current_headers('Authorization')

    if not access_token:
        access_token = http_helpers.get_current_cookies(COOKIE_KEY.ACCESS_TOKEN)

    if not access_token:
        return

    # return cache_helpers.delete(build_cache_key(access_token))


def validate_jwt_token(token):
    """
    Xác thự JWT token
    :param token:
    :return:
    """
    if not token:
        return None
    try:
        data = jwt.decode(token, key=current_app.config.get('JWT_TOKEN'), algorithms=current_app.config.get('JWT_ALG'))
    except Exception as e:
        _logger.info("Decode token fail: %s - %s", (token, str(e)))
        return None

    if not data:
        return None
    current_time = time_helpers.get_unix_timestamp()

    if current_time > data.get('exp'):
        return None
    # if data.get('iss'):
    #     user_info = get_user_info(data.get('iss'))
    #     return user_info
    if data.get('sid'):
        return {
            "sid": data.get('sid'),
            "action": data.get('action'),
            "need_update_info": True
        }
    return None