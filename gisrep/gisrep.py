"""
Application source for the gisrep issues reporter tool

Attributes:
    DEFAULT_CONFIG_FILE (str): Default config file name
    DEFAULT_CONFIG_FILEPATH (str): Full file path to default config file
    DEFAULT_CONFIG_DIR (str): Default config file directory
"""

import getpass
import os
import sys

from github import Github

from .cli import Cli
from .config import Config
from .templates.template_manager import (
    InternalTemplateManager, ExternalTemplateManager)

DEFAULT_CONFIG_DIR = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisrep_config"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    os.path.expanduser("~"), DEFAULT_CONFIG_FILE)


def main():
    """Main function for Gisrep tool
    """

    handlers = {
        'init': init,
        'report': report,
        'list': list_templates,
    }
    # Parse command line arguments
    cli = Cli(handlers)
    cli.parse(sys.argv[1:])


def init(args):
    """Initialises the tool config file

    Args:
        args (argparse.Namespace): Command arguments
    """
    # Prompt for username and password
    username = input("Github username:")
    password = getpass.getpass("Github password:")

    initial_config = {
        'username': username,
        'password': password,
    }

    # Initialise config file
    Config(
        DEFAULT_CONFIG_FILEPATH,
        initial_config=initial_config,
        force=args.force)


def report(args):
    """Publishes a report using specified query, template and output

    Args:
        args (argparse.Namespace): Command arguments
    """
    # Create the template manger
    if args.user_template:
        # We have been passed a template file path
        template_dir = os.path.dirname(
            os.path.abspath(args.user_template))
        template_tag = os.path.splitext(
            os.path.basename(args.user_template))[0]
        builder = ExternalTemplateManager(template_dir)
    elif args.template:
        # We have been passed a template tag
        template_tag = args.template
        builder = InternalTemplateManager()

    # Create PyGithub API object
    if os.path.exists(DEFAULT_CONFIG_FILEPATH):
        # Read in the existing config
        config = Config(DEFAULT_CONFIG_FILEPATH)
        # Instantiate an API client with Github credentials
        credentials = config.get_credentials()
        api = Github(
            credentials['username'],
            credentials['password'])
    else:
        # Instantiate an API client without Github credentials
        api = Github()

    # Request the issues
    issues = api.search_issues(
        args.query,
        sort="created",
        order="asc")

    # Generate report
    report_obj = builder.generate(
        template_tag,
        issues)

    # Output report
    print(report_obj)


def list_templates(args):  # pylint: disable=unused-argument
    """Lists the templates available for publishing

    Args:
        args (argparse.Namespace): Command arguments
    """
    builder = InternalTemplateManager()
    for template in builder.list():
        print(template)


if __name__ == '__main__':
    main()
