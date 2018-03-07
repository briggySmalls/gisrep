Installation
************

General
~~~~~~~

Install gisrep using pip with:

::

    pip install gisrep

This installs the ``gisrep`` script to the command line.

Linux
~~~~~

Gisrep uses keyring to interface with the system password manager. On Linux, the recommended
keyring relies on SecretStorage, which in turn relies on dbus-python.

dbus-python does not install correctly when using the Python installers, so dbus-python must
 be installed as a system package. E.g. on Ubuntu:

::

    sudo apt-get install python3-dbus

See the `SecretStorage GitHub repo
<https://github.com/mitya57/secretstorage>`__ for details.
