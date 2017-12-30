import os

from gisrep.config import Config

import pytest

TEST_INITIAL_CONFIG = {
    'username': "my_name",
    'password': "my_password",
}


class TestPasswordManager(object):
    def __init__(self):
        self.passwords = {}

    def set_password(self, service, username, password):
        self.passwords[service + username] = password

    def get_password(self, service, username):
        return self.passwords[service + username]


@pytest.fixture
def config(tmpdir):
    return Config(
        os.path.join(str(tmpdir), '.gisreprc'),
        TestPasswordManager(),
        initial_config=TEST_INITIAL_CONFIG)
