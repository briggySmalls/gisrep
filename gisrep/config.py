import toml
import keyring
import os

DEFAULT_PASSWORD_SERVICE = "gisrep"


class Config(object):

    def __init__(self, path, initial_config=None, force=False):
        """
        Class for managing configuration file.

        :param      path:            The path of the config file
        :param      initial_config:  The initial configuration
        :param      force:           Whether to force creation of a new config file
        :type       path:            string
        :type       initial_config:  dict
        :type       force:           boolean

        :returns:   None
        :rtype:     None
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
            self.config = self.create_config(initial_config)
            self.write()
        else:
            # No config found (or provided)
            raise RuntimeError("Config file doesn't exist")

    def get_credentials(self):
        """
        Gets the credentials from the config

        :returns:   The credentials.
        :rtype:     dict
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

    def create_config(self, initial_config):
        """
        Creates a configuration file

        :param      initial_config:  The initial configuration
        :type       initial_config:  dict

        :returns:   Configuration
        :rtype:     Config
        """

        # Save the password in the password manager
        keyring.set_password(
            DEFAULT_PASSWORD_SERVICE,
            initial_config['username'],
            initial_config['password'])

        config = {}

        # Format a github section
        config['github'] = {
            'username': initial_config['username'],
            'password_service': DEFAULT_PASSWORD_SERVICE,
        }

        # Return the new config
        return config

    def read(self):
        """
        Reads the configuration stored in the config file

        :returns:   Configuration
        :rtype:     dict
        """

        return toml.load(self.file_path)

    def write(self):
        """
        Writes the current configuration to the config file

        :returns:   None
        :rtype:     None
        """

        with open(self.file_path, 'w') as config_file:
            toml.dump(self.config, config_file)
