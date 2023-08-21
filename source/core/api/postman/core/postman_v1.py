# coding=utf-8
import logging

from source.core import api
from source.core.api import api as rest_api
from ...postman.core import postman

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)


class PostmanDoc(api.postman.BaseResource, api.postman.BaseApi):
    def get(self):
        urlvars = False  # Build query strings in URLs
        swagger = True  # Export Swagger specifications
        data = postman.PostmanCollectionV1(rest_api, swagger=swagger).as_dict(urlvars=urlvars)
        for r in data['requests']:
            r['url'] = r['url'].replace(rest_api.base_url, "{{host}}/")
            r['headers'] = r['headers'].replace('Authorization:', 'Authorization:{{access_token}}')
        return data
