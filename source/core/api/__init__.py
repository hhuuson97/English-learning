import logging

import flask_restx as _fr
from flask import Blueprint, render_template, request
from flask_restx._http import HTTPStatus
from flask_restx.swagger import Swagger
from flask_restx.utils import not_none

from source.utils import request_log_utils

__author__ = 'VuTNT'
_logger = logging.getLogger('root')

api_blueprint = Blueprint('v1_api', __name__)

api = _fr.Api(
    app=api_blueprint,
    version='1.0',
    title="Hub Connector APIs",
    description=(
        "It is APIs for Hub Connector Service<style>.models {display: none !important}</style>"
    ),
    validate=False,
    add_specs=False,
    doc='/scdocs/',
    tags=[]
)


@api.documentation
def custom_swagger_ui():
    return render_template('swagger-ui.html', title=api.title,
                           specs_url=api.specs_url)


class CustomSwagger(Swagger):
    def serialize_resource(self, ns, resource, url, route_doc=None, **kwargs):
        doc = self.extract_resource_doc(resource, url, route_doc=route_doc)
        tags = (route_doc or {}).get('tags', [])
        if doc is False:
            return
        path = {
            'parameters': self.parameters_for(doc) or None
        }
        for method in [m.lower() for m in resource.methods or []]:
            methods = [m.lower() for m in kwargs.get('methods', [])]
            if doc[method] is False or methods and method not in methods:
                continue
            path[method] = self.serialize_operation(doc, method)
            path[method]['tags'] = tags or [ns.name]
        return not_none(path)


class SwaggerView(_fr.Resource):
    '''Render the Swagger specifications as JSON'''

    def get(self):
        schema = CustomSwagger(api).as_dict()
        return schema, HTTPStatus.INTERNAL_SERVER_ERROR if 'error' in schema else HTTPStatus.OK

    def mediatypes(self):
        return ['application/json']


def _register_specs(app_or_blueprint):
    if api._add_specs:
        endpoint = str('specs')
        api._register_view(
            app_or_blueprint,
            SwaggerView,
            api.default_namespace,
            '/swagger.json',
            endpoint=endpoint,
            resource_class_args=(api,)
        )
        api.endpoints.add(endpoint)


api._register_specs = _register_specs


def init_app(app, **kwargs):
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Health Api
    from .health import init_app as init_health_app
    from .health.urls import init_health_api_url
    init_health_app(app)
    init_health_api_url()

    # Api v1
    from .v1 import init_app as init_api_v1_app
    from .v1.urls import init_v1_web_api_url
    init_api_v1_app(app)
    init_v1_web_api_url()

    # Postman Collection v1 Document
    from .postman import init_app as init_postman_v1_app
    from .postman.urls import init_postman_v1_url
    init_postman_v1_app(app)
    init_postman_v1_url()


class BaseApi(object):

    def response_message(self, code, message):
        return {
            'status': code,
            'message': message
        }

    def return_general(self, code, message, data=None, http_code=None, header=None):
        """ Trả về thông tin 1 lời gọi ReST API tổng quan

        :param int code: Mã trả về
        :param str message: thông tin chi tiết
        :return:
        """

        return {
                   'code': code,
                   'message': message,
                   'data': data
               }, http_code or code

    def return_general_list(self, code, message, data=None, total=None, http_code=None, header=None, **kwargs):
        results = {
            "items": data or [],
            "extra": {**(kwargs.get('extra') or {}), **{
                "paging": {
                    "total": total or 0,
                    "limit": kwargs.get('limit') or 0,
                    "next_token": kwargs.get('next_token') or ""
                }
            }
                      }
        }
        return self.return_general(code=code, message=message, data=results, http_code=http_code, header=header)


class BaseResource(_fr.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            _logger.info('Received data with log:\n'
                         '%s\n'
                         '%s' % (self.endpoint, request.json)
                         )
        except Exception as ex:
            pass
            # _logger.error("Create log request: ", ex)


class BaseLogRequestLogResource(BaseResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_log_id = None
        self.custom_log = None
        self.save_response_log = False
        self.save_log()

    def save_log(self):

        try:
            _logger.info('Received data with log:\n'
                         '%s\n'
                         '%s' % (self.endpoint, request.json)
                         )
            rq = request_log_utils.handel_save_request()
            if rq:
                self.custom_log = rq
                self.custom_log_id = rq.id

        except Exception as ex:
            _logger.error("Create log request: ", ex)


class BaseLogRequestLogApi(BaseApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_log(self, data):
        try:
            if self.custom_log and self.save_response_log:
                self.custom_log.update(data[0] if data and isinstance(data, tuple) and len(data) > 0 else data)
        except Exception as ex:
            _logger.error("Update log request: ", ex)

    def response_message(self, code, message):
        data = super().response_message(code, message)
        self.update_log(data)
        return data

    def return_general(self, code, message, data=None, http_code=None):
        data = super().return_general(code, message, data, http_code)
        self.update_log(data)
        return data


class BaseTransactionsLogResource(BaseLogRequestLogResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_log(self):

        try:
            _logger.info('Received data with log:\n'
                         '%s\n'
                         '%s' % (self.endpoint, request.json)
                         )
            rq = request_log_utils.handel_save_request(save_type='transaction')
            if rq:
                self.custom_log = rq
                self.custom_log_id = rq.id

        except Exception as ex:
            _logger.error("Create log request: ", ex)


from .errors import *
