"""Minimal twitter API shim using http://mike.verdone.ca/twitter/."""

from __future__ import absolute_import

import os
import textwrap

from twitter.api import Twitter as BaseTwitter
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET
from twitter.oauth import OAuth, read_token_file

from .search import SearchManager


class Twitter(BaseTwitter):
    @classmethod
    def from_oauth_file(cls, filepath=None):
        """Get an object bound to the Twitter API using your own credentials.

        The `twitter` library ships with a `twitter` command that uses PIN
        OAuth. Generate your own OAuth credentials by running `twitter` from
        the shell, which will open a browser window to authenticate you. Once
        successfully run, even just one time, you will have a credential file
        at ~/.twitter_oauth.

        This factory function reuses your credential file to get a `Twitter`
        object. (Really, this code is just lifted from the `twitter.cmdline`
        module to minimize OAuth dancing.)
        """
        if filepath is None:
            # Use default OAuth filepath from `twitter` command-line program.
            home = os.environ.get('HOME', os.environ.get('USERPROFILE', ''))
            filepath = os.path.join(home, '.twitter_oauth')

        oauth_token, oauth_token_secret = read_token_file(filepath)

        twitter = cls(
            auth=OAuth(
                oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
            api_version='1.1',
            domain='api.twitter.com')

        return twitter


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

    Arguments are passed to :meth:`birding.twitter.Twitter.from_oauth_file`.
    """
    return TwitterSearchManager(Twitter.from_oauth_file(*a, **kw))


def main():
    """Do the default action of `twitter` command."""
    from twitter.cmdline import Action, OPTIONS
    twitter = Twitter.from_oauth_file()
    Action()(twitter, OPTIONS)


if __name__ == '__main__':
    main()
