"""Tool to follow output of birding."""

from __future__ import print_function

import json
import sys
from contextlib import contextmanager
from time import sleep

from pykafka import KafkaClient
from pykafka.exceptions import KafkaException

from .config import get_config
from .search import SearchManager


def follow_topic_from_config():
    """Read kafka config, then dispatch to `follow_topic`."""
    config = get_config()['ResultTopicBolt']
    return follow_topic(config['hosts'], config['topic'])


def follow_topic(hosts, name, retry_interval=1):
    """Dump each message from kafka topic to stdio."""
    while True:
        try:
            client = KafkaClient(hosts=hosts)
            topic = client.topics[name]
            consumer = topic.get_simple_consumer(reset_offset_on_start=True)
        except Exception as e:
            if not should_try_kafka_again(e):
                raise
            with flushing(sys.stderr):
                print(
                    'Failed attempt to connect to Kafka. Will retry ...',
                    file=sys.stderr)
            sleep(retry_interval)
        else:
            with flushing(sys.stdout):
                print('Connected to Kafka.')
            break

    for message in consumer:
        with flushing(sys.stdout, sys.stderr):
            status = load(message.value)
            if status:
                dump(status)


def follow_fd(fd):
    """Dump each line of input to stdio."""
    for line in fd:
        if not line.strip():
            continue

        with flushing(sys.stdout, sys.stderr):
            status = load(line)
            if status:
                dump(status)


def load(message):
    try:
        return json.loads(message)
    except Exception as e:
        print(str(e), file=sys.stderr)


def dump(*statuses):
    try:
        print(SearchManager.dump(statuses))
        print('')
    except UnicodeEncodeError as e:
        print(str(e), file=sys.stderr)


@contextmanager
def flushing(*fds):
    yield
    for fd in fds:
        fd.flush()


def should_try_kafka_again(error):
    """Determine if the error means to retry or fail, True to retry."""
    msg = 'Unable to retrieve'
    return isinstance(error, KafkaException) and str(error).startswith(msg)


if __name__ == '__main__':
    follow_topic_from_config()
