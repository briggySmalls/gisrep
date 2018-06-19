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
from gisrep.reporters.gitlab import pass_gitlab
from gisrep.reporters.github import pass_github

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
    config = attr.ib(type=click.File)


pass_common = click.make_pass_decorator(CommonOptions)


@cli.group()
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
def report(ctx, template, config):
    """Publishes a report of nicely formatted issues specified by a
    Github issues search query (see
    help.github.com/articles/searching-issues-and-pull-requests/)
    """

    # Save context
    ctx.obj = CommonOptions(
        template=template,
        config=config)


@report.command()
@pass_github
@pass_common
def github(common, reporter, query):
    """Publish issues from a Github search query
    (see help.github.com/articles/searching-issues-and-pull-requests/)"""
    generate_report(common, reporter, query)


@report.command()
@pass_gitlab
@pass_common
def gitlab(common, reporter, query):
    """Publish issues from a GitLab search query
    (see https://docs.gitlab.com/ee/user/search/)"""
    generate_report(common, reporter, query)


def generate_report(common, reporter, query):
    # Generate report
    report = reporter.generate_report(query, common.template)

    # Output report
    click.echo(report)


def main():
    """Entry point to command line application
    """

    # Parse command line arguments
    try:
        cli()
    except GisrepError as exc:
        click.echo("Gisrep Error: {}".format(exc))
    except GithubException as exc:
        click.echo("Github API Error: {}".format(exc))
    except keyring.errors.KeyringError as exc:
        click.echo("Keyring Error: {}".format(exc))


if __name__ == '__main__':
    main()
