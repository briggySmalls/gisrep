Getting started
***************

Publishing reports
~~~~~~~~~~~~~~~~~~

Publishing reports uses the ``report`` command and a query for the `Github search
API <https://developer.github.com/v3/search/#search-issues>`__:

.. code-block:: none

    gisrep report "repo:briggySmalls/gisrep is:open label:enhancement"

Which will print a summary of the issues to the console:

.. code-block:: none

    - Make project open-source friendly [#2]
    - Add custom errors and improve handling [#4]
    - Add coverage tests [#14]
    - Allow user to provide jinja2 environment configuration [#16]
    ...

Read the Github guide on `searching issues and pull
requests <https://help.github.com/articles/searching-issues-and-pull-requests/>`__
for help constructing queries.

Formatting results
~~~~~~~~~~~~~~~~~~

Issues can be formatted with templates - either those shipped with
gisrep internally, or external user templates.

.. code-block:: none

    # Specify gisrep template tag
    gisrep report "repo:twbs/bootstrap is:open label:feature" --internal list_by_labels.html

    # Pass path of a user template
    gisrep report "repo:twbs/bootstrap is:open label:feature" --external ./custom-report.rst.tplt

Internal template tags can be listed using the `list` command:

.. code-block:: none

    gisrep list

Read the `templates documentation <./templates.html>`__ for creating
custom templates.

Private repositories
~~~~~~~~~~~~~~~~~~~~

The tool needs Github credentials in order to access private repositories.
Credentials can be provided as command line arguments directly, or supplied
in a `.gisreprc` config file.
A config file can be initialised and saved to your home directory with the `init` command:

.. code-block:: none

    gisrep init

You will be prompted for your Github username and password. The password is stored in your system’s
password manager using `keyring <https://pypi.python.org/pypi/keyring>`__.

Note that if your Github
account uses 2 factor authentication, then the password provided to gisrep
should be a `personal access token
<https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__.
