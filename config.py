import configparser
import keyring
import os

DEFAULT_CONFIG_PATH = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".ir_config"
DEFAULT_PASSWORD_SERVICE = "issues-reporter"


class Config(object):
    def __init__(self, path=DEFAULT_CONFIG_PATH, initial_config=None, force=False):
        # Create the parser instance
        self.parser = configparser.ConfigParser()
        self.file_path = os.path.join(path, DEFAULT_CONFIG_FILE)
        # Determine if a config file already exists
        if os.path.exists(self.file_path) and not force:
            if initial_config is not None:
                # Attempted to overwrite config without 'force'
                raise RuntimeError("Config file already exists")
            # Read the existing config file
            self.parser.read(self.file_path)
        elif initial_config is not None:
            # We are creating the config file now
            self._create_config_file(
                initial_config['username'],
                initial_config['password'])
        else:
            # No config found (or provided)
            raise RuntimeError("Config file doesn't exist")

    def get_credentials(self):
        username = self.parser['user']['username']
        password_service = self.parser['user']['service']
        password = keyring.get_password(
            password_service,
            username)
        return {
            'username': username,
            'password': password,
        }

    def _create_config_file(self, username, password):       
        # Set the config content
        self.parser['user'] = {
            'username': username,
            'service': DEFAULT_PASSWORD_SERVICE,
        }
        # Save the password in the password manager
        keyring.set_password(DEFAULT_PASSWORD_SERVICE, username, password)
        # Save the new config file
        self._save()

    def _save(self):
        with open(self.file_path, 'w') as config_file:
            self.parser.write(config_file)
