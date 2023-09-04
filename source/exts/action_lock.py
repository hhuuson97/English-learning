"""
This module provides:

  - a class to prevent an action to be occured many times in a timespan
  - use caching to prevent it

"""
from source import models as m
import functools
import inspect
import werkzeug.exceptions as _excs
from sqlalchemy import event
from source.helpers import cache_helpers

_DEFAULT_TIMESPAN = 5  # 10 seconds


class TooManyActionError(_excs.TooManyRequests):
    pass


class ObjNotFound(_excs.BadRequest):

    def __init__(self, cls, key):
        description = '%s#%s not found' % (cls, key)
        super().__init__(description)


class ObjLock(object):
    """Lock 1 object để thực hiện 1 hành động
    1. Lock khi được gọi (decorator, with statement)
    2. Release lock tại thời điểm DB commit gần nhất hoặc (timestpan sau
    3. Nếu acquire lock

    Usage:
        with ObjLock(10, m.BlNew):
            pass

        class SomeClass(object):
            @ObjLock.lock(m.BlNew)
            def update_obj(id, *args, **kwargs):
                pass
    """
    _obj_cls = None
    lock_key_format = None

    def __init__(self, key_value, obj_cls=None, timespan=_DEFAULT_TIMESPAN):
        """
        :param key_value: thông tin để lấy đối tượng này, mặc định là id
        :param obj_cls: tên Model class để lấy đối tượng này
        :param int timespan: thời gian tối đa release lock
        """
        self._key_value = key_value
        if obj_cls:
            assert not self._obj_cls, 'Can not overwrite self._obj_cls'
            self._obj_cls = obj_cls
        self.timespan = timespan
        if not self.lock_key_format:
            self.lock_key_format = '%s-%%s' % self.__class__.__name__
        self._obj = self._get_obj()
        self._lock_key = self.lock_key_format % self._get_obj_identity()

        # event.listen(
        #     m.db.session,
        #     'after_commit',
        #     self._on_session_commit
        # )
        # event.listen(
        #     m.db.session,
        #     'after_rollback',
        #     self._on_session_rollback
        # )

    # def _on_session_rollback(self, session):
    #     self.release()

    # def _on_session_commit(self, session):
    #     self.release()

    def _get_obj(self):
        """ Lấy Obj instance

        :rtype: object
        """
        obj = m.db.session.query(self._obj_cls).get(self._key_value)
        if not obj:
            raise ObjNotFound(self._obj_cls, self._key_value)

        return obj

    def _get_obj_identity(self, obj=None):
        """ Lấy định danh của Obj

        :rtype: str
        """
        obj = obj or self._obj
        return m.db.inspect(obj).identity[0]

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if exc_type: # there's an exception
        self.release()
        # TODO: release if session commited
        # default will release after timeout
        pass

    def acquire(self):
        """ Verify wherether any action occured in last self.timespan seconds

        Raise self.exc if there is.
        If not, mark the action occured
        """
        if cache_helpers.cache.get(self._lock_key):
            raise TooManyActionError(
                'Too many actions on %s in last %d seconds' % (
                    self._obj,
                    self.timespan
                )
            )

        cache_helpers.cache.set(
            self._lock_key,
            1,
            timeout=self.timespan,
        )

    def release(self):
        cache_helpers.cache.delete(self._lock_key)

    @classmethod
    def lock(cls, obj_cls=None, timespan=_DEFAULT_TIMESPAN):
        """ Sử dụng như 1 decorator cho 1 function.
            1. Lấy tham số đầu tiên của function làm obj_key
            2. Nếu không có tham số theo thứ tự, lấy tham số keyword 'id'

        :param obj_cls: class của object cần lock. Mặc định là của class Lock
        :param int timespan: thời gian timeout
        :return:
        """
        def decorator(fn):
            def get_key_value(*args, **kwargs):
                if len(args) > 0:
                    key_val = args[0]
                else:
                    try:
                        key_val = kwargs['id']
                    except KeyError as e:
                        raise ValueError(
                            '%s: Can not detect identity with function %s' % (
                                cls,
                                fn
                            ))
                return key_val

            @functools.wraps(fn)
            def wrapper(self, *args, **kwargs):
                key_value = get_key_value(*args, **kwargs)
                locker = cls(
                    key_value,
                    obj_cls=obj_cls,
                    timespan=timespan
                )
                with locker:
                    return fn(self, *args, **kwargs)
            return wrapper
        return decorator
