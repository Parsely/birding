.. _tour:

A tour of `birding`'s implementation
====================================

Python Twitter Client
---------------------

There are many `Python packages for Twitter`__. The `Python Twitter Tools`_
project (``pip install twitter``) is of interest because:

1. It has a command-line application to get twitter_ activity which includes a
   straightforward authentication workflow to log into twitter and get OAuth_
   credentials, using a PIN-Based_ workflow.
2. It provides APIs in Python which bind to `twitter's public APIs`_ in a
   dynamic and predictable way, where Python attribute and method names
   translate to URL paths, e.g. ``twitter.statuses.friends_timeline()``
   retrieves data from ``http://twitter.com/statuses/friends_timeline.json``.
3. The OAuth credentials saved by the command-line tool can be readily used
   when making API calls using the package.

__ https://pypi.python.org/pypi?%3Aaction=search&term=twitter&submit=search


Twitter API
-----------

To ease configuration, birding adds a
:meth:`~birding.twitter_api.Twitter.from_oauth_file` method which will creates
a `Twitter` binding using the OAuth credential file created by the ``twitter``
command-line application. The ``twitter`` command need only be run once to
create this file, which is saved in the user home directory at
``~/.twitter_oauth``. Once that file is in place, twitter API interactions look
like this:

* `Twitter API Demo <https://github.com/Parsely/birding/blob/master/docs/Twitter%20API%20Demo.ipynb>`_


Search Manager
--------------

It is useful to solve the problem itself before being concerned with details
about the topology. birding's :class:`~birding.search.SearchManager` composes
the `Twitter` object into higher-level method signatures which perform the
processing steps needed for the given :ref:`topology`. A full interaction
before applying Storm looks like this (see ``In[2]``):

* `Simple Simulated Stream <https://github.com/Parsely/birding/blob/master/docs/Simple%20Simulated%20Stream.ipynb>`_


Storm Bolts
-----------

With APIs in place to do the work, Bolt_ classes provide Storm components:

* :class:`~birding.bolt.TwitterSearchBolt` searches the input terms.
* :class:`~birding.bolt.TwitterLookupBolt` expands search results into full tweets.
* :class:`~birding.bolt.ResultTopicBolt` publishes the lookup results to Kafka.


Storm Spouts
------------

Spout_ classes provide Storm components which take birding's input and provide
the source of streams in the topology:

* :class:`~birding.spout.TermCycleSpout` cycles through a static list of terms.


Storm Topology
--------------

With Storm components ready for streamparse, a topology can pull it all
together. birding's topology uses the `Clojure DSL`_; the `streamparse
discussion of topologies`_ has more detail. In the topology definition below,
note the class references ``"birding.bolt.TwitterSearchBolt"``,
``"birding.bolt.TwitterLookupBolt"``, and
``"birding.bolt.ResultTopicBolt"``. These are full Python namespace references
to the birding classes. The names given in the DSL can then be used to wire the
components together. For example, the definition of ``"search-bolt"
(python-bolt-spec ...)`` allows ``"search-bolt"`` to be used as input in
another bolt, ``"lookup-bolt" (python-bolt-spec ... {"search-bolt" :shuffle}
... )``.

.. literalinclude:: ../topologies/birding.clj
   :language: clojure

Next, goto one of:

* :ref:`solo`
* :ref:`production`
* :ref:`config`

.. _`Python Twitter Tools`: http://mike.verdone.ca/twitter/
.. _twitter: https://twitter.com
.. _OAuth: https://dev.twitter.com/oauth
.. _PIN-Based: https://dev.twitter.com/oauth/pin-based
.. _`twitter's public APIs`: https://dev.twitter.com/rest/public
.. _Bolt: https://storm.apache.org/documentation/Concepts.html#bolts
.. _Spout: https://storm.apache.org/documentation/Concepts.html#spouts
.. _`Clojure DSL`: http://storm.apache.org/documentation/Clojure-DSL.html
.. _`streamparse discussion of topologies`:
   http://streamparse.readthedocs.org/en/master/topologies.html
