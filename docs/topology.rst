.. _topology:

Problem statement & topology
============================

Problem Statement
-----------------

Take as input a sequence of terms and timestamps and produce a "filtered
firehose" of twitter_ activity using only `twitter's public APIs`_, without
requiring special API access to twitter or any third party.


Specifics
---------

* Input is in the format of (term, timestamp), where `term` is any string and
  `timestamp` is a date/time value in an ISO 8601 format,
  e.g. ``2015-06-25T08:00Z``.
* The motivating use-case:

  * provides this input as a Kafka_ topic
  * prefers output be sent to a Kafka topic & include full twitter API results
  * prefers the solution be implemented in Python_


Observations
------------

Twitter provides `GET search/tweets`_ to get relevant Tweets_ (status updates)
matching a specified query. Any detail not provided in the search results can
be accessed with `GET statuses/lookup`_, looking up multiple status updates in
a batched request.

The problem has potentially unbounded streams of data, which makes Storm_ a
relevant technology for the solution. Given that the motivating use-case
prefers Python with Kafka I/O, streamparse_ and pykafka_ are relavant.

Topology
--------

Given the problem statement, a streaming solution looks something like:

.. Anyone with the link should be able to access / fork this drawing.
.. image:: birding-topology-sketch.svg
   :target: https://docs.google.com/drawings/d/1dijNLPjn_96Q2VyPaiGYUfrnO6jXA0sBcIEKcnNERjE/edit


Other Goals
-----------

The solution should:

* Encode best practices about how to use Storm_/streamparse_ and
  Kafka_/pykafka_.
* Be fully public & open source to serve as an example project, so it should
  not depend on anything specific to a specific company/organization. Depending
  on the publicly scrutable Twitter API is, of course, okay.
* Include basic command-line tools for testing the topology with data and ways
  to configure things like Twitter authentication credentials.

Next, goto one of:

* :ref:`solo`
* :ref:`tour`

.. _twitter: https://twitter.com
.. _`twitter's public APIs`: https://dev.twitter.com/rest/public
.. _Kafka: http://kafka.apache.org
.. _Python: http://python.org
.. _`GET search/tweets`:
   https://dev.twitter.com/rest/reference/get/search/tweets
.. _`Tweets`: https://dev.twitter.com/overview/api/tweets
.. _`GET statuses/lookup`:
   https://dev.twitter.com/rest/reference/get/statuses/lookup
.. _Storm: http://storm.apache.org
.. _streamparse: https://github.com/Parsely/streamparse
.. _pykafka: https://github.com/Parsely/pykafka
