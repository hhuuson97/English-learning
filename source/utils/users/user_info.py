import logging

from flask import current_app

from source.helpers import cache_helpers
from source.models.user import User, UserRole
from source.utils.user_utils import build_cache_key, build_user_obj_cache

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)


def get_user_info(user_id):
    """
    Lấy thông tin của một user theo ID, Ưu tiên lấy từ cache -> db
    :param user_id:
    :return: dict|None
    """
    cache_data = get_cache_user_login(user_id)
    if cache_data:
        return cache_data

    info = User.query.filter(User.id == user_id,
                             User.role_id != UserRole.disabled
                             ).first()
    if info:
        set_cache_user_login(info, timeout=current_app.config.get('TIME_CACHE_USER'))
        data = cache_helpers.get(key=build_cache_key(user_id))
        return data
    return None


def set_cache_user_login(user, timeout=3600):
    user_cache = build_user_obj_cache(user)
    cache_helpers.set(key=build_cache_key(user.id), value=user_cache, timeout=timeout)
    # if user.profile_url:
    #     cache_helpers.set(key=build_cache_key(user.profile_url), value=user_cache, timeout=timeout)
    return user_cache


def get_cache_user_login(user_id):
    user_data = cache_helpers.get(key=build_cache_key(user_id))
    if user_data and not user_data.get('_just_updated_2_2_2'):
        return None
    return user_data
