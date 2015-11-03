.. _api:

API
===

.. module:: birding.search

.. autofunction:: search_manager_from_config()

.. autoclass:: SearchManager
   :members:


.. module:: birding.twitter

.. autoclass:: Twitter
   :members:

.. autoclass:: TwitterSearchManager
   :members:

.. autofunction:: TwitterSearchManagerFromOAuth()


.. module:: birding.gnip

.. autoclass:: Gnip
   :members:

.. autoclass:: GnipSearchManager
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

.. autofunction:: shelf_from_config()

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
