Changelog
=========

..
   All enhancements and patches to Fedinesia will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   The format is trending towards that described at `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
   and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

See the fragment files in the `changelog.d directory`_.

.. _changelog.d directory: https://codeberg.org/MarvinsMastodonTools/lemmy2fedi/src/branch/main/changelog.d


.. scriv-insert-here

.. _changelog-2.0.1:

2.0.1 — 2024-12-24
==================

Changed
-------

- Freshen up CI / nox with more checks.

- Updated dependencies versions

.. _changelog-2.0.0:

2.0.0 — 2024-11-17
==================

Breaking
--------

- Removed functionality to reblog / boost statuses. This can now be done by `fedibooster`_.
  As part of this I have removed the following fields from the [Fediverse] section of the config file:
  - max_reblog
  - no_reblog_tags
  - no_reblog_users
  - search_instance
  - search_tags

.. _fedibooster: https://codeberg.org/marvinsmastodontools/fedibooster

Changed
-------

- Updated CI to include `bandit`_ checks.

.. _bandit: https://github.com/PyCQA/bandit

- Update CI to use standard uv container image as provided by Astral

- Updated dependencies versions

.. _changelog-1.4.0:

1.4.0 — 2024-11-05
==================

Breaking
--------

- Replace boosting statuses from the home timeline with boost statuses containing some tags.
  These statuses can optionally be sourced from another instance.
  To implement this two new configuration parameters in the `[Fediverse]` section have been added:

  - `search_instance`: is of type string and points to instance that should be used to find statuses with certain tags.
  - `search_tags`: is a list of strings and is the list of hashtags to search statuses for. Statuses having _any_ of the
    tags in this list will be considered for reblogging / boosting.

Changed
-------

- Minor change to how duplicate posts are recorded. There might be a slight increase in the size of the history DB.

- Updated CI

- Updated pre-commit config

- Updated dependencies versions

.. _changelog-1.3.0:

1.3.0 — 2024-10-12
==================

Added
-----

- Added ability to skip reblogging posts by certain users. Users can be specified similar
  to how no reblog tags are specified in a `no_reblog_users` list in the config file.
  Users should be specified in the format <username>@<instance.url>

Changed
-------

- Updated dependencies versions.

.. _changelog-1.2.0:

1.2.0 — 2024-09-08
==================

Added
-----

- Command line option to point to full path to logging config file.

- Docker / Podman container file to be able to run `lemmy2fedi` in a docker container
  The docker file is located at https://codeberg.org/marvinsmastodontools/-/packages/container/lemmy2fedi

Changed
-------

- Updated dependencies versions

.. _changelog-1.1.2:

1.1.2 — 2024-08-31
==================

Changed
-------

- Added handling of RatelimitError when loading home timeline

- Updated Dependencies

.. _changelog-1.1.1:

1.1.1 — 2024-08-25
==================

Changed
-------

- Update dependencies versions

.. _changelog-1.1.0:

1.1.0 — 2024-06-10
==================

Added
-----

- Added config option called `history_prune_age` to define maximum age we are
  keeping history records for. Any posts older than this in days will be pruned.
  This option defaults to `30` days if not otherwise set.

Changed
-------

- Updated dependencies versions

.. _changelog-1.0.0:

1.0.0 — 2024-05-10
==================

Initial release
