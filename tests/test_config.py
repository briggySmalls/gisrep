import os

from gisrep.config import Config

import pytest

TEST_INITIAL_CONFIG = {
    'username': "my_name",
    'password': "my_password",
}


@pytest.fixture
def config(tmpdir):
    return Config(
        path=os.path.join(tmpdir, '.gisreprc'),
        initial_config=TEST_INITIAL_CONFIG)


@pytest.mark.keyring
def test_new_config(config):
    # Assert config file exists
    assert os.path.exists(config.file_path)

    # Assert the original config object
    assert_credentials(config, TEST_INITIAL_CONFIG)

    # Assert a fresh config object
    new_config = Config(config.file_path)
    assert_credentials(new_config, TEST_INITIAL_CONFIG)


@pytest.mark.keyring
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
            initial_config=different_content,
            force=False)

    # Now force a new config file to be written
    new_config = Config(
        path=config.file_path,
        initial_config=different_content,
        force=True)

    # Assert contents of origintal config object
    assert_credentials(new_config, different_content)

    # Assert contents of fresh config object
    assert_credentials(Config(config.file_path), different_content)


def assert_credentials(self, config, expected_credentials):
    # Get the content
    credentials = config.get_credentials()
    # Assert config content
    assert credentials['username'] == expected_credentials['username']
    assert credentials['password'] == expected_credentials['password']
