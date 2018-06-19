"""
Application source for the gisrep issues reporter tool

Attributes:
    DEFAULT_CONFIG_FILE (str): Default config file name
    DEFAULT_CONFIG_FILEPATH (str): Full file path to default config file
    DEFAULT_CONFIG_DIR (str): Default config file directory
"""
import os
from pathlib import Path

import click
from github import GithubException
import keyring
import attr

from gisrep.config import Config
from gisrep.errors import GisrepError
from gisrep.reporters.reporter import create_reporter

DEFAULT_CONFIG_DIR = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisreprc"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
DEFAULT_TEMPLATE = 'simple_report.md'


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


@click.group()
def cli():
    """Main function for Gisrep tool
    """

    # Parse command line arguments
    pass


@cli.command()
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


def pathlib_wrapper(ctx, param, value):
    """Wrap a path argument in a pathlib.Path

    Args:
        ctx (click.Context): Click context
        param (str): Parameter name
        value (click.Path): The path argument

    Returns:
        pathlib.Path: The wrapped path
    """
    del ctx, param
    # Wrap any paths in a pathlib object
    if value is not None:
        return Path(value)
    return value


@attr.s()
class CommonOptions(object):
    template = attr.ib(type=click.Path)
    query = attr.ib(type=str)
    config = attr.ib(type=click.File)


pass_common = click.make_pass_decorator(CommonOptions)


@cli.group()
@click.argument('query')
@click.option(
    '--template',
    type=click.Path('rb'),
    callback=pathlib_wrapper,
    help="Custom template for formatting the results")
@click.option(
    '--config',
    type=click.File('rb'),
    help="Path to gisrep config file")
@click.pass_context
def report(ctx, query, template, config):
    """Publishes a report of nicely formatted issues specified by a
    Github issues search query (see
    help.github.com/articles/searching-issues-and-pull-requests/)

    \b
    QUERY: The Github query to find issues for
    """

    # Save context
    ctx.obj = CommonOptions(
        query=query,
        template=template,
        config=config)


@report.command()
@click.option('--username', help="Github username")
@click.option('--password', help="Github password")
@pass_common
def github(common, username, password):
    """Publish issues from a Github search query
    (see help.github.com/articles/searching-issues-and-pull-requests/)"""
    generate_report("github", common, username=username, password=password)


@report.command()
@click.option('--token', help="GitLab personal access token")
@click.option(
    '--url',
    default="https://gitlab.com",
    help="GitLab instance URL")
@pass_common
def gitlab(common, token, url):
    """Publish issues from a GitLab search query
    (see https://docs.gitlab.com/ee/user/search/)"""
    generate_report("gitlab", common, token=token, url=url)


def generate_report(reporter_name, common, **kwargs):
    # Get reporter
    reporter = create_reporter(reporter_name, **kwargs)

    # Generate report
    report = reporter.generate_report(common.query, common.template)

    # Output report
    click.echo(report)


def main():
    """Entry point to command line application
    """

    # Parse command line arguments
    try:
        cli(  # pylint: disable=unexpected-keyword-arg
            obj={'is_internal_template': False})
    except GisrepError as exc:
        click.echo("Gisrep Error: {}".format(exc))
    except GithubException as exc:
        click.echo("Github API Error: {}".format(exc))
    except keyring.errors.KeyringError as exc:
        click.echo("Keyring Error: {}".format(exc))


if __name__ == '__main__':
    main()
