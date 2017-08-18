import unittest
from gisrep.config import Config
import os

TEST_CONFIG_PATH = os.path.abspath('.')
TEST_CONFIG_FILE = os.path.join(TEST_CONFIG_PATH, '.gisrep_config')
TEST_INITIAL_CONFIG = {
    'username': "my_name",
    'password': "my_password",
}

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Ensure no previous file exists
        try:
            os.remove(TEST_CONFIG_FILE)
        except OSError:
            pass

        # Create a new config file
        self.config = self.new_config(
            initial_config=TEST_INITIAL_CONFIG)

    def tearDown(self):
        # Remove the config file
        os.remove(TEST_CONFIG_FILE)

    def test_new_config(self):
        # Assert config file exists
        self.assertTrue(os.path.exists(TEST_CONFIG_FILE))

        # Assert the original config object
        self.assert_credentials(self.config, TEST_INITIAL_CONFIG)
        # Assert a fresh config object
        self.assert_credentials(self.new_config(), TEST_INITIAL_CONFIG)

    def test_force_config(self):
        # Create different config content
        different_content = {
            'username': "different_name",
            'password': "different_password",
        }

        def init_new_config(force):
            return self.new_config(
                initial_config=different_content,
                force=force)

        # First try to create new config without force arg
        self.assertRaises(RuntimeError, init_new_config, False)

        # Now force a new config file to be written
        config = init_new_config(force=True)

        # Assert contents of origintal config object
        self.assert_credentials(config, different_content)
        # Assert contents of fresh config object
        self.assert_credentials(self.new_config(), different_content)

    def new_config(self, **kwargs):
        return Config(path=TEST_CONFIG_FILE, **kwargs)

    def assert_credentials(self, config, expected_credentials):
        # Get the content
        credentials = config.get_credentials()
        # Assert config content
        self.assertEqual(credentials['username'], expected_credentials['username'])
        self.assertEqual(credentials['password'], expected_credentials['password'])
