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
        path=os.path.join(str(tmpdir), '.gisreprc'),
        initial_config=TEST_INITIAL_CONFIG)
