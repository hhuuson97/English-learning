def init_postman_v1_url():
    from . import postman_v1_api
    from .core.postman_v1 import PostmanDoc

    postman_v1_api.add_resource(PostmanDoc, '/postman_v1')
