# coding=utf-8
import logging
from source.exts.cache_manager import cache

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

LANGUAGE_OBJ = {}


def build_key(key):
    return "HUB_%s" % key


def set_cache(**kwargs):
    return set(**kwargs)


def get_cache(**kwargs):
    return get(**kwargs)


def delete_cache(**kwargs):
    return delete(**kwargs)


def set(key, value, timeout=None):
    key = build_key(key=key)
    return cache.set(key=key, value=value, timeout=timeout)


def setnx(key, value, timeout=60):
    key = build_key(key=key)
    return cache.add(key=key, value=value, timeout=timeout)


def get(key, default=None):
    key = build_key(key=key)
    return cache.get(key=key) or default


def delete(key):
    key = build_key(key=key)
    return cache.delete(key=key)

