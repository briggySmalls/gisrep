"""
Application source for the gisrep issues reporter tool

Attributes:
    DEFAULT_CONFIG_FILE (str): Default config file name
    DEFAULT_CONFIG_FILEPATH (str): Full file path to default config file
    DEFAULT_CONFIG_DIR (str): Default config file directory
"""
import os

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


def _get_template_manager(internal, external):
    """Gets template objects

    Args:
        template (str): Template provided by user
        is_external (bool): Indicates template is external to gisrep

    Returns:
        Tuple(TemplateManager, str): Template manager and tag of template
    """
    if external:
        # We have been passed a template file path
        template_dir = os.path.dirname(
            os.path.abspath(template))
        template_tag = os.path.splitext(
            os.path.basename(template))[0]
        manager = ExternalTemplateManager(template_dir)
    else:
        # We have been passed a template tag
        template_tag = template if template is not None else 'simple_report.md'
        manager = InternalTemplateManager()

    return manager, template_tag


@click.group()
def main():
    """Main function for Gisrep tool
    """

    # Parse command line arguments
    pass


@main.command()
@click.option(
    '--force/--no-force',
    default=False,
    help="Overwrite an existing config file")
@click.option(
    '--local/--global',
    default=False,
    help="Path to a directory in which to save the file")
@click.argument('username')
@click.password_option()
def init(username, password, force, local):
    """Creates a '.gisreprc' configuration file to store Github username and
    adds the password to the system password manager.

    USERNAME: Github username
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


def internal_template_callback(ctx, _, value):
    if value:
        ctx.is_internal_template = True


def external_template_callback(ctx, _, value):
    if ctx.is_internal_template and value:
        # We only allow one of internal/external to be supplied
        click.echo("Only one of --internal/--external may be supplied")
        ctx.exit()


@main.command()
@click.argument('query')
@click.option(
    '--external',
    type=click.Path('rb'),
    help="Custom template for formatting the results",
    callback=external_template_callback)
@click.option(
    '--internal',
    type=str,
    default="simple_report.md",
    help="Internal Gisrep template for formatting the results",
    callback=internal_template_callback,
    is_eager=True)
@click.option(
    '--config',
    type=click.File('rb'),
    help="Path to gisrep config file")
@click.option('--credentials', nargs=2, type=str, help="Username and password")
def report(query, external, internal, config, credentials):
    """Publishes a report of nicely formatted Github issues specified by a
    Github issues search query (see
    help.github.com/articles/searching-issues-and-pull-requests/)

    \b
    QUERY: The Github query to find issues for
    """

    # Attempt to get Github credentials
    if not credentials:
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
    builder, template_tag = _get_template_manager(internal, external)

    # Generate report
    report_obj = builder.generate(
        template_tag,
        issues)

    # Output report
    print(report_obj)


@main.command()
def templates():
    """Lists internal templates shipped with gisrep that may be used with the
    'report' command to format the results.
    """
    builder = InternalTemplateManager()
    for template in builder.list():
        print(template)


if __name__ == '__main__':
    main(is_internal_template=False)
