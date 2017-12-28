from unittest.mock import Mock

from gisrep import gisrep

import conftest
import pytest


def test_get_credentials_direct():
    # Construct mock argparse.Namespace object
    credentials_args = Mock(
        username=conftest.TEST_INITIAL_CONFIG['username'],
        password=conftest.TEST_INITIAL_CONFIG['password'],
        config=None)

    # Make call to _get_credentials
    credentials = gisrep._get_credentials(
        credentials_args)

    # Assert returned credentials are correct
    assert credentials['username'] == conftest.TEST_INITIAL_CONFIG['username']
    assert credentials['password'] == conftest.TEST_INITIAL_CONFIG['password']


@pytest.mark.keyring
def test_get_credentials_local_config(config):
    # Construct mock argparse.Namespace object specifying config file
    local_config_args = Mock(
        username=None,
        password=None,
        config=config.file_path)

    # Make call to _get_credentials
    credentials = gisrep._get_credentials(
        local_config_args)

    # Assert returned credentials are correct
    assert credentials['username'] == conftest.TEST_INITIAL_CONFIG['username']
    assert credentials['password'] == conftest.TEST_INITIAL_CONFIG['password']
