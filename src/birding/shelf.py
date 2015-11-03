"""Track terms using a simple dict-like interface."""

import abc
import collections
import time

import elasticsearch
from repoze.lru import LRUCache

from .config import import_name


UNSET = object()


def shelf_from_config(config, **default_init):
    """Get a `Shelf` instance dynamically based on config.

    `config` is a dictionary containing ``shelf_*`` keys as defined in
    :mod:`birding.config`.
    """
    shelf_cls = import_name(config['shelf_class'], default_ns='birding.shelf')
    init = {}
    init.update(default_init)
    init.update(config['shelf_init'])
    shelf = shelf_cls(**init)
    if hasattr(shelf, 'set_expiration') and 'shelf_expiration' in config:
        shelf.set_expiration(config['shelf_expiration'])
    return shelf


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

    def unpack(self, key, value):
        """Unpack value from ``getitem``.

        This is useful for `Shelf` implementations which require metadata be
        stored with the shelved values, in which case ``pack`` should implement
        the inverse operation. By default, the value is simply passed through
        without modification. The ``unpack`` implementation is called on
        ``__getitem__`` and therefore can raise `KeyError` if packed metadata
        indicates that a value is invalid.
        """
        return value

    def pack(self, key, value):
        """Pack value given to ``setitem``, inverse of ``unpack``."""
        return value

    def __getitem__(self, key):
        return self.unpack(key, self.getitem(self.__keytransform__(key)))

    def __setitem__(self, key, value):
        self.setitem(self.__keytransform__(key), self.pack(key, value))

    def __delitem__(self, key):
        self.delitem(self.__keytransform__(key))

    def __keytransform__(self, key):
        return key

    def __iter__(self):
        raise NotImplementedError('Shelf instances do not support iteration.')

    def __len__(self):
        raise NotImplementedError('Shelf instances do not support iteration.')


class FreshPacker(object):
    """Mixin for pack/unpack implementation to expire shelf content."""

    #: Values are no longer fresh after this value, in seconds.
    expire_after = 5 * 60

    def unpack(self, key, value):
        """Unpack and return value only if it is fresh."""
        value, freshness = value
        if not self.is_fresh(freshness):
            raise KeyError('{} (stale)'.format(key))
        return value

    def pack(self, key, value):
        """Pack value with metadata on its freshness."""
        return value, self.freshness()

    def set_expiration(self, expire_after):
        """Set a new expiration for freshness of all unpacked values."""
        self.expire_after = expire_after

    def freshness(self):
        """Clock function to use for freshness packing/unpacking."""
        return time.time()

    def is_fresh(self, freshness):
        """Return False if given freshness value has expired, else True."""
        if self.expire_after is None:
            return True
        return self.freshness() - freshness <= self.expire_after


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


class FreshLRUShelf(FreshPacker, LRUShelf):
    """A Least-Recently Used shelf which expires values."""


class ElasticsearchShelf(Shelf):
    """A shelf implemented using an elasticsearch index."""

    def __init__(self, index='shelf', doc_type='shelf', **elasticsearch_init):
        self.es = elasticsearch.Elasticsearch(**elasticsearch_init)
        self.index_client = elasticsearch.client.IndicesClient(self.es)
        self.index = index
        self.doc_type = doc_type

    def getitem(self, key):
        try:
            doc = self.es.get(index=self.index, doc_type=self.doc_type, id=key)
        except elasticsearch.exceptions.NotFoundError:
            raise KeyError(key)

        if not doc:
            raise KeyError(key)

        try:
            value = doc['_source']['value']
        except KeyError:
            raise KeyError('{} (malformed data)'.format(key))

        return value

    def setitem(self, key, value):
        self.es.index(
            index=self.index,
            doc_type=self.doc_type,
            id=key,
            body={'value': value},
            refresh=True)

    def delitem(self, key):
        self.es.delete(index=self.index, doc_type=self.doc_type, id=key)

    def clear(self):
        self.index_client.delete(self.index)


class FreshElasticsearchShelf(FreshPacker, ElasticsearchShelf):
    """An shelf implementation with elasticsearch which expires values."""
