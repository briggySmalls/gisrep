|Build Status|

Gisrep
======

The command line Github issues reporter, powered by
`PyGithub <https://github.com/PyGithub/PyGithub>`__ and the
`jinja2 <http://jinja.pocoo.org/docs/2.10/>`__ templating engine.

Installation
------------

::

    pip install gisrep

This installs the ``gisrep`` script to the command line.

Usage
-----

You can type `gisrep --help` to see guidance on how to use the script.

Publishing reports
~~~~~~~~~~~~~~~~~~

Publishing reports uses the ``report`` subcommand and a query for the `Github search
API <https://developer.github.com/v3/search/#search-issues>`__:

::

    gisrep report "repo:twbs/bootstrap is:open label:feature"

Which will print a summary of the issues to the console:

::

    - v4 - Touch gesture support for carousel [#17118]
    - Modal animations for v4 - some examples [#17219]
    - Request - bring muted backgrounds back [#17245]
    - Horizontal collapse [#17496]
    - Add styling for <input type="range"> [#17916]
    - Consider integrating Drool to check for leaks in the JS [#17932]
    - Add option to enable/disable animation of Collapse on a per-show/hide basis [#18127]
    ...

Read the Github guide on `searching issues and
pull
requests <https://help.github.com/articles/searching-issues-and-pull-requests/>`__
for help constructing queries.

Formatting results
~~~~~~~~~~~~~~~~~~

Issues can be formatted with templates - either those shipped with gisrep, or custom user templates.

::

    # Specify gisrep template tag
    gisrep report "repo:twbs/bootstrap is:open label:feature" --internal list_by_labels.html

    # Pass path of a user template
    gisrep report "repo:twbs/bootstrap is:open label:feature" --external ./custom-report.rst

To list the tags for built-in templates use the following command:

::

    gisrep list

Read the `templates
readme <gisrep/templates/README.rst>`__ for creating custom templates.

Private repositories
--------------------

The tool needs Github credentials in order to access private repositories.
Credentials can be provided as command line arguments directly, or supplied
in a `.gisreprc` config file.

A config file can be initialised and saved to your home directory with the following command:

::

    gisrep init

You will be prompted for your Github username and password. Note that if your Github
account uses 2 factor authentication, then the password provided to gisrep
should be a `personal access token
<https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__.

The password is stored in your system’s password manager using
`keyring <https://pypi.python.org/pypi/keyring>`__.

.. |Build Status| image:: https://travis-ci.org/briggySmalls/gisrep.svg?branch=master
   :target: https://travis-ci.org/briggySmalls/gisrep
