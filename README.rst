|Build Status| |Coverage Status| |PyPI Versions|

Gisrep
======

The command line Github issues reporter, making requests with
`PyGithub <https://github.com/PyGithub/PyGithub>`__ and formatting the results with
`jinja2 <http://jinja.pocoo.org/docs/2.10/>`__.

Taster
------

Generate issue reports and release notes effortlessly with a query for the `Github search
API <https://developer.github.com/v3/search/#search-issues>`__:

.. code-block:: none

    $ pip install gisrep
    $ gisrep report 'repo:briggySmalls/gisrep label:enhancement milestone:"milestone name"'
    - Make project open-source friendly [#2]
    - Add custom errors and improve handling [#4]
    - Add coverage tests [#14]
    - Allow user to provide jinja2 environment configuration [#16]
    ...

Features
--------

- Customisable output using either included or custom templates
- Connect to private Github repos

Documentation
-------------

For guidance on installation and usage, check out the
`documentation <https://briggysmalls.github.io/gisrep/>`__.

Contributing
------------

You may contribute in several ways like creating new features, fixing
bugs or improving documentation and examples. `Find more information in
CONTRIBUTING.rst <CONTRIBUTING.rst>`__.

.. |Build Status| image:: https://travis-ci.org/briggySmalls/gisrep.svg?branch=master
   :target: https://travis-ci.org/briggySmalls/gisrep?branch=master
.. |Coverage Status| image:: https://coveralls.io/repos/github/briggySmalls/gisrep/badge.svg?branch=master
   :target: https://coveralls.io/github/briggySmalls/gisrep?branch=master
.. |PyPI Versions| image:: https://img.shields.io/pypi/pyversions/gisrep.svg
   :alt: PyPI - Python Version
