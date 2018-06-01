"""
Tests the gisrep module
"""

from gisrep.gisrep import _get_credentials

from .conftest import TEST_INITIAL_CONFIG


def test_local_config_credentials(config):
    """Tests the _get_credentials function find a local config file

    Args:
        config (Config): A config object
    """

    # Make call to _get_credentials
    credentials = _get_credentials(  # pylint: disable=protected-access
        config=config.file_path)

    # Assert returned credentials are correct
    assert credentials['username'] == TEST_INITIAL_CONFIG['username']
    assert credentials['password'] == TEST_INITIAL_CONFIG['password']
