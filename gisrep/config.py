"""Config file management logic

Attributes:
    PASSWORD_SERVICE_NAME (str): Password service name used to store
    credentials
"""

import os

import keyring
import toml

from .errors import GisrepError

PASSWORD_SERVICE_NAME = "gisrep"


def create_config(initial_config):
    """Creates a configuration file

    Args:
        initial_config (dict): The initial configuration

    Returns:
        Config: Configuration object
    """

    # Save the password in the keyring
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

    def __init__(
            self, path, initial_config=None, force=False):
        """Class for managing configuration file.

        Args:
            path (str): The path of the config file
            initial_config (dict, optional): The initial configuration
            force (bool, optional): Whether to force creation of a new config
                                    file

        Raises:
            GisrepError: Description
        """

        self._file_path = path
        # Determine if a config file already exists
        if os.path.exists(self._file_path) and not force:
            if initial_config is not None:
                # Attempted to overwrite config without 'force'
                raise GisrepError(
                    "Config file already exists. Try the --force argument")

            # Read the existing config file
            self.config = self.read()
        elif initial_config is not None:
            # We are creating the config file now
            self.config = create_config(initial_config)
            self.write()
        else:
            # No config found (or provided)
            raise GisrepError("Config file doesn't exist")

    @property
    def file_path(self):
        """Gets the file path of the config file abstracted by this object

        Returns:
            str: File path of config file
        """
        return self._file_path

    def get_credentials(self):
        """Gets the credentials from the configuration file

        Returns:
            dict: The credentials

        Raises:
            GisrepError: Description
        """
        username = self.config['github']['username']
        password_service = self.config['github']['password_service']
        password = keyring.get_password(
            password_service,
            username)

        if password is None:
            raise GisrepError("Password not found in password manager")

        return {
            'username': username,
            'password': password,
        }

    def read(self):
        """Reads the configuration stored in the config file

        Returns:
            dict: Configuration
        """
        return toml.load(self._file_path)

    def write(self):
        """Writes the current configuration to the config file
        """
        with open(self._file_path, 'w') as config_file:
            toml.dump(self.config, config_file)
