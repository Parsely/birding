"""Storm Spout classes."""

import datetime
import itertools

from streamparse.spout import Spout

from .config import get_config, import_name


def DispatchSpout(*a, **kw):
    """Factory to dispatch spout class based on config."""
    spout_class_name = get_config()['Spout']
    spout_class = import_name(spout_class_name, default_ns='birding.spout')
    return spout_class(*a, **kw)


class TermMethods(object):
    @staticmethod
    def pack_tup_id(term, timestamp):
        """Pack term, timestamp into a tuple ID suitable for Storm.

        Example:

        >>> TermMethods.pack_tup_id('search it!', '2015-09-24T14:39:53.429183')
        'search it! 2015-09-24T14:39:53.429183'
        >>>
        """
        return '{} {}'.format(term, timestamp)

    @staticmethod
    def parse_tup_id(tup_id):
        """Parse a `pack_tup_id`-packed tuple ID into term, timestamp.

        Example:

        >>> TermMethods.parse_tup_id('search it! 2015-09-24T14:39:53.429183')
        ('search it!', '2015-09-24T14:39:53.429183')
        >>>
        """
        return tuple(tup_id.rsplit(' ', 1))


class TermCycleSpout(Spout, TermMethods):
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
        self.emit([term, timestamp], tup_id=self.pack_tup_id(term, timestamp))
