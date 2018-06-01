"""
Tests the gisrep module
"""

import os

from gisrep.gisrep import _get_credentials, _get_template_manager

from .conftest import TEST_INITIAL_CONFIG
from .test_template_manager import (
    EXTERNAL_TEMPLATE_TAG, INTERNAL_TEMPLATE_TAG, TEST_DATA_DIR,
    assert_external_list, assert_internal_list)


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


def test_internal_template_manager():
    """Tests the _get_template_manager function finds an internal template
    """

    # Make call to _get_template_manager
    manager, tag = _get_template_manager(  # pylint: disable=protected-access
        external=None, internal=INTERNAL_TEMPLATE_TAG)

    # Assert returned variables are correct
    assert tag == INTERNAL_TEMPLATE_TAG
    assert_internal_list(manager)


def test_external_template_manager():
    """Tests the _get_template_manager function finds an external template
    """

    # Make call to _get_template_manager
    manager, tag = _get_template_manager(  # pylint: disable=protected-access
        internal=None,
        external=os.path.join(TEST_DATA_DIR, EXTERNAL_TEMPLATE_TAG))

    # Assert returned variables are correct
    assert tag == "test_template"
    assert_external_list(manager)
