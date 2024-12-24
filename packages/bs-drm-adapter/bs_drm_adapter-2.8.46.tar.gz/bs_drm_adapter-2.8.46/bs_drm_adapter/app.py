import logging
import os
import yaml
import io
import json
import warnings
from flask import Flask, request
from flask_restful import Resource, Api
from bs_drm_adapter import DrmAdapterError, get_adapter
from logging import getLogger
from logging.config import dictConfig
from werkzeug.middleware.profiler import ProfilerMiddleware

from bs_drm_adapter.adapters import profile_to_subscriber_map


warnings.filterwarnings(action='ignore',module='.*secretstorage.*')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] <%(process)d> %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
api = Api(app)

def load_configuration(configuration_file):
    with io.open(configuration_file, 'r') as cf:
        conf = yaml.safe_load(cf)

    return conf


def get_adapter_options():
    try:
        return app.config['DRM_ADAPTER_CONFIG']['drm_adapter_options']
    except KeyError:
        return {}


def get_configuration(key, mandatory=True, default=None):
    try:
        return app.config['DRM_ADAPTER_CONFIG'][key]
    except KeyError:
        if mandatory and default is None:
            raise DrmAdapterError(f'Missing mandatory configuration key {key}', 101)
        else:
            return default


app.config['CONFIGURATION_FILE'] = os.getenv('BS_DRM_ADAPTER_CONFIGURATION', '../os/bs-drm-adapter.yml')
app.config['DRM_ADAPTER_CONFIG'] = load_configuration(app.config['CONFIGURATION_FILE'])

app.logger.debug(f"Service configuration: {app.config['DRM_ADAPTER_CONFIG']}")

# Set up logging
log_level = get_configuration('log_level', mandatory=False, default='INFO')
app.logger.info(f"Switching log level to {log_level}")
app.logger.setLevel(log_level)
getLogger('zeep.transports').setLevel(log_level)
getLogger('bs_drm_adapter.adapters').setLevel(log_level)

adapter = get_adapter(get_configuration('drm_adapter_mode'))(get_configuration('service_routing_host'),
                                                             get_configuration('minimum_entitlement_validity',
                                                                               mandatory=False,
                                                                               default=0),
                                                             get_configuration('content_entitlement_check',
                                                                               mandatory=False,
                                                                               default=True),
                                                             get_configuration('force_device_id_check',
                                                                               mandatory=False,
                                                                               default=True),
                                                             get_configuration('map_profile_to_subscriber',
                                                                               mandatory=False,
                                                                               default=False),
                                                             get_configuration('map_profile_fallback_to_subscriber',
                                                                               mandatory=False,
                                                                               default=False),
                                                             **get_configuration('drm_adapter_options',
                                                                                 mandatory=False,
                                                                                 default={}))
app.logger.info(f"Initialized DRM adapter in {get_configuration('drm_adapter_mode')} mode")

if get_configuration('profile_app', mandatory=False, default=False):
    pfile = open(get_configuration('profile_file', mandatory=False, default='../logs/profile.log'), 'w+')
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, stream=pfile, sort_by=['cumtime'], restrictions=[30])


class Entitlement(Resource):
    def post(self):
        data = request.get_json() if request.is_json else json.loads(request.data)

        return adapter.check_entitlement(data)


class Status(Resource):
    def get(self):
        return {'routing_host': get_configuration('service_routing_host'),
                'adapter_mode': get_configuration('drm_adapter_mode'),
                'status': 'ok'}

class Map(Resource):
    def get(self):
        profile = request.args.get('profile')
        if profile:
            subscriber = profile_to_subscriber_map.get(profile)
            if subscriber:
                return {'profile': profile, 'subscriber': subscriber}, 200
            else:
                return {'error': 'Profile not found'}, 404
        return {'profile_to_subscriber_map': profile_to_subscriber_map}, 200

    def post(self):
        data = request.data.decode('utf-8')
        if not data:
            return {'error': 'Invalid input'}, 400

        try:
            lines = data.splitlines()
            for line in lines:
                profile, subscriber = line.split(',')
                profile_to_subscriber_map[profile] = subscriber
                logging.info(f"Updated profile_to_subscriber_map: {profile} -> {subscriber}")
        except Exception as e:
            return {'error': str(e)}, 400

        return {'status': 'ok'}


entitlement_resources = [
    '/drm-adapter/entitlement'
]

status_resources = [
    '/drm-adapter/status'
]

map_resources = [
    '/drm-adapter/map',
]

api.add_resource(Entitlement, *entitlement_resources)
api.add_resource(Status, *status_resources)
api.add_resource(Map, *map_resources)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9010, debug=False)
