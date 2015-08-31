"""birding uses a validated configuration file for runtime details.

Configuration files use a `YAML <http://yaml.org/>`_ format. All values have a
default (below) and accept values of the same name in the configuration file,
which has a default path of ``birding.yml`` in the current working
directory. If needed, the ``BIRDING_CONF`` environment variable can point to
the filepath of the configuration file.

The scope of the configuration file is limited to details of birding itself,
not of Storm-related topics. Storm details are in the project topology
definition.

When a configuration value is a Python dotted name, it is a string reference to
the Python object to import. In general, when the value is just an object name
without a full namespace, its assumed to be the relevant birding namespace,
e.g. ``LRUShelf`` is assumed to be ``birding.shelf.LRUShelf``. Respective
``*_init`` configuration values specify keyword (not positional) arguments to
be passed to the class constructor.

See :ref:`production` for further discussion on configuration in production
environments.

For advanced API usage, see :func:`get_config`. The config includes an
`Appendix` to support any additional values not known to birding, such that
these values are available in ``config['Appendix']`` and bypass any
validation. This is useful for code which uses birding's config loader and
needs to define additional values.

Defaults::

    spout: TermCycleSpout
    TermCycleSpout:
      terms:
      - real-time analytics
      - apache storm
      - pypi
    TwitterSearchBolt:
      shelf_class: LRUShelf
      shelf_init: {}
    ElasticsearchIndexBolt:
      elasticsearch_class: elasticsearch.Elasticsearch
      elasticsearch_init:
        hosts:
        - localhost: 9200
      index: tweet
      doc_type: tweet
    ResultTopicBolt:
      kafka_class: pykafka.KafkaClient
      kafka_init:
        hosts: 127.0.0.1:9092 # comma-separated list of hosts
      topic: tweet
    Appendix: {}

"""

import importlib
import logging
import os
import textwrap
from collections import Mapping
from io import StringIO

import travesty as tv
import yaml
from repoze.lru import LRUCache


BIRDING_CONF_DEFAULT = 'birding.yml'
BIRDING_CONF = os.environ.get('BIRDING_CONF', BIRDING_CONF_DEFAULT)


SCHEMA = tv.SchemaMapping().of(
    spout = tv.String(),
    TermCycleSpout = tv.SchemaMapping().of(
        terms = tv.List().of(tv.String())),
    TwitterSearchBolt = tv.SchemaMapping().of(
        shelf_class = tv.String(),
        shelf_init = tv.StrMapping().of(tv.Passthrough())),
    ElasticsearchIndexBolt = tv.SchemaMapping().of(
        elasticsearch_class = tv.String(),
        elasticsearch_init = tv.StrMapping().of(tv.Passthrough()),
        index = tv.String(),
        doc_type = tv.String()),
    ResultTopicBolt = tv.SchemaMapping().of(
        kafka_class = tv.String(),
        kafka_init = tv.StrMapping().of(tv.Passthrough()),
        topic = tv.String()),
    Appendix = tv.Passthrough())


CACHE = LRUCache(16) # size


