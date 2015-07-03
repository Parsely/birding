"""Search twitter. Get tweets."""

from __future__ import print_function, unicode_literals

import textwrap


class SearchManager(object):
    """Service object to provide fully-hydrated tweets given a search query."""

    def __init__(self, twitter):
        self.twitter = twitter

    def search(self, q=None, **kw):
        if q is None:
            raise ValueError('No search query provided for `q` keyword.')
        return self.twitter.search.tweets(q=q, **kw)

    def lookup_search_result(self, result, **kw):
        return self.lookup(s['id_str'] for s in result['statuses'], **kw)

    def lookup(self, id_list, **kw):
        result_id_pack = ','.join([str(_id) for _id in id_list])
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
        return '\n\n'.join(status_str_list)
