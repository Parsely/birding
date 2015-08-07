from __future__ import absolute_import, print_function

import datetime
import itertools

from streamparse.spout import Spout


class SimpleSimulationSpout(Spout):
    urls = [
        'http://www.parsely.com/',
        'http://streamparse.readthedocs.org/',
        'https://pypi.python.org/pypi/streamparse',
    ]

    def initialize(self, stormconf, context):
        self.url_seq = itertools.cycle(self.urls)

    def next_tuple(self):
        url = next(self.url_seq)
        timestamp = datetime.datetime.now().isoformat()
        self.emit([url, timestamp])
