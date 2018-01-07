"""
Tests the Config module
"""

import os

import pytest

from gisrep.config import Config

from .conftest import TEST_INITIAL_CONFIG


def test_new_config(config):
    """Tests the creation of a duplicate config object

    Args:
        config (Config): A config object
    """

    # Assert config file exists
    assert os.path.exists(config.file_path)

    # Assert the original config object
    assert_credentials(config, TEST_INITIAL_CONFIG)

    # Assert a fresh config object
    new_config = Config(config.file_path)
    assert_credentials(new_config, TEST_INITIAL_CONFIG)


def test_force_config(config):
    """Tests the forced creation of a new config object

    Args:
        config (Config): A config object
       (MockPasswordManager): A mock password manager
    """
    # Create different config content
    different_content = {
        'username': "different_name",
        'password': "different_password",
    }

    # First try to create new config without force arg
    with pytest.raises(RuntimeError):
        Config(
            path=config.file_path,
            initial_config=different_content,
            force=False)

    # Now force a new config file to be written
    new_config = Config(
        path=config.file_path,
        initial_config=different_content,
        force=True)

    # Assert contents of original config object
    assert_credentials(new_config, different_content)

    # Assert contents of fresh config object
    assert_credentials(
        Config(config.file_path),
        different_content)


def assert_credentials(config, expected_credentials):
    """Helper function to assert Config credentials match those supplied

    Args:
        config (Config): Config object
        expected_credentials (dict): Credentials to assert
    """
    # Get the content
    credentials = config.get_credentials()

    # Assert config content
    assert credentials['username'] == expected_credentials['username']
    assert credentials['password'] == expected_credentials['password']
