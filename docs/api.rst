.. _api:

API
===

.. module:: birding.twitter_api

.. autoclass:: Twitter
   :members:


.. module:: birding.search

.. autoclass:: SearchManager
   :members:

.. autoclass:: TwitterSearchManager
   :members:


.. Use ClassName() to remove __init__ function signature from autoclass, as
   component classes are not instantiated directly.

.. module:: birding.spout

.. autofunction:: DispatchSpout()

.. autoclass:: TermCycleSpout()
   :members:


.. module:: birding.bolt

.. autoclass:: TwitterSearchBolt()
   :members:

.. autoclass:: TwitterLookupBolt()
   :members:

.. autoclass:: ElasticsearchIndexBolt()
   :members:

.. autoclass:: ResultTopicBolt()
   :members:


.. autofunction:: birding.config.get_config


.. module:: birding.shelf

.. autoclass:: Shelf
   :members:

.. autoclass:: FreshPacker
   :members:

.. autoclass:: LRUShelf
   :members:

.. autoclass:: FreshLRUShelf
   :members:

.. autoclass:: ElasticsearchShelf
   :members:

.. autoclass:: FreshElasticsearchShelf
   :members:
