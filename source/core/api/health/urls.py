def init_health_api_url():
    from . import health_api
    from .core.health import HealthLive, HealthPing

    health_api.add_resource(HealthPing, '/ping')
    health_api.add_resource(HealthLive, '/live')
