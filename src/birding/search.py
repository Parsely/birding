"""Search. Get tweets."""

import textwrap
from abc import ABCMeta, abstractmethod

from .config import import_name
from .twitter_api import Twitter


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


class TwitterSearchManager(SearchManager):
    """Service object to provide fully-hydrated tweets given a search query."""

    def __init__(self, twitter):
        self.twitter = twitter

    def search(self, q=None, **kw):
        """Search twitter for ``q``, return `results`__ directly from twitter.

        __ https://dev.twitter.com/rest/reference/get/search/tweets
        """
        if q is None:
            raise ValueError('No search query provided for `q` keyword.')
        return self.twitter.search.tweets(q=q, **kw)

    def lookup_search_result(self, result, **kw):
        """Perform :meth:`lookup` on return value of :meth:`search`."""
        return self.lookup(s['id_str'] for s in result['statuses'], **kw)

    def lookup(self, id_list, **kw):
        """Lookup list of statuses, return `results`__ directly from twitter.

        Input can be any sequence of numeric or string values representing
        twitter status IDs.

        __ https://dev.twitter.com/rest/reference/get/statuses/lookup
        """
        result_id_pack = ','.join([str(_id) for _id in id_list])
        if not result_id_pack:
            return []
        return self.twitter.statuses.lookup(_id=result_id_pack)

    @staticmethod
    def dump(result):
        """Dump result into a string, useful for debugging."""
        if isinstance(result, dict):
            # Result is a search result.
            statuses = result['statuses']
        else:
            # Result is a lookup result.
            statuses = result
        status_str_list = []
        for status in statuses:
            status_str_list.append(textwrap.dedent(u"""
                @{screen_name} -- https://twitter.com/{screen_name}
                {text}
            """).strip().format(
                screen_name=status['user']['screen_name'],
                text=status['text']))
        return u'\n\n'.join(status_str_list)


def TwitterSearchManagerFromOAuth(*a, **kw):
    """Build :class:`TwitterSearchManager` from user OAuth file.

    Arguments are passed to
    :meth:`birding.twitter_api.Twitter.from_oauth_file`.
    """
    return TwitterSearchManager(Twitter.from_oauth_file(*a, **kw))
