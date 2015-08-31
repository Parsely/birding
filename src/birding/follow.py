"""Tool to follow output of birding."""

from __future__ import print_function

import json
import sys

from .search import SearchManager


def follow_fd(fd):
    """Dump each line of input to stdio."""
    for line in fd:
        try:
            if not line.strip():
                continue

            try:
                status = json.loads(line)
            except Exception as e:
                print(str(e), file=sys.stderr)
                continue

            try:
                print(SearchManager.dump([status]))
            except UnicodeEncodeError as e:
                print(str(e), file=sys.stderr)
                continue

            print('')
        finally:
            sys.stdout.flush()
            sys.stderr.flush()


if __name__ == '__main__':
    follow_fd(sys.stdin)
