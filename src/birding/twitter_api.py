"""Minimal twitter API shim using http://mike.verdone.ca/twitter/."""

import os

from twitter.api import Twitter
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET
from twitter.oauth import OAuth, read_token_file


def build_twitter():
    """Get an object bound to the Twitter API using your own credentials.

    The `twitter` library ships with a `twitter` command that uses PIN
    OAuth. Generate your own OAuth credentials by running `twitter` from the
    shell, which will open a browser window to authenticate you. Once
    successfully run, even just one time, you will have a credential file at
    ~/.twitter_oauth.

    This factory function reuses your credential file to get a `Twitter`
    object. (Really, this code is just lifted from the `twitter.cmdline` module
    to minimize OAuth dancing.)
    """
    oauth_filename = (
        os.environ.get('HOME', os.environ.get('USERPROFILE', ''))
        + os.sep + '.twitter_oauth')
    oauth_token, oauth_token_secret = read_token_file(oauth_filename)

    twitter = Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        api_version='1.1',
        domain='api.twitter.com')

    return twitter


def main():
    """Do the default action of `twitter` command."""
    from twitter.cmdline import Action, OPTIONS
    twitter = build_twitter()
    Action()(twitter, OPTIONS)


if __name__ == '__main__':
    main()
