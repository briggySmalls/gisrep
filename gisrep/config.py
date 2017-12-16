"""Config file management logic

Attributes:
    PASSWORD_SERVICE_NAME (str): Password service name used to store
    credentials
"""

import os

import keyring
import toml

PASSWORD_SERVICE_NAME = "gisrep"


def create_config(initial_config):
    """Creates a configuration file

    Args:
        initial_config (dict): The initial configuration

    Returns:
        Config: Configuration object
    """

    # Save the password in the password manager
    keyring.set_password(
        PASSWORD_SERVICE_NAME,
        initial_config['username'],
        initial_config['password'])

    config = {}

    # Format a github section
    config['github'] = {
        'username': initial_config['username'],
        'password_service': PASSWORD_SERVICE_NAME,
    }

    # Return the new config
    return config


class Config(object):

    """Config file content abstraction

    Attributes:
        config (dict): Configuration file content
        file_path (str): File path of config file
    """

    def __init__(self, path, initial_config=None, force=False):
        """Class for managing configuration file.

        Args:
            path (str): The path of the config file
            initial_config (dict, optional): The initial configuration
            force (bool, optional): Whether to force creation of a new config
                                    file

        Raises:
            RuntimeError: Description
        """

        self.file_path = path
        # Determine if a config file already exists
        if os.path.exists(self.file_path) and not force:
            if initial_config is not None:
                # Attempted to overwrite config without 'force'
                raise RuntimeError("Config file already exists")

            # Read the existing config file
            self.config = self.read()
        elif initial_config is not None:
            # We are creating the config file now
            self.config = create_config(initial_config)
            self.write()
        else:
            # No config found (or provided)
            raise RuntimeError("Config file doesn't exist")

    def get_credentials(self):
        """Gets the credentials from the configuration file

        Returns:
            dict: The credentials

        Raises:
            RuntimeError: Description
        """
        username = self.config['github']['username']
        password_service = self.config['github']['password_service']
        password = keyring.get_password(
            password_service,
            username)

        if password is None:
            raise RuntimeError("Password not found in password manager")

        return {
            'username': username,
            'password': password,
        }

    def read(self):
        """Reads the configuration stored in the config file

        Returns:
            dict: Configuration
        """
        return toml.load(self.file_path)

    def write(self):
        """Writes the current configuration to the config file
        """
        with open(self.file_path, 'w') as config_file:
            toml.dump(self.config, config_file)
