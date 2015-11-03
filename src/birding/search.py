"""Search. Get tweets."""

from abc import ABCMeta, abstractmethod

from .config import import_name


def search_manager_from_config(config, **default_init):
    """Get a `SearchManager` instance dynamically based on config.

    `config` is a dictionary containing ``class`` and ``init`` keys as defined
    in :mod:`birding.config`.
    """
    manager_cls = import_name(config['class'], default_ns='birding.search')
    init = {}
    init.update(default_init)
    init.update(config['init'])
    manager = manager_cls(**init)
    return manager


class SearchManager(object):
    """Abstract base class for service object to search for tweets."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, q=None, **kw):
        """Search for ``q``, return results directly from source."""

    @abstractmethod
    def lookup_search_result(self, result, **kw):
        """Perform :meth:`lookup` on return value of :meth:`search`."""

    @abstractmethod
    def lookup(self, id_list, **kw):
        """Lookup list of statuses, return results directly from source.

        Input can be any sequence of numeric or string values representing
        status IDs.
        """
