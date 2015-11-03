"""Minimal Gnip API using HTTP requests."""

import textwrap

import requests

from .search import SearchManager


class Gnip(object):
    """Simple binding to Gnip search API."""

    session_class = requests.Session

    default_params = {
        'publisher': 'twitter',
        'maxResults': 500,
    }

    def __init__(self, base_url, stream, username, password, **params):
        """Prepare HTTP session for gnip searches."""
        self.base_url = base_url
        self.stream = stream
        self.username = username
        self.password = password

        self.params = {} # Use on every search.
        self.params.update(self.default_params)
        self.params.update(params)

        self.session = self.start_session()

    def start_session(self):
        session = self.session_class()
        session.auth = (self.username, self.password)
        return session

    def search(self, q, **kw):
        """Search Gnip for given query, returning deserialized response."""
        url = '{base_url}/search/{stream}'.format(**vars(self))

        params = {
            'q': q,
        }
        params.update(self.params)
        params.update(kw)

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


class GnipSearchManager(SearchManager):
    """Service object to provide fully-hydrated tweets given a search query."""

    def __init__(self, *a, **kw):
        self.gnip = Gnip(*a, **kw)

    def search(self, q, **kw):
        """Search gnip for ``q``, return `results`__ directly from gnip.

        __ http://support.gnip.com/apis/search_api/api_reference.html
        """
        return self.gnip.search(q, **kw)

    def lookup_search_result(self, result, **kw):
        """Do almost nothing, just pass-through results."""
        return result['results']

    def lookup(self, id_list, **kw):
        """Not implemented."""
        raise NotImplementedError('gnip does not have have a lookup API.')

    @staticmethod
    def dump(result):
        """Dump result into a string, useful for debugging."""
        if isinstance(result, dict):
            # Result is a search result.
            statuses = result['results']
        else:
            # Result is a lookup result.
            statuses = result
        status_str_list = []
        for status in statuses:
            status_str_list.append(textwrap.dedent(u"""
                @{screen_name} -- https://twitter.com/{screen_name}
                {text}
            """).strip().format(
                screen_name=status['actor']['preferredUsername'],
                text=status['body']))
        return u'\n\n'.join(status_str_list)