def get_config(filepath=None, default_loader=None, on_missing=None):
    """Get a dict for the current birding configuration.

    The resulting dictionary is fully populated with defaults, such that all
    valid keys will resolve to valid values. Invalid and extra values in the
    configuration result in an exception.

    See :ref:`config` (module-level docstring) for discussion on how birding
    configuration works, including filepath loading. Note that a non-default
    filepath set via env results in a :py:exc:`OSError` when the file is
    missing, but the default filepath is ignored when missing.

    This function caches its return values as to only parse configuration once
    per set of inputs. As such, treat the resulting dictionary as read-only as
    not to accidentally write values which will be seen by other handles of the
    dictionary.

    Args:
        filepath (str): path to birding configuration YAML file.
        default_loader (callable):
            callable which returns file descriptor with YAML data of default
            configuration values
        on_missing (callable): callback to call when file is missing.
    Returns:
        dict: dict of current birding configuration; treat as read-only.

    """
    # Handle cache lookup explicitly in order to support keyword arguments.
    cache_key = (filepath, default_loader, on_missing)
    if CACHE.get(cache_key) is not None:
        return CACHE.get(cache_key)

    logger = logging.getLogger('birding')

    if filepath is None:
        filepath = BIRDING_CONF
    if default_loader is None:
        default_loader = get_defaults_file
    if on_missing is None:
        on_missing = logger.info

    logger.info(
        'Looking for configuration file: {}'.format(os.path.abspath(filepath)))
    if not os.path.exists(filepath):
        # Log a message if filepath is default; raise error if not default.
        on_missing('No {} configuration file found.'.format(filepath))
        if filepath != BIRDING_CONF_DEFAULT:
            # Stat the missing file to result in OSError.
            os.stat(filepath)

    config = yaml.safe_load(default_loader())
    tv.validate(SCHEMA, config)
    if os.path.exists(filepath):
        file_config = yaml.safe_load(open(filepath))
        if file_config:
            config = overlay(file_config, config)
            tv.validate(SCHEMA, config)

    CACHE.put(cache_key, config)

    return config


def get_defaults_file(*a, **kw):
    """Get a file object with YAML data of configuration defaults.

    Arguments are passed through to :func:`get_defaults_str`.
    """
    fd = StringIO()
    fd.write(get_defaults_str(*a, **kw))
    fd.seek(0)
    return fd


def get_defaults_str(raw=None, after='Defaults::'):
    """Get the string YAML representation of configuration defaults."""
    if raw is None:
        raw = __doc__
    return unicode(textwrap.dedent(raw.split(after)[-1]).strip())


def overlay(upper, lower):
    """Return the overlay of `upper` dict onto `lower` dict.

    This operation is similar to `dict.update`, but recurses when it encounters
    a dict/mapping, as to allow nested leaf values in the lower collection
    which are not in the upper collection. Whenever the upper collection has a
    value, its value is used.

    >>> overlay({'a': 0}, {})
    {'a': 0}
    >>> abc = {'a': 0, 'b': 1, 'c': 2}
    >>> abc == overlay({'a': 0, 'c': 2}, {'a': None, 'b': 1})
    True
    >>> result = {' ': None, '_': abc}
    >>> result == overlay(
    ...   {'_': {'a': 0, 'c': 2}, ' ': None},
    ...   {'_': {'a': None, 'b': 1}})
    ...
    True
    >>>
    """
    result = {}
    for key in upper:
        if is_mapping(upper[key]):
            lower_value = lower.get(key, {})
            if not is_mapping(lower_value):
                msg = 'Attempting to overlay a mapping on a non-mapping: {}'
                raise ValueError(msg.format(key))
            result[key] = overlay(upper[key], lower_value)
        else:
            result[key] = upper[key]
    for key in lower:
        if key in result:
            continue
        result[key] = lower[key]
    return result


def is_mapping(x):
    return isinstance(x, Mapping) or isinstance(x, dict)


def import_name(name, default_ns=None):
    """Import an object based on the dotted string.

    >>> import_name('textwrap') # doctest: +ELLIPSIS
    <module 'textwrap' from '...'>
    >>> import_name('birding.config') # doctest: +ELLIPSIS
    <module 'birding.config' from '...'>
    >>> import_name('birding.config.get_config') # doctest: +ELLIPSIS
    <function get_config at ...>
    >>>

    If `ns` is provided, use it as the namespace if `name` does not have a dot.

    >>> ns = 'birding.config'
    >>> x = import_name('birding.config.get_config')
    >>> x # doctest: +ELLIPSIS
    <function get_config at ...>
    >>> x == import_name('get_config', default_ns=ns)
    True
    >>> x == import_name('birding.config.get_config', default_ns=ns)
    True
    >>>
    """
    if '.' not in name:
        if default_ns is None:
            return importlib.import_module(name)
        else:
            name = default_ns + '.' + name
    module_name, object_name = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, object_name)


if __name__ == '__main__':
    import doctest
    import pprint

    doctest.testmod()
    pprint.pprint(get_config())
