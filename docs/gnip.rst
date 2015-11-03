.. _gnip:

Searching Gnip
==============

`Gnip <https://gnip.com/>`_ is Twitter's enterprise API platform, which birding
supports for projects seeking to search at higher rates than allowed in the
public API. The configuration snippet below uses Gnip's APIs instead of
Twitter. See :ref:`config` for how to configure birding.

.. code-block:: yaml

    SearchManager:
      class: birding.gnip.GnipSearchManager
      init:
        base_url: https://search.gnip.com/accounts/Example
        stream: prod.json
        username: admin@example.org
        password: This.yml.file.should.be.untracked.

See birding API docs for :class:`~birding.gnip.Gnip` and
:class:`~birding.gnip.GnipSearchManager` for underlying behavior, which is
minimal.
