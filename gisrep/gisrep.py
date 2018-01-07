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

from github import Github, GithubException
import keyring

from .cli import Cli
from .config import Config
from .errors import GisrepError
from .templates.template_manager import (
    ExternalTemplateManager, InternalTemplateManager)

DEFAULT_CONFIG_DIR = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisreprc"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)


def _get_credentials(args):
    """Gets Github credentials from command line or config file

    Args:
        args (list): List of command line arguments passed to gisrep

    Returns:
        dict: Github credentials
    """
    if args.username:
        # Get credentials from command line
        assert args.password
        credentials = {
            'username': args.username,
            'password': args.password,
        }
    else:
        # Try to get credentials from a config file
        if args.config:
            # User supplied a config file path
            config_filepath = args.config
        elif os.path.exists(DEFAULT_CONFIG_FILEPATH):
            # Global config file provided
            config_filepath = DEFAULT_CONFIG_FILEPATH
        else:
            # There are no credentials to be used
            return None

        # Create a config object
        config = Config(config_filepath)

        # Instantiate an API client with Github credentials
        credentials = config.get_credentials()

    return credentials


def _get_template_manager(args):
    """Gets template objects

    Args:
        args (list): List of command line arguments passed to gisrep

    Returns:
        Tuple(TemplateManager, str): Template manager and tag of template
    """
    if args.external:
        # We have been passed a template file path
        template_dir = os.path.dirname(
            os.path.abspath(args.external))
        template_tag = os.path.splitext(
            os.path.basename(args.external))[0]
        manager = ExternalTemplateManager(template_dir)
    elif args.internal:
        # We have been passed a template tag
        template_tag = args.internal
        manager = InternalTemplateManager()

    return manager, template_tag


def main():
    """Main function for Gisrep tool
    """
    # Create a CLI object for parsing invocation arguments
    handlers = {
        'init': init,
        'report': report,
        'list': list_templates,
    }
    cli = Cli(handlers)

    # Parse command line arguments
    try:
        cli.parse(sys.argv[1:])
    except GisrepError as exc:
        print("Gisrep Error: {}".format(exc))
    except GithubException as exc:
        print("Github API Error: {}".format(exc))
    except keyring.errors.KeyringError as exc:
        print("Keyring Error: {}".format(exc))


def init(args):
    """Initialises the tool config file

    Args:
        args (argparse.Namespace): Command arguments
    """
    directory = (
        os.path.abspath(args.local)
        if args.local else
        DEFAULT_CONFIG_DIR)

    if not os.path.exists(directory):
        raise GisrepError(
            "Cannot find config directory '{}'".format(directory))

    filepath = os.path.join(
        directory,
        DEFAULT_CONFIG_FILE)

    if not args.force and os.path.exists(filepath):
        raise GisrepError(
            "Config file '{}' already exists".format(filepath))

    # Prompt for username and password
    initial_config = {
        'username': input("Github username:"),
        'password': getpass.getpass("Github password:"),
    }

    # Initialise config file
    Config(
        filepath,
        initial_config=initial_config,
        force=args.force)


def report(args):
    """Publishes a report using specified query, template and output

    Args:
        args (argparse.Namespace): Command arguments
    """
    # Create the template manger
    builder, template_tag = _get_template_manager(args)

    # Attempt to get Github credentials
    credentials = _get_credentials(args)

    # Create PyGithub API object
    if credentials is not None:
        api = Github(
            credentials['username'],
            credentials['password'])
    else:
        api = Github()

    # Request the issues
    issues = api.search_issues(
        args.query,
        sort="created",
        order="asc")

    # Check issues were found
    if not issues.get_page(0):
        raise GisrepError("No matching issues found")

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
