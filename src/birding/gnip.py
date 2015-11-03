"""Minimal Gnip API using HTTP requests."""

import requests


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
