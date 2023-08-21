import logging

from source.core import api
from source.helpers.http_request import HttpRequest

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)
# coding=utf-8

class DemoApi(api.v1.BaseResource, api.v1.BaseApi):
    def get(self, service):
        """ Demo call http api
        """
        # GET HttpRequest.get(uri, dict params)
        uri = "uri_sample"
        results = HttpRequest.get(uri,
                                  {
                                      "param": "value"
                                  })
        # POST HttpRequest.post(uri, data=dict data)
        results = HttpRequest.post(uri, data={
                                      "param": "value"
                                  })

        # PUT HttpRequest.put(uri, data=dict data)
        results = HttpRequest.put(uri, data={
            "param": "value"
        })
        return self.return_general(200, 'OK', results)
