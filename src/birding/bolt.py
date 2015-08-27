from __future__ import absolute_import, print_function

import json

from pykafka import KafkaClient
from streamparse.bolt import Bolt

from .search import SearchManager
from .twitter_api import Twitter


class TwitterSearchBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare :class:`~birding.twitter_api.Twitter` object w/OAuth file.
        2. Prepare to track searched URLs as to avoid redundant searches.
        """
        self.manager = SearchManager(Twitter.from_oauth_file())
        self.url_set = set() # This will not scale.

    def process(self, tup):
        """Process steps:

        1. Stream in (url, timestamp).
        2. Perform :meth:`~birding.search.SearchManager.search` on URL.
        3. Emit (url, timestamp, search_result).
        """
        url, timestamp = tup.values
        if url not in self.url_set:
            self.log(
                'search: {url}, {timestamp}'
                .format(url=url, timestamp=timestamp))
            search_result = self.manager.search(q=url)
            self.emit([url, timestamp, search_result])
            self.url_set.add(url)


class TwitterLookupBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare :class:`~birding.twitter_api.Twitter` object w/OAuth file.
        """
        self.manager = SearchManager(Twitter.from_oauth_file())

    def process(self, tup):
        """Process steps:

        1. Stream in (url, timestamp, search_result).
        2. Perform :meth:`~birding.search.SearchManager.lookup_search_result`.
        3. Emit (url, timestamp, lookup_result).
        """
        url, timestamp, search_result = tup.values
        self.log(
            'lookup: {url}, {timestamp}'
            .format(url=url, timestamp=timestamp))
        lookup_result = self.manager.lookup_search_result(search_result)
        self.emit([url, timestamp, lookup_result])


class ResultTopicBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Connect to Kafka.
        2. Prepare Kafka producer for `tweet` topic.
        """
        # TODO: Move specifics into configuration.
        self.client = KafkaClient(hosts='127.0.0.1:9092')
        self.topic = self.client.topics['tweet']
        self.producer = self.topic.get_producer()

    def process(self, tup):
        """Process steps:

        1. Stream third positional value from input into Kafka topic.
        """
        # This could be more efficient by passing the result from twitter
        # straight through to the producer, instead of deserializing and
        # reserializing json.
        self.producer.produce(json.dumps(status) for status in tup.values[2])
