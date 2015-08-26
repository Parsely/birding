birding: public API twitter search stream
=========================================

**WORK IN PROGRESS**

Overview
--------

`birding` is an open source project to produce a stream of recent twitter_
activity based on a sequence of search terms, using only `twitter's public
APIs`_. It serves as both a standalone project and a demo of distributed
real-time computing with Python_ using Storm_/streamparse_ and Kafka_/pykafka_.

Dependencies are fully automated; run with::

    make run

See the docs (below) for discussion on how to use birding in an existing
streamparse project.

To discuss this project, join the `streamparse user group`_.

.. _twitter: https://twitter.com
.. _`twitter's public APIs`: https://api.twitter.com
.. _Storm: http://storm.apache.org
.. _Python: http://python.org
.. _Kafka: http://kafka.apache.org
.. _streamparse: https://github.com/Parsely/streamparse
.. _pykafka: https://github.com/Parsely/pykafka
.. _`streamparse user group`: https://github.com/Parsely/streamparse#user-group


Documentation
-------------

* `HEAD <http://birding.readthedocs.org/en/master/>`_
* `Stable <http://birding.readthedocs.org/en/stable/>`_


Python Support
--------------

The birding project uses Python 2.7 and will also support Python 3.4+ when
underlying dependencies support Python 3.
