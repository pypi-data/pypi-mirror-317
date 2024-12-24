import logging
from abc import ABC, abstractmethod
from datetime import datetime as dt
from datetime import timedelta as td
from functools import lru_cache

import pytz
from zeep import Client, Settings
from zeep.cache import InMemoryCache
from zeep.exceptions import Error
from zeep.transports import Transport

profile_to_subscriber_map = {}

class DrmAdapterError(Exception):
    def __init__(self, error_message='Unknown error', error_code=500):
        """
        List of error codes:
            100 - Unsupported adapter
            101 - Missing mandatory configuration key
            104 - DRM check failed
            105 - Invalid request data
            106 - Unable to map profileUid to subscriberUid
            200 - Other adapter specific errors
        """
        self.error_message = error_message
        self.error_code = error_code


class DrmAdapter(ABC):
    _provider_name = None

    def __init__(self, obapi_host, minimum_entitlement_validity=0, content_entitlement_check=True,
                 force_device_check=True, map_profile_to_subscriber=False, map_profile_fallback_to_subscriber=False):
        self.drm_api_client = Client(wsdl=f'{obapi_host}/OB/drm/endpoint?wsdl',
                                     transport=Transport(cache=InMemoryCache(timeout=3600)),
                                     settings=Settings(strict=False))
        self.user_api_client = Client(wsdl=f'{obapi_host}/OB/user/endpoint?wsdl',
                                      transport=Transport(cache=InMemoryCache(timeout=3600)),
                                      settings=Settings(strict=False))
        self.logger = logging.getLogger(__name__)
        self.minimum_entitlement_validity = int(minimum_entitlement_validity)
        self.content_entitlement_check = content_entitlement_check
        self.force_device_check = force_device_check
        self.map_profile_to_subscriber = map_profile_to_subscriber
        self.map_profile_fallback_to_subscriber = map_profile_fallback_to_subscriber

    @property
    def name(self):
        return self._provider_name

    def _check_drm_api(self, subscriber_uid, device_uid=None, content_uid=None):
        drm_entitlement_request = self.drm_api_client.get_type('ns0:DrmEntitlementRequest')
        req = drm_entitlement_request(subscriberUid=self._map_profile_to_subscriber(subscriber_uid) if self.map_profile_to_subscriber else subscriber_uid,
                                     deviceUid=device_uid if self.force_device_check else None,
                                     drmProviderUid=self._provider_name,
                                     drmContentUid=content_uid if self.content_entitlement_check else None)

        try:
            res = self.drm_api_client.service.checkEntitlement(req)
        # This is not the most beautiful handling of exception but as we're only converting and not actually handling
        # it should be fine.
        except Error as e:
            raise DrmAdapterError(e.message, 104)

        return res

    @lru_cache(maxsize=65536, typed=False)
    def _map_profile_to_subscriber(self, subscriber_uid):

        if subscriber_uid in profile_to_subscriber_map:
            mapped_subscriber_uid = profile_to_subscriber_map.get(subscriber_uid)
            self.logger.info(f"Mapped profileUid: {subscriber_uid} to subscriberUid: {mapped_subscriber_uid}")
            return mapped_subscriber_uid
        else:
            self.logger.info(f"No mapping found for profileUid temporarily will return -1 (indicating regardless permission): {subscriber_uid}")
        return -1

    def check_entitlement(self, request_data):
        try:
            data = self.parse_request_data(request_data)
            self.logger.debug(f"Parsed request data: {data}")
        except DrmAdapterError as e:
            return self.prepare_not_entitled_response(e.error_message)

        try:
            drm_entitlement = self._check_drm_api(**data)

            if drm_entitlement['entitlement'] == 'GRANTED':
                utc = pytz.timezone('UTC')
                minimum_validity = dt.now(tz=pytz.UTC) + td(seconds=self.minimum_entitlement_validity)
                entitlement_validity = utc.localize(dt.strptime(drm_entitlement['validTill'], '%Y-%m-%d'))
                entitlement_validity = max(entitlement_validity, minimum_validity)
                self.logger.info(f"Entitlement for content \"{data['content_uid']}\" GRANTED to requester "
                                 f"\"{data['subscriber_uid']}\" by DRM API, "
                                 f"entitlement valid until \"{entitlement_validity.strftime('%Y-%m-%d %H:%M:%S')}\"")
                return self.prepare_entitled_response(entitlement_validity,
                                                      **data)
            else:
                self.logger.info(f"Entitlement for content \"{data['content_uid']}\" NOT GRANTED to requester "
                                 f"\"{data['subscriber_uid']}\" by DRM API")
                return self.prepare_not_entitled_response()
        except DrmAdapterError as e:
            self.logger.info(f"Entitlement for content \"{data['content_uid']}\" NOT GRANTED to requester "
                             f"\"{data['subscriber_uid']}\" due to error: \"<{e.error_code}> {e.error_message}\"")
            return self.prepare_not_entitled_response(e.error_message)

    @abstractmethod
    def prepare_entitled_response(self, validity, subscriber_uid, device_uid=None, content_uid=None, http_code=None):
        pass

    @abstractmethod
    def prepare_not_entitled_response(self, message=None, http_code=None):
        pass

    @abstractmethod
    def parse_request_data(self, data):
        """
        Must return dictionary with keys: subscriber_uid, device_uid, content_uid
        """
        pass


