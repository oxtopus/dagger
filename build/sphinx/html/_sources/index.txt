.. Dagger documentation master file, created by
   sphinx-quickstart on Wed Jul 17 22:13:31 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======
Dagger
======

.. _installation:

Installation
============

Installation is managed via setuptools.

::

    $ python setup.py install


Usage
=====

Once installed, dagger operations are executed via the included ``dagger``
command-line utility, specifying sub-commands.  For a complete list of
available sub-commands, run ``dagger --help``.

For example:

::

    $ dagger --help
    Usage: dagger [command] [options]

    Available commands:

        status
        init
        run

    Options:
      -h, --help  show this help message and exit

Initializing a project
----------------------

First, initiliaze a project using the ``init`` sub-command.

::

    $ cd <path to project>
    $ dagger init

By default, this will create a branch named ``CI`` in your project repository
and a file named ``dagger.cfg`` in the root of the project in the ``CI``
branch.

::

    $ git checkout CI
    $ cat dagger.cfg
    [dagger]
    tracking = master
    remote = origin
    script =

Edit your ``dagger.cfg`` file, specifying a value for the ``script``
configuration option in the ``[dagger]`` section.  This is the command that
will validate a project.  Add and commit your changes, return to your
development branch.

::

    $ git commit -a
    $ git checkout master

Next steps
----------

At any time, you can run the ``status`` sub-command to report the status of
your project within the context of Dagger.  The status sub-command will report
the number of commits your stable branch is behind development:

::

    $ dagger status

If this is your first time, your stable branch will be significantly behind
your development branch (this is normal).

::

    $ dagger run

Assuming validation passed, your stable branch will have caught up to
development.  Verify by running the ``status`` sub-command again:

::

    $ dagger status

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

