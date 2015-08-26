.. _solo:

Downloading and running `birding`
=================================

.. note::

   Existing streamparse projects should include the `birding Python package
   <https://pypi.python.org/pypi/birding>`_ instead of cloning the birding
   repository, which is described in :ref:`production`.

The birding project fully automates dependencies for the purposes of
development, demo, or light usage. In a terminal on a Unix-like system, clone
the birding repository::

    git clone https://github.com/Parsely/birding.git
    cd birding

Then run::

    make run

The birding project makes every effort to detect if an underlying dependency is
unmet. If ``make run`` fails, look for messages indicating what is missing or
what went wrong. If an error is unclear, `submit an issue
<https://github.com/Parsely/birding/issues>`_ including a build log and mention
your operating system. To create a `build.log`::

    make run 2>&1 | tee build.log

When birding is running, its console output is verbose as it includes all
output of zookeeper, kafka, storm, and streamparse. Note that -- as with all
streamparse projects -- output from the birding code itself ends up in the
``logs/`` directory and not in the console. To stop running `birding`, issue a
keyboard interrupt in the console with Control-C::

    Control-C

Next, goto one of:

* :ref:`tour`
* :ref:`production`
* :ref:`config`
