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
import click

from .config import Config
from .errors import GisrepError
from .templates.template_manager import (
    ExternalTemplateManager, InternalTemplateManager)

DEFAULT_CONFIG_DIR = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisreprc"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)


def _get_credentials(config):
    """Gets Github credentials from a config file

    Args:
        args (list): List of command line arguments passed to gisrep

    Returns:
        dict: Github credentials
    """
    # Try to get credentials from a config file
    if config:
        # User supplied a config file path
        config_filepath = config
    elif os.path.exists(DEFAULT_CONFIG_FILEPATH):
        # Global config file provided
        config_filepath = DEFAULT_CONFIG_FILEPATH
    else:
        # There are no credentials to be used
        return None

    # Create a config object
    config = Config(config_filepath)

    # Instantiate an API client with Github credentials
    return config.get_credentials()


def _get_template_manager(template):
    """Gets template objects

    Args:
        template (str): Template provided by user

    Returns:
        Tuple(TemplateManager, str): Template manager and tag of template
    """
    if template:
        # We have been passed a template file path
        template_dir = os.path.dirname(
            os.path.abspath(template))
        template_tag = os.path.splitext(
            os.path.basename(template))[0]
        manager = ExternalTemplateManager(template_dir)
    else:
        # We have been passed a template tag
        template_tag = template
        manager = InternalTemplateManager()

    return manager, template_tag


@click.group()
def main():
    """Main function for Gisrep tool
    """

    # Parse command line arguments
    try:
        cli.parse(sys.argv[1:])
    except GisrepError as exc:
        print("Gisrep Error: {}".format(exc))
    except GithubException as exc:
        print("Github API Error: {}".format(exc))
    except keyring.errors.KeyringError as exc:
        print("Keyring Error: {}".format(exc))


@main.command()
@main.option(
    '--force/--no-force',
    default=False,
    help="Overwrite an existing config file")
@main.option(
    '--local/--global',
    default=False,
    help="Path to a directory in which to save the file")
@click.argument('username')
@click.password_option()
def init(username, password, force, local):
    """Creates a '.gisreprc' configuration file to store Github username and
    adds the password to the system password manager.

    Args:
        args (argparse.Namespace): Command arguments

    Raises:
        GisrepError: Description
    """
    directory = (
        os.path.abspath(local)
        if local else
        DEFAULT_CONFIG_DIR)

    if not os.path.exists(directory):
        raise GisrepError(
            "Cannot find config directory '{}'".format(directory))

    filepath = os.path.join(
        directory,
        DEFAULT_CONFIG_FILE)

    if not force and os.path.exists(filepath):
        raise GisrepError(
            "Config file '{}' already exists".format(filepath))

    # Prompt for username and password
    initial_config = {
        'username': username,
        'password': password,
    }

    # Initialise config file
    Config(
        filepath,
        initial_config=initial_config,
        force=force)


@main.command()
@click.argument('query')
@click.option('--credentials', nargs=2, type=str, help="Username and password")
@click.option(
    '--template',
    type=click.Path('rb'),
    help="External template for formatting results")
@click.option(
    '--config',
    type=click.File('rb'),
    help="Path to gisrep config file")
def report(query, template, credentials, config):
    """Publishes a report of nicely formatted Github issues specified by a
    Github issues search query (see
    help.github.com/articles/searching-issues-and-pull-requests/)

    Args:
        args (argparse.Namespace): Command arguments
    """

    # Attempt to get Github credentials
    if config and not credentials:
        credentials = _get_credentials(config)

    # Create PyGithub API object
    if credentials is not None:
        api = Github(
            credentials['username'],
            credentials['password'])
    else:
        api = Github()

    # Request the issues
    issues = api.search_issues(query, sort="created", order="asc")

    # Check issues were found
    if not issues.get_page(0):
        raise GisrepError("No matching issues found")

    # Create the template manger
    builder, template_tag = _get_template_manager(template)

    # Generate report
    report_obj = builder.generate(
        template_tag,
        issues)

    # Output report
    print(report_obj)


@main.command()
def list_templates():
    """Lists internal templates shipped with gisrep that may be used with the
    'report' command to format the results.

    Args:
        args (argparse.Namespace): Command arguments
    """
    builder = InternalTemplateManager()
    for template in builder.list():
        print(template)


if __name__ == '__main__':
    main()
