# coding=utf-8
import logging
import hashlib, binascii

import jwt
from flask import current_app
from sqlalchemy import or_
from source.helpers import cache_helpers, string_helpers, http_helps, languages_helpers, time_helpers
from source.models.user import User, UserRole
from source.helpers.contants import COOKIE_KEY, MESSAGES

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

PASS_SALT = "124xvs5dv"


def update_cache_user(user):
    access_token = http_helps.get_current_cookies(COOKIE_KEY.ACCESS_TOKEN)
    cache_helpers.set(key=build_cache_key(access_token), value=user.to_dict, timeout=7 * 24 * 60 * 60)


def hash_password(password):
    if not password:
        return None
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PASS_SALT.encode('utf-8'),
        100000
    )
    return binascii.hexlify(dk).decode("utf-8")


def check_password(password, hash_str):
    str_enc = hash_password(password)
    return str_enc == hash_str


def build_cache_key(key):
    return "USER_%s" % key


def valid_token(token):
    if not token:
        return None
    data = cache_helpers.get(build_cache_key(token))
    return data


def login(username=None, password=None):
    enc_pass = hash_password(password)
    check = User.query.filter(
        or_(
            User.username == username,
            User.email == username
        ),
        User.role_id != UserRole.disabled,
        User.password == enc_pass
    ).first()
    if check:
        access_token = string_helpers.gen_uuid()
        data = check.to_dict
        data.update({
            COOKIE_KEY.ACCESS_TOKEN: access_token
        })
        cache_helpers.set(key=build_cache_key(access_token), value=data, timeout=7 * 24 * 60 * 60)
        return data, None
    return None, languages_helpers.get(MESSAGES.LOGIN_WRONG_INFO)


def logout(access_token=None):
    if not access_token:
        access_token = http_helps.get_current_headers('Authorization')

    if not access_token:
        access_token = http_helps.get_current_cookies(COOKIE_KEY.ACCESS_TOKEN)

    if not access_token:
        return

    return cache_helpers.delete(build_cache_key(access_token))


def gen_jwt_user_token(user, expire=604800, action=None):
    """
    Tạo mã access_token để trả lại hệ thống khác
    :param user:
    :param expire:
    :param action:
    :return:
    """
    message = {
        'iss': user.id,
        'iat': time_helpers.get_unix_timestamp(),
        'exp': time_helpers.get_unix_timestamp() + expire,
        'sig': string_helpers.md5(user.password),
        'action': action or []
    }
    token = jwt.encode(message, current_app.config.get('JWT_TOKEN'), current_app.config.get('JWT_ALG'))
    set_cache_user_login(user, timeout=current_app.config.get('TIME_CACHE_USER'))
    return {
        "token": token,
        "expire_in": expire
    }


def set_cache_user_login(user, timeout=3600):
    user_cache = build_user_obj_cache(user)
    cache_helpers.set(key=build_cache_key(user.id), value=user_cache, timeout=timeout)
    # if user.profile_url:
    #     cache_helpers.set(key=build_cache_key(user.profile_url), value=user_cache, timeout=timeout)
    return user_cache

def build_user_obj_cache(user):
    """
    :params User user
    """
    user_obj = user.to_dict
    return user_obj
