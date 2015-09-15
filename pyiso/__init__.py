import imp
import os.path
from os import environ
from logging import DEBUG, INFO

#########################################
# For Testing Purposes
# Add caching to unittesting
# Print every time the testing hits the cache successfully
import requests
import requests_cache
requests_cache.install_cache(expire_after=60*10)

__version__ = '0.2.11'

log_dict = {'True': DEBUG, False: INFO}
LOG_LEVEL = log_dict[environ.get('DEBUG', False)]

BALANCING_AUTHORITIES = {
    'AZPS': {'module': 'sveri', 'class': 'SVERIClient'},
    'BPA': {'module': 'bpa', 'class': 'BPAClient'},
    'CAISO': {'module': 'caiso', 'class': 'CAISOClient'},
    'DEAA': {'module': 'sveri', 'class': 'SVERIClient'},
    'ELE': {'module': 'sveri', 'class': 'SVERIClient'},
    'ERCOT': {'module': 'ercot', 'class': 'ERCOTClient'},
    'HGMA': {'module': 'sveri', 'class': 'SVERIClient'},
    'IID': {'module': 'sveri', 'class': 'SVERIClient'},
    'ISONE': {'module': 'isone', 'class': 'ISONEClient'},
    'GRIF': {'module': 'sveri', 'class': 'SVERIClient'},
    'MISO': {'module': 'miso', 'class': 'MISOClient'},
    'NEVP': {'module': 'nvenergy', 'class': 'NVEnergyClient'},
    'NYISO': {'module': 'nyiso', 'class': 'NYISOClient'},
    'PJM': {'module': 'pjm', 'class': 'PJMClient'},
    'PNM': {'module': 'sveri', 'class': 'SVERIClient'},
    'SPPC': {'module': 'nvenergy', 'class': 'NVEnergyClient'},
    'SPP': {'module': 'spp', 'class': 'SPPClient'},
    'SRP': {'module': 'sveri', 'class': 'SVERIClient'},
    'TEPC': {'module': 'sveri', 'class': 'SVERIClient'},
    'WALC': {'module': 'sveri', 'class': 'SVERIClient'},
    'EU': {'module': 'eu', 'class': 'EUClient'},
}


def client_factory(client_name, **kwargs):
    """Return a client for an external data set"""
    # set up
    dir_name = os.path.dirname(os.path.abspath(__file__))
    error_msg = 'No client found for name %s' % client_name
    client_key = client_name.upper()

    # find client
    try:
        client_vals = BALANCING_AUTHORITIES[client_key]
        module_name = client_vals['module']

        class_name = client_vals['class']
    except KeyError:
        raise ValueError(error_msg)

    # find module
    try:
        fp, pathname, description = imp.find_module(module_name, [dir_name])
    except ImportError:
        raise ValueError(error_msg)

    # load
    try:
        mod = imp.load_module(module_name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

    # instantiate class
    try:
        client_inst = getattr(mod, class_name)(**kwargs)
    except AttributeError:
        raise ValueError(error_msg)

    # set name
    client_inst.NAME = client_name

    return client_inst
