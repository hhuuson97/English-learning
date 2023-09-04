# coding=utf-8
import logging
from source.models.database import db_session
from source.models.env_settings import EnvSettings
from source.helpers import cache_helpers
from source.helpers.cache_helpers import cache

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

key_cache_settings = "all_settings"


def init_all_setting():
    """
    Khởi tạo tất cả các setting và lưu vào cách
    :return:
    """
    try:
        data = EnvSettings.query.filter(EnvSettings.status.is_(True)).with_entities(
            EnvSettings.name,
            EnvSettings.group,
            EnvSettings.value
        ).all()
    except:
        return
    result = {}
    for r in data:
        name, group, value = r
        if group:
            key_group = "GROUP_%s" % group
            if key_group not in result:
                result[key_group] = {}

            result[key_group][name] = value
        result[name] = value

    cache_helpers.set(key=key_cache_settings, value=result, timeout=180 * 24 * 60 * 60)
    cache.delete_memoized(get_settings_for_web)


def get(name=None, group=None, default=None, convert_dict=True):
    """
    Lấy một setting theo name hoặc group
    :param name:
    :param group:
    :param default:
    :param convert_dict:
    :return:
    """
    results = cache_helpers.get(key=key_cache_settings, default={})
    if group:
        key_group = "GROUP_%s" % group
        results = results.get(key_group) or default

        if not name and not convert_dict:
            return [{"name": key, "value": value} for key, value in results.items()]

    if name:
        results = results.get(name) or default

    return results


def get_from_db(name=None, group=None, default=None, convert_dict=True):
    """
    Lấy danh sách các settings từ database
    :param name:
    :param group:
    :param default:
    :param convert_dict:
    :return:
    """
    query = EnvSettings.query.filter(EnvSettings.status.is_(True)).with_entities(EnvSettings.name, EnvSettings.value)
    if group:
        res = query.filter(EnvSettings.group == group).all()
        if name:
            for r in res:
                if r[0] == name:
                    return r[1].strip()
            return default
        if convert_dict:
            data = {}
            for r in res:
                data[r[0].strip()] = r[1].strip()
            return data
        return [{"name": r[0], "value": r[1].strip()} for r in res] if res else default
    elif name:
        res = query.filter(EnvSettings.name == name).first()
        return res[1] if res else default
    return default


def set(name, value, group=None):
    query = [
        EnvSettings.name == name,
        EnvSettings.status.is_(True)
    ]
    if group:
        query.append(EnvSettings.group == group)

    res = EnvSettings.query.filter(*query).first()
    if res:
        res.value = str(value)
    else:
        db_session.add(
            EnvSettings(
                name=name.upper(),
                group=group.upper(),
                value=str(value)
            ))
        db_session.commit()
    init_all_setting()


@cache.memoize(timeout=86400)
def get_settings_for_web():
    """
    Lấy tất cả các setting cho web
    :return arr:
    """
    data = EnvSettings.query.filter(EnvSettings.display_for_web.is_(True), EnvSettings.status.is_(True)).with_entities(
        EnvSettings.name, EnvSettings.value).all()
    results = {}
    for itm in data:
        results[itm[0].strip()] = itm[1].strip()
    return results
