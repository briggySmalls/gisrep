import configparser
import os

DEFAULT_CONFIG_PATH = os.path.abspath('~/')
DEFAULT_CONFIG_FILE = '.ir_config'


class Config(object):
    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.file_path = os.path.join(path, DEFAULT_CONFIG_FILE)
        self.parser = configparser.ConfigParser()
        if os.path.exists(self.file_path):
            self.parser.read(self.file_path)

    def init(self, username, password):
        self.parser['user'] = {
            'username': username,
            'password': password,
        }
        # Save the new details
        self.save()

    def set_repo(self, tag, url):
        self.parser['tag'] = {'url': url}
        self.save()

    def save(self):
        with open(self.file_path, 'w') as config_file:
            self.parser.write(config_file)
