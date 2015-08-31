.. _production:

Using `birding` in production
=============================

.. note:: birding is currently alpha software.

If birding itself satisfies project requirements, see the streamparse project's
discussion of `remote deployment`_ and use ``sparse submit`` from a checkout of
the birding repository. Otherwise, birding is available on the `Python Package
Index <https://pypi.python.org/pypi>`_, which projects can use as a
dependency::

    pip install birding

Once installed in the Python environment, birding references are available to
the topology definition. A project's topology can include
``python-spout-spec`` and ``python-bolt-spec`` declarations which have class
references to ``birding.spout`` and ``birding.bolt`` namespaces, respectively.
The snippet below illustrates this. The :ref:`storm-topology` section has more
detail.

.. code-block:: clojure

    "search-bolt" (python-bolt-spec
        options
        {"term-spout" ["term"]}
        "birding.bolt.TwitterSearchBolt"
        ["term" "timestamp" "search_result"]
        :p 2)

The streamparse project discusses `remote deployment`_ using the ``sparse
submit`` command. :ref:`config` discusses the ``birding.yml`` file which is
located by the ``BIRDING_CONF`` environment variable. Projects using birding
should include its configuration file as part of host configuration management
or a streamparse submit hook, and likewise set the ``BIRDING_CONF`` variable
accordingly.

Next, goto :ref:`config`.

.. _`remote deployment`:
   http://streamparse.readthedocs.org/en/master/quickstart.html#remote-deployment
