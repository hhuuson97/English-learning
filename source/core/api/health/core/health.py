# coding=utf-8
import logging

from source.core import api

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)


class HealthPing(api.health.BaseResource, api.health.BaseApi):
    def get(self):
        """ Kiểm tra connect

        """
        return self.return_general(200, 'OK', {"ping": True})


class HealthLive(api.health.BaseResource, api.health.BaseApi):
    def get(self):
        """ Kiểm tra connect service

        """
        return self.return_general(200, 'OK', {"ping": True})
