# coding=utf-8
import logging
from source.core import api
from source.utils import setting_utils

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class WebSettings(api.v1.BaseResource, api.v1.BaseApi):
    def get(self):
        """ Lấy các settings

        """
        data = setting_utils.get_settings_for_web()
        return self.return_general(200, 'OK', data)
