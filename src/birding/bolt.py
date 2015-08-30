from __future__ import absolute_import, print_function

import json

from pykafka import KafkaClient
from streamparse.bolt import Bolt

from .config import get_config
from .search import SearchManager
from .shelf import LRUShelf
from .twitter_api import Twitter


class TwitterSearchBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare :class:`~birding.twitter_api.Twitter` object w/OAuth file.
        2. Prepare to track searched terms as to avoid redundant searches.
        """
        self.manager = SearchManager(Twitter.from_oauth_file())
        self.term_shelf = LRUShelf()

    def process(self, tup):
        """Process steps:

        1. Stream in (term, timestamp).
        2. Perform :meth:`~birding.search.SearchManager.search` on term.
        3. Emit (term, timestamp, search_result).
        """
        term, timestamp = tup.values
        if term not in self.term_shelf:
            self.log(
                'search: {term}, {timestamp}'
                .format(term=term, timestamp=timestamp))
            search_result = self.manager.search(q=term)
            self.emit([term, timestamp, search_result])
            self.term_shelf[term] = timestamp


class TwitterLookupBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare :class:`~birding.twitter_api.Twitter` object w/OAuth file.
        """
        self.manager = SearchManager(Twitter.from_oauth_file())

    def process(self, tup):
        """Process steps:

        1. Stream in (term, timestamp, search_result).
        2. Perform :meth:`~birding.search.SearchManager.lookup_search_result`.
        3. Emit (term, timestamp, lookup_result).
        """
        term, timestamp, search_result = tup.values
        self.log(
            'lookup: {term}, {timestamp}'
            .format(term=term, timestamp=timestamp))
        lookup_result = self.manager.lookup_search_result(search_result)
        self.emit([term, timestamp, lookup_result])


class ResultTopicBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Connect to Kafka.
        2. Prepare Kafka producer for `tweet` topic.
        """
        config = get_config()['ResultTopicBolt']
        self.client = KafkaClient(hosts=config['hosts'])
        self.topic = self.client.topics[config['topic']]
        self.producer = self.topic.get_producer()

    def process(self, tup):
        """Process steps:

        1. Stream third positional value from input into Kafka topic.
        """
        # This could be more efficient by passing the result from twitter
        # straight through to the producer, instead of deserializing and
        # reserializing json.
        self.producer.produce(json.dumps(status) for status in tup.values[2])
