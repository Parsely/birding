"""Namespace of all modules in the birding package."""

import logging

from . import bolt, config, follow, search, shelf, spout, twitter
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
    'shelf',
    'spout',
    'twitter',
]


# Configure the logger. No logger configuration is exposed by birding itself. A
# project using birding can change the log level after importing `birding`
# with:
#
#     logging.getLogger('birding').setLevel(logging.DEBUG)
#
logger = logging.getLogger('birding')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)
