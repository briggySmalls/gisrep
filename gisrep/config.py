import toml
import keyring
import os

DEFAULT_CONFIG_PATH = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisrep_config"
DEFAULT_PASSWORD_SERVICE = "gisrep"


class Config(object):
    def __init__(self, path=DEFAULT_CONFIG_PATH, initial_config=None, force=False):
        # Read the contents of an existing config file
        self.file_path = os.path.join(path, DEFAULT_CONFIG_FILE)

        # Determine if a config file already exists
        if os.path.exists(self.file_path) and not force:
            if initial_config is not None:
                # Attempted to overwrite config without 'force'
                raise RuntimeError("Config file already exists")

            # Read the existing config file
            self.config = self._read()
        elif initial_config is not None:
            # We are creating the config file now
            self.config = self._create_config(initial_config)
            self._write()
        else:
            # No config found (or provided)
            raise RuntimeError("Config file doesn't exist")

    def get_credentials(self):
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

    def add_template_dir(self, directory):
        self.template_dirs.append(directory)
        self._write()

    def add_output_dir(self, directory):
        self.output_dirs.append(directory)
        self._write()

    def remove_template_dir(self, directory):
        self.template_dirs.remove(directory)
        self._write()

    def remove_output_dir(self, directory):
        self.output_dirs.remove(directory)
        self._write()

    @property
    def template_dirs(self):
        return self.config['tool']['user_template_dirs']

    def _create_config(self, initial_config):       
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

        # Create tool placeholder config
        config['tool'] = {
            'user_template_dirs': [],
        }

        # Return the new config
        return config

    def _read(self):
        return toml.load(self.file_path)

    def _write(self):
        with open(self.file_path, 'w') as config_file:
            toml.dump(self.config, config_file)
