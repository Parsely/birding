.. _index:

`birding`: streamparse/kafka demo
=================================

`birding` is an `open source project`__ to produce a stream of recent twitter_
activity based on a sequence of search terms, using only `twitter's public
APIs`_. It serves as both a standalone project and a demo of distributed
real-time computing with Python_ using Storm_/streamparse_ and Kafka_/pykafka_.

__ https://github.com/Parsely/birding

:ref:`topology` describes the problem and how it fits into a topology.
:ref:`solo` describes how to interact with birding for development, demo, or
light usage. :ref:`tour` provides a light introduction to internals.
:ref:`production` discusses how birding is packaged for production use in an
existing streamparse project. :ref:`config` discusses various options for
birding behavior when running locally or in production.

.. toctree::
   :maxdepth: 2

   topology
   solo
   tour
   production
   config
   todo
   api

This project and its documentation are works in progress. See :ref:`todo`.

To discuss this project, join the `streamparse user group`_.

:ref:`Documentation Index <genindex>`

.. _twitter: https://twitter.com
.. _`twitter's public APIs`: https://dev.twitter.com/rest/public
.. _Storm: http://storm.apache.org
.. _Python: http://python.org
.. _Kafka: http://kafka.apache.org
.. _streamparse: https://github.com/Parsely/streamparse
.. _pykafka: https://github.com/Parsely/pykafka
.. _`streamparse user group`: https://github.com/Parsely/streamparse#user-group
