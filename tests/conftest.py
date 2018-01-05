"""
Pytest module for common test configuration code

Attributes:
    TEST_INITIAL_CONFIG (TYPE): Description
"""

import os

import pytest

from gisrep.config import Config

TEST_INITIAL_CONFIG = {
    'username': "my_name",
    'password': "my_password",
}


class MockPasswordManager(object):

    """Mocks a password manager

    Attributes:
        passwords (dict): Lookup for passwords
    """

    def __init__(self):
        self.passwords = {}

    def set_password(self, service, username, password):
        """Records a password against a service/username combination

        Args:
            service (str): Service password is associated with
            username (str): Username password is associated with
            password (str): Password to store
        """
        self.passwords[service + username] = password

    def get_password(self, service, username):
        """Returns a password for a given servie/username combination

        Args:
            service (str): Description
            username (str): Description

        Returns:
            str: Password
        """
        return self.passwords[service + username]


@pytest.fixture
def password_manager():
    """Returns a MockPasswordManager object

    Returns:
        MockPasswordManager: The mock password manager
    """
    return MockPasswordManager()


@pytest.fixture
def config(tmpdir, password_manager):  # pylint: disable=redefined-outer-name
    """Fixture that provides a config object

    Args:
        tmpdir (py.path.local): Temporary pytest directory to place config file
        password_manager (MockPasswordManager): Mock password manager

    Returns:
        Config: Config object
    """
    return Config(
        os.path.join(str(tmpdir), '.gisreprc'),
        password_manager,
        initial_config=TEST_INITIAL_CONFIG)
