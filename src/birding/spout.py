"""Storm Spout classes."""

import datetime
import itertools

from streamparse.spout import Spout

from .config import get_config


class TermCycleSpout(Spout):
    def initialize(self, stormconf, context):
        """Initialization steps:

        1. Prepare sequence of terms based on config: TermCycleSpout/terms.
        """
        self.terms = get_config()['TermCycleSpout']['terms']
        self.term_seq = itertools.cycle(self.terms)

    def next_tuple(self):
        """Next tuple steps:

        1. Emit (term, timestamp) for next term in sequence w/current UTC time.
        """
        term = next(self.term_seq)
        timestamp = datetime.datetime.utcnow().isoformat()
        self.emit([term, timestamp])
