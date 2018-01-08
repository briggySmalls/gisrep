Contributing
============

Contributions to gisrep are warmly welcomed, thank you for your
endeavours! 🙌

Bug reporting and feature requests are tracked using Github's issue
tracker. Don't hesitate to create an issue for either if one does not
already exist.

Please note we have a `Code of Conduct`_, please
follow it in all your interactions with the project.

Pull Request Process
--------------------

The following outlines the preferred pull request process, we follow the
"fork-and-pull" Git workflow:

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch. Use a branch with a name of the
   form ``{type}/{name}`` where:

   -  ``{type}`` is either ‘fix’ for a bug fix or ‘enhancement’ for an
      enhancement.
   -  ``{name}`` is a short descriptive name in kebab-case.

4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes. Reference
   any relevant issues in your pull request description.
6. Ensure that the CI server finds the tests to pass.

NOTE: Be sure to merge the latest from "upstream" before making a pull
request!

Testing
-------

Tests and their dependencies are managed by
`tox <https://tox.readthedocs.io/en/latest/#>`__.

Running all the tests, as on the CI server, is as simple as:

::

    pip install tox
    tox

Chances are you will prefer to run a subset of tests locally:

::

    tox -e py36  # Run tests on python 3.6 environment
    tox -e coverage  # Run tests with coverage report
    tox -e lint  # Run the linters
    tox -e format  # Run the formatters

Code of Conduct
---------------

Our Pledge
~~~~~~~~~~

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our
project and our community a harassment-free experience for everyone,
regardless of age, body size, disability, ethnicity, gender identity and
expression, level of experience, nationality, personal appearance, race,
religion, or sexual identity and orientation.

Our Standards
~~~~~~~~~~~~~

Examples of behavior that contributes to creating a positive environment
include:

-  Using welcoming and inclusive language
-  Being respectful of differing viewpoints and experiences
-  Gracefully accepting constructive criticism
-  Focusing on what is best for the community
-  Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

-  The use of sexualized language or imagery and unwelcome sexual
   attention or advances
-  Trolling, insulting/derogatory comments, and personal or political
   attacks
-  Public or private harassment
-  Publishing others’ private information, such as a physical or
   electronic address, without explicit permission
-  Other conduct which could reasonably be considered inappropriate in a
   professional setting

Our Responsibilities
~~~~~~~~~~~~~~~~~~~~

Project maintainers are responsible for clarifying the standards of
acceptable behavior and are expected to take appropriate and fair
corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit,
or reject comments, commits, code, wiki edits, issues, and other
contributions that are not aligned to this Code of Conduct, or to ban
temporarily or permanently any contributor for other behaviors that they
deem inappropriate, threatening, offensive, or harmful.

Scope
~~~~~

This Code of Conduct applies both within project spaces and in public
spaces when an individual is representing the project or its community.
Examples of representing a project or community include using an
official project e-mail address, posting via an official social media
account, or acting as an appointed representative at an online or
offline event. Representation of a project may be further defined and
clarified by project maintainers.

Attribution
~~~~~~~~~~~

This Code of Conduct is adapted from `Billy Thompson’s gist
<https://gist.github.com/PurpleBooth/b24679402957c63ec426>`__ which is in
turn adapted from the `Contributor Covenant version 1.5
<http://contributor-covenant.org/version/1/4/>`__.
