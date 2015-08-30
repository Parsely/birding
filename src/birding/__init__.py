from __future__ import absolute_import, print_function

import logging

from . import bolt, config, follow, search, spout, twitter_api
from .version import VERSION, __version__
from .version import __doc__ as __license__


__all__ = [
    'VERSION',
    '__license__',
    '__version__',
    'bolt',
    'config',
    'follow',
    'search',
    'spout',
    'twitter_api',
]


# Configure the logger. No configuration is exposed by birding itself. A
# project using birding can change the log level after importing `birding`
# with:
#
#     logging.getLogger('birding').setLevel(logging.DEBUG)
#
logger = logging.getLogger('birding')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)
