import os
from unittest.mock import Mock

from gisrep import gisrep

import conftest
from test_template_manager import (
    EXTERNAL_TEMPLATE_TAG, INTERNAL_TEMPLATE_TAG, TEST_DATA_DIR,
    assert_external_list, assert_internal_list)


def test_get_credentials_direct():
    # Construct mock argparse.Namespace object
    args = Mock(
        username=conftest.TEST_INITIAL_CONFIG['username'],
        password=conftest.TEST_INITIAL_CONFIG['password'],
        config=None)

    # Make call to _get_credentials
    credentials = gisrep._get_credentials(
        args,
        conftest.TestPasswordManager())

    # Assert returned credentials are correct
    assert credentials['username'] == conftest.TEST_INITIAL_CONFIG['username']
    assert credentials['password'] == conftest.TEST_INITIAL_CONFIG['password']


def test_get_credentials_local_config(config):
    # Construct mock argparse.Namespace object specifying config file
    args = Mock(
        username=None,
        password=None,
        config=config.file_path)

    # Make call to _get_credentials
    credentials = gisrep._get_credentials(
        args,
        config._password_manager)

    # Assert returned credentials are correct
    assert credentials['username'] == conftest.TEST_INITIAL_CONFIG['username']
    assert credentials['password'] == conftest.TEST_INITIAL_CONFIG['password']


def test_get_template_manager_internal():
    # Construct mock argparse.Namespace object specifying config file
    args = Mock(
        external=None,
        internal=INTERNAL_TEMPLATE_TAG)

    # Make call to _get_template_manager
    manager, tag = gisrep._get_template_manager(args)

    # Assert returned variables are correct
    assert tag == INTERNAL_TEMPLATE_TAG
    assert_internal_list(manager)


def test_get_template_manager_external():
        # Construct mock argparse.Namespace object specifying config file
    args = Mock(
        internal=None,
        external=os.path.join(TEST_DATA_DIR, EXTERNAL_TEMPLATE_TAG))

    # Make call to _get_template_manager
    manager, tag = gisrep._get_template_manager(args)

    # Assert returned variables are correct
    assert tag == "test_template"
    assert_external_list(manager)
