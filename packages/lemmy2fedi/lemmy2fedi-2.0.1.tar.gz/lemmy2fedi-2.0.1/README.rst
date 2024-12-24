""""""""""""""""""""""""""
Lemmy2Fedi
""""""""""""""""""""""""""

|Repo| |CI| |AGPL|

|Checked with| |Downloads|

|Code style| |Version| |Wheel|



Lemmy2Fedi is a command line (CLI) tool / bot / robot to cross post statuses from Lemmy communities to a
Fediverse / Mastodon account.
It respects rate limits imposed by servers.

Install and run from `PyPi <https://pypi.org>`_
=================================================

It's ease to install Lemmy2Fedi from Pypi using the following command::

    pip install lemmy2fedi

Once installed Lemmy2Fedi can be started by typing ``lemmy2fedi`` into the command line.

Install and run from `Source <https://codeberg.org/MarvinsMastodonTools/lemmy2fedi>`_
==============================================================================================

Alternatively you can run Lemmy2Fedi from source by cloning the repository using the following command line::

    git clone https://codeberg.org/MarvinsMastodonTools/lemmy2fedi.git

Lemmy2Fedi uses `uv`_ for dependency control, please install Rye before proceeding further.

Before running, make sure you have all required python modules installed. With Rye this is as easy as::

    uv sync

Run Lemmy2Fedi with the command `uv run lemmy2fedi`

Configuration / First Run
=========================

Lemmy2Fedi will ask for all necessary parameters when run for the first time and store them in ```config.toml``
file in the current directory.

Licensing
=========
Lemmy2Fedi is licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_

Supporting Lemmy2Fedi
==========================

There are a number of ways you can support Lemmy2Fedi:

- Create an issue with problems or ideas you have with/for Lemmy2Fedi
- Create a pull request if you are more of a hands on person.
- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.
- You can send me small change in Monero to the address below:

Monero donation address
-----------------------
``867kZN5dq8bX63sZAF562PjRNrnccWVreEhyHzovqCSHBXTYbMNFU8uJ4dv7TqhnmuV3vf39bst1DYhgPyHJxjFtKauk3MC``


.. _uv: https://docs.astral.sh/uv/

.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
    :alt: AGLP 3 or later
    :target:  https://codeberg.org/MarvinsMastodonTools/lemmy2fedi/src/branch/main/LICENSE.md

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
    :alt: Repo at Codeberg.org
    :target: https://codeberg.org/MarvinsMastodonTools/lemmy2fedi

.. |Downloads| image:: https://pepy.tech/badge/lemmy2fedi
    :alt: Download count
    :target: https://pepy.tech/project/lemmy2fedi

.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: Black
    :target: https://github.com/psf/black

.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green
    :alt: Checked with pip-audit
    :target: https://pypi.org/project/pip-audit/

.. |Version| image:: https://img.shields.io/pypi/pyversions/lemmy2fedi
    :alt: PyPI - Python Version

.. |Wheel| image:: https://img.shields.io/pypi/wheel/lemmyfedi
    :alt: PyPI - Wheel

.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/lemmy2fedi/status.svg
    :alt: CI / Woodpecker
    :target: https://ci.codeberg.org/MarvinsMastodonTools/lemmy2fedi
