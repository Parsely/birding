"""Storm Bolt classes."""

import json

from streamparse.bolt import Bolt

from .config import get_config, import_name
from .search import SearchManager
from .twitter_api import Twitter


class TwitterSearchBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare :class:`~birding.twitter_api.Twitter` object w/OAuth file.
        2. Prepare to track searched terms as to avoid redundant searches.
        """
        self.manager = SearchManager(Twitter.from_oauth_file())
        config = get_config()['TwitterSearchBolt']
        shelf_class = import_name(
            config['shelf_class'], default_ns='birding.shelf')
        self.term_shelf = shelf_class(**config['shelf_init'])

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


class ElasticsearchIndexBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Prepare elasticsearch connection, including details for indexing.
        """
        config = get_config()['ElasticsearchIndexBolt']
        elasticsearch_class = import_name(config['elasticsearch_class'])
        self.es = elasticsearch_class(**config['elasticsearch_init'])
        self.index = config['index']
        self.doc_type = config['doc_type']

    def process(self, tup):
        """Process steps:

        1. Index third positional value from input to elasticsearch.
        """
        self.es.bulk(
            self.generate_bulk_body(tup.values[2]),
            index=self.index,
            doc_type=self.doc_type)

    @staticmethod
    def generate_bulk_body(statuses):
        for status in statuses:
            yield {'index': {'_id': status['id_str']}}
            yield status


class ResultTopicBolt(Bolt):
    def initialize(self, conf, ctx):
        """Initialization steps:

        1. Connect to Kafka.
        2. Prepare Kafka producer for `tweet` topic.
        3. Prepare to track tweets published to topic, to avoid redundant data.
        """
        config = get_config()['ResultTopicBolt']
        kafka_class = import_name(config['kafka_class'])
        self.client = kafka_class(**config['kafka_init'])
        self.topic = self.client.topics[config['topic']]
        self.producer = self.topic.get_producer()

        shelf_class = import_name(
            config['shelf_class'], default_ns='birding.shelf')
        shelf_init = config['shelf_init']

        # Use own default index value while still allowing user config.
        shelf_init['index'] = shelf_init.get('index', 'pre_kafka_shelf')
        self.tweet_shelf = shelf_class(**shelf_init)

    def process(self, tup):
        """Process steps:

        1. Stream third positional value from input into Kafka topic.
        """
        status_seq = self.iter_using_shelf(tup.values[2], self.tweet_shelf)
        # This could be more efficient by passing the result from twitter
        # straight through to the producer, instead of deserializing and
        # reserializing json.
        self.producer.produce(json.dumps(status) for status in status_seq)

    @staticmethod
    def iter_using_shelf(statuses, shelf):
        for status in statuses:
            id_str = status['id_str']
            if id_str in shelf:
                continue
            yield status
            shelf[id_str] = None
