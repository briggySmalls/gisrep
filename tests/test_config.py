import os

from gisrep.config import Config

from conftest import TEST_INITIAL_CONFIG
import pytest


def test_new_config(config):
    # Assert config file exists
    assert os.path.exists(config.file_path)

    # Assert the original config object
    assert_credentials(config, TEST_INITIAL_CONFIG)

    # Assert a fresh config object
    new_config = Config(config.file_path, config._password_manager)
    assert_credentials(new_config, TEST_INITIAL_CONFIG)


def test_force_config(config):
    # Create different config content
    different_content = {
        'username': "different_name",
        'password': "different_password",
    }

    # First try to create new config without force arg
    with pytest.raises(RuntimeError):
        Config(
            path=config.file_path,
            password_manager=config._password_manager,
            initial_config=different_content,
            force=False)

    # Now force a new config file to be written
    new_config = Config(
        path=config.file_path,
        password_manager=config._password_manager,
        initial_config=different_content,
        force=True)

    # Assert contents of original config object
    assert_credentials(new_config, different_content)

    # Assert contents of fresh config object
    assert_credentials(
        Config(config.file_path, config._password_manager),
        different_content)


def assert_credentials(config, expected_credentials):
    # Get the content
    credentials = config.get_credentials()
    # Assert config content
    assert credentials['username'] == expected_credentials['username']
    assert credentials['password'] == expected_credentials['password']