class CastlabsAdapter(DrmAdapter):
    _provider_name = 'castlabs'
    _supported_profiles = ['purchase', 'rental']

    def __init__(self, obapi_host, minimum_entitlement_validity, content_entitlement_check, force_device_check,
                 map_profile_to_subscriber, map_profile_fallback_to_subscriber, redirect_url, profile='rental',
                 crt_response_properties=None):
        super().__init__(obapi_host, minimum_entitlement_validity, content_entitlement_check, force_device_check,
                         map_profile_to_subscriber, map_profile_fallback_to_subscriber)
        self.redirect_url = redirect_url
        self.profile = self._validate_profile(profile)
        self.crt_response_properties = self._sanitize_crt_response_properties(crt_response_properties)

    def prepare_entitled_response(self, validity, subscriber_uid, device_uid=None, content_uid=None, message=None,
                                  http_code=200):
        res = {'accountingId': f'{content_uid}-{subscriber_uid}',
               'assetId': content_uid,
               'profile': {},
               'message': 'granted'
               }

        if self.profile == 'purchase':
            res['profile'] = {'purchase': {}}
        if self.profile == 'rental':
            play_duration = int((validity - dt.now(tz=pytz.UTC)).total_seconds() * 1000)
            res['profile'] = {'rental': {
                'absoluteExpiration': f'{validity.isoformat()}',
                'playDuration': play_duration}
            }

        if self.crt_response_properties:
            res.update(self.crt_response_properties)

        return res, http_code

    def prepare_not_entitled_response(self, message=None, http_code=200):
        res = {'redirectUrl': self.redirect_url,
               'message': 'not_granted'}

        return res, http_code

    def parse_request_data(self, data):
        try:
            return {'subscriber_uid': data['user'],
                    'device_uid': data['client'],
                    'content_uid': data['asset']}
        except Exception:
            self.logger.error(f'Unable to parse request data from: {data}.')
            raise DrmAdapterError('Unable to parse request data', 105)

    def _validate_profile(self, profile):
        if profile not in self._supported_profiles:
            self.logger.error(f'Unsupported DRM profile "{profile}". Suported: {self._supported_profiles}')
            raise DrmAdapterError(f'Unsupported DRM profile "{profile}". Supported :{self._supported_profiles}.', 200)

        return profile

    def _sanitize_crt_response_properties(self, crt_response_properties):
        for key in ['accountingId', 'assetId', 'profile', 'message']:
            removed_key = crt_response_properties.pop(key, None)
            if removed_key:
                self.logger.warning(f'Removing violating configuration key "{removed_key}" found in '
                                    f'drm_adapter_options.crt_response_properties.')

        return crt_response_properties
