from __future__ import absolute_import, print_function

import datetime
import itertools

from streamparse.spout import Spout


class SimpleSimulationSpout(Spout):
    terms = [
        'real-time analytics',
        'apache storm',
        'pypi',
    ]

    def initialize(self, stormconf, context):
        self.term_seq = itertools.cycle(self.terms)

    def next_tuple(self):
        term = next(self.term_seq)
        timestamp = datetime.datetime.now().isoformat()
        self.emit([term, timestamp])
