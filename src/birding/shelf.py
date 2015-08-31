"""Track terms using a simple dict-like interface."""

import abc
import collections

from repoze.lru import LRUCache


UNSET = object()


class Shelf(collections.MutableMapping):
    """Abstract base class for a shelf to track -- but not iterate -- values.

    Provides a dict-interface.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getitem(self, key):
        """Get an item's value from the shelf or raise KeyError(key)."""

    @abc.abstractmethod
    def setitem(self, key, value):
        """Set an item on the shelf, with the given value."""

    @abc.abstractmethod
    def delitem(self, key):
        """Remove an item from the shelf."""

    @abc.abstractmethod
    def clear(self):
        """Remove all items from the shelf."""

    def __getitem__(self, key):
        return self.getitem(self.__keytransform__(key))

    def __setitem__(self, key, value):
        self.setitem(self.__keytransform__(key), value)

    def __delitem__(self, key):
        self.delitem(self.__keytransform__(key))

    def __keytransform__(self, key):
        return key

    def __iter__(self):
        raise NotImplementedError('Shelf instances do not support iteration.')

    def __len__(self):
        raise NotImplementedError('Shelf instances do not support iteration.')


class LRUShelf(Shelf):
    """An in-memory Least-Recently Used shelf up to `maxsize`.."""

    def __init__(self, maxsize=1000):
        self.store = LRUCache(int(maxsize))

    def getitem(self, key):
        value = self.store.get(key, UNSET)
        if value is UNSET:
            raise KeyError(key)
        return value

    def setitem(self, key, value):
        self.store.put(key, value)

    def delitem(self, key):
        self.store.invalidate(key)

    def clear(self):
        self.store.clear()
