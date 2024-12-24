from .adapters import CastlabsAdapter
from .adapters import DrmAdapterError

_adapters = {
    'castlabs': CastlabsAdapter
}

def get_available_adapters():
    return _adapters

def get_adapter(adapter):
    available = get_available_adapters()
    if adapter not in available.keys():
        raise DrmAdapterError(f'Unsupported adapter {adapter}. Supported are {set(available.keys())}', 100)
    else:
        return available[adapter]
