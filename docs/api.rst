.. _api:

API
===

.. module:: birding.twitter_api

.. autoclass:: Twitter
   :members:


.. module:: birding.search

.. autoclass:: SearchManager
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

.. autoclass:: ResultTopicBolt()
   :members:


.. autofunction:: birding.config.get_config


.. module:: birding.shelf

.. autoclass:: Shelf
   :members:

.. autoclass:: LRUShelf
   :members:
