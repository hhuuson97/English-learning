# coding=utf-8
import logging
import json
import urllib
import traceback
import urllib.parse

import urllib3
from requests import request
from source.utils import request_log_utils

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class HttpRequest:
    _UTF8 = 'utf-8'
    _MAX_TIMEOUT = 20

    _http = urllib3.PoolManager()
    _save_func = request_log_utils.save_http

    def __init__(self):
        pass

    @staticmethod
    def save_log(url, method, headers, body, response):
        HttpRequest._save_func(url=url, type='http', header=headers, body=body, method=method, response=response)

    @staticmethod
    def get(url, query_strings=None, headers=None, json_output=True, is_log=True, timeout=None):
        result = None
        response = None
        msq_err = None
        try:
            response = HttpRequest._http.request('GET', url, fields=query_strings, headers=headers,
                                                 timeout=timeout or HttpRequest._MAX_TIMEOUT)
        except Exception as e:
            _logger.exception(e)
            msq_err = traceback.format_exc()
        if response and response.data:
            decoded = response.data.decode(HttpRequest._UTF8)
            result = decoded
            if json_output:
                try:
                    result = json.loads(result)
                except Exception as e:
                    pass
        if is_log:
            HttpRequest.save_log(url=url, method='GET', headers=headers, body=query_strings, response=result or msq_err)
        return result

    @staticmethod
    def post(url, query_string_data=None, data=None, headers={}, json_output=True, send_form_data_instead_of_json=False,
             verify=None, is_log=True, timeout=None):
        return HttpRequest._post_put_delete('POST', url, query_string_data, data, headers, json_output,
                                            send_form_data_instead_of_json, verify, is_log, timeout=timeout)

    @staticmethod
    def put(url, query_string_data=None, data=None, headers={}, json_output=True, send_form_data_instead_of_json=False,
            verify=None, is_log=True, timeout=None):
        return HttpRequest._post_put_delete('PUT', url, query_string_data, data, headers, json_output,
                                            send_form_data_instead_of_json, verify, is_log, timeout=timeout)

    @staticmethod
    def delete(url, query_string_data=None, data=None, headers={}, json_output=True,
               send_form_data_instead_of_json=False, verify=None, is_log=True):
        return HttpRequest._post_put_delete('DELETE', url, query_string_data, data, headers, json_output,
                                            send_form_data_instead_of_json, verify, is_log)

    @staticmethod
    def _post_put_delete(method, url, query_string_data=None, data=None, headers={}, json_output=True,
                         send_form_data_instead_of_json=False, verify=None, is_log=True, timeout=None):
        result = None
        response = None
        msq_err = None

        if not timeout:
            timeout = HttpRequest._MAX_TIMEOUT

        encoded_data = data if send_form_data_instead_of_json else json.dumps(data)
        encoded_args = urllib.parse.urlencode(query_string_data) if query_string_data is not None else ''
        url = '{}?{}'.format(url, encoded_args) if encoded_args else url
        if not send_form_data_instead_of_json:
            headers['Content-Type'] = 'application/json'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        try:
            if verify is None:
                response = HttpRequest._http.request(method, url, fields=encoded_data,
                                                     headers=headers,
                                                     timeout=timeout) if send_form_data_instead_of_json \
                    else HttpRequest._http.request(method, url, body=encoded_data, headers=headers, timeout=timeout)
            else:
                response = request(method, url, data=encoded_data, headers=headers, verify=verify, timeout=timeout)
        except Exception as e:
            _logger.exception(e)
            msq_err = traceback.format_exc()

        if response and (hasattr(response, 'data') or hasattr(response, 'text')):
            result = getattr(response, 'data') if hasattr(response, 'data') else getattr(response, 'text')
            if json_output:
                try:
                    result = json.loads(result)
                except Exception as e:
                    pass

        if is_log:
            HttpRequest.save_log(url=url, method=method, headers=headers, body=data, response=result or msq_err)
        return result
