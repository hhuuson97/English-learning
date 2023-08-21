def init_v1_web_api_url():
    def join_tags(tags=None):
        return {
            "name": "V1",
            "tags": ['v1'] + (tags or ['v1_other'])
        }

    from . import web_v1_api

    from .core.settings import WebSettings
    from .core.demo import DemoApi
    from .core.voice import VoiceApi
    from .core.library import LibraryApi

    # Web Settings
    web_v1_api.add_resource(WebSettings, '/settings', route_doc=join_tags(['v1_settings']))

    # Demo Api
    web_v1_api.add_resource(DemoApi, '/demo', route_doc=join_tags(['v1_demo']))

    # Voice Api
    web_v1_api.add_resource(VoiceApi, '/voice', route_doc=join_tags(['v1_voice']))

    # Library Api
    web_v1_api.add_resource(LibraryApi, '/library', route_doc=join_tags(['v1_library']))
